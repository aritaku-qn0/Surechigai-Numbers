import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";

import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  deleteUser,
  reauthenticateWithPopup
} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";

import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  deleteDoc,
  runTransaction,
  onSnapshot,
  collection
} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDDHkY0j2G0jGyimRTrUr3CpArDHc5hQ98",
  authDomain: "surechigai-numbers.firebaseapp.com",
  projectId: "surechigai-numbers",
  storageBucket: "surechigai-numbers.firebasestorage.app",
  messagingSenderId: "1049904814367",
  appId: "1:1049904814367:web:54203af0eff830c4a9382a"
};

const app = initializeApp(firebaseConfig);

window.auth = getAuth(app);
window.db = getFirestore(app);
window.provider = new GoogleAuthProvider();

window.signInWithPopup = signInWithPopup;
window.signOut = signOut;
window.onAuthStateChanged = onAuthStateChanged;
window.doc = doc;
window.getDoc = getDoc;
window.setDoc = setDoc;
window.deleteDoc = deleteDoc;
window.runTransaction = runTransaction;
window.deleteUser = deleteUser;
window.reauthenticateWithPopup = reauthenticateWithPopup;
window.onSnapshot = onSnapshot;
window.collection = collection;

console.log("deleteUser =", deleteUser);
console.log("reauthenticateWithPopup =", reauthenticateWithPopup);