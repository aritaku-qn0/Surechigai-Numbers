from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import requests
import os
import base64
import cv2
import numpy as np
import re

app = Flask(__name__)
CORS(app)

def normalize_ocr_text(text):
    table = str.maketrans(
        "０１２３４５６７８９ー－‐‑–—―−",
        "0123456789--------"
    )
    return text.translate(table)


def format_plate_number(raw):
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 3:
        digits = "0" + digits
    if len(digits) != 4:
        return None
    return f"{digits[:2]}-{digits[2:]}"


def extract_plate_number(text):
    normalized = normalize_ocr_text(text)
    candidates = []

    for match in re.finditer(r"(?<!\d)(\d{1,2})\s*-\s*(\d{2})(?!\d)", normalized):
        plate = format_plate_number(match.group(1) + match.group(2))
        if plate:
            candidates.append(plate)

    for match in re.finditer(r"(?<!\d)(\d{2})\s+(\d{2})(?!\d)", normalized):
        plate = format_plate_number(match.group(1) + match.group(2))
        if plate:
            candidates.append(plate)

    for match in re.finditer(r"(?<!\d)(\d{4})(?!\d)", normalized):
        plate = format_plate_number(match.group(1))
        if plate:
            candidates.append(plate)

    return candidates[-1] if candidates else None

PREF_MAP = {
    # 北海道
    "札幌":"北海道",
    "函館":"北海道",
    "旭川":"北海道",
    "帯広":"北海道",
    "北見":"北海道",
    "釧路":"北海道",

    # 東北
    "青森":"青森",
    "弘前":"青森",
    "八戸":"青森",
    "岩手":"岩手",
    "盛岡":"岩手",
    "平泉":"岩手",
    "仙台":"宮城",
    "宮城":"宮城",
    "秋田":"秋田",
    "山形":"山形",
    "庄内":"山形",
    "福島":"福島",
    "会津":"福島",
    "郡山":"福島",

    # 関東
    "水戸":"茨城",
    "土浦":"茨城",
    "つくば":"茨城",
    "宇都宮":"栃木",
    "那須":"栃木",
    "群馬":"群馬",
    "前橋":"群馬",
    "高崎":"群馬",
    "大宮":"埼玉",
    "川越":"埼玉",
    "所沢":"埼玉",
    "越谷":"埼玉",
    "春日部":"埼玉",
    "熊谷":"埼玉",
    "千葉":"千葉",
    "成田":"千葉",
    "習志野":"千葉",
    "市川":"千葉",
    "船橋":"千葉",
    "松戸":"千葉",
    "品川":"東京",
    "足立":"東京",
    "多摩":"東京",
    "八王子":"東京",
    "世田谷":"東京",
    "杉並":"東京",
    "江東":"東京",
    "葛飾":"東京",
    "板橋":"東京",
    "練馬":"東京",
    "横浜":"神奈川",
    "川崎":"神奈川",
    "湘南":"神奈川",
    "相模":"神奈川",

    # 中部
    "新潟":"新潟",
    "長岡":"新潟",
    "上越":"新潟",
    "富山":"富山",
    "金沢":"石川",
    "福井":"福井",
    "山梨":"山梨",
    "松本":"長野",
    "長野":"長野",
    "諏訪":"長野",
    "岐阜":"岐阜",
    "飛騨":"岐阜",
    "静岡":"静岡",
    "浜松":"静岡",
    "沼津":"静岡",
    "富士山":"静岡",
    "名古屋":"愛知",
    "豊橋":"愛知",
    "三河":"愛知",

    # 関西
    "三重":"三重",
    "鈴鹿":"三重",
    "滋賀":"滋賀",
    "京都":"京都",
    "大阪":"大阪",
    "なにわ":"大阪",
    "和泉":"大阪",
    "堺":"大阪",
    "神戸":"兵庫",
    "姫路":"兵庫",
    "奈良":"奈良",
    "和歌山":"和歌山",

    # 中国・四国
    "鳥取":"鳥取",
    "島根":"島根",
    "岡山":"岡山",
    "倉敷":"岡山",
    "広島":"広島",
    "福山":"広島",
    "山口":"山口",
    "下関":"山口",
    "徳島":"徳島",
    "香川":"香川",
    "愛媛":"愛媛",
    "高知":"高知",

    # 九州・沖縄
    "福岡":"福岡",
    "北九州":"福岡",
    "久留米":"福岡",
    "筑豊":"福岡",
    "佐賀":"佐賀",
    "長崎":"長崎",
    "佐世保":"長崎",
    "熊本":"熊本",
    "大分":"大分",
    "宮崎":"宮崎",
    "鹿児島":"鹿児島",
    "奄美":"鹿児島",
    "沖縄":"沖縄"
}
@app.route("/")
def index():
    return send_file("すれ違いナンバーズ/numplate_game.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("すれ違いナンバーズ", filename)

@app.route("/analyze", methods=["POST"])
def analyze():
    
    print("analyze開始", flush=True)

    data = request.json

    image_base64 = data["image"]

    image_bytes = base64.b64decode(image_base64)

    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, buffer = cv2.imencode(".jpg", image)
    image_bytes = buffer.tobytes()

    api_key = os.environ["OCR_SPACE_API_KEY"]

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={
            "image": ("plate.jpg", image_bytes)
        },
        data={
            "apikey": api_key,
            "language": "jpn",
            "OCREngine": "2"
        }
    )

    result = response.json()

    text = ""

    if result.get("ParsedResults"):
        text = result["ParsedResults"][0]["ParsedText"]
    
    plate_number = extract_plate_number(text)

    print("OCR結果:", (text), flush=True)
    print("読み取り番号:", plate_number, flush=True)
    print(result, flush=True)

    for area, pref in PREF_MAP.items():
        if area in text:
            if not plate_number:
                return jsonify({
                    "found": False,
                    "reason": "number_not_found",
                    "prefecture": pref,
                    "plate_area": area
                })

            return jsonify({
                "found": True,
                "prefecture": pref,
                "plate_area": area,
                "plate_number": plate_number
            })

    return jsonify({
        "found": False
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
