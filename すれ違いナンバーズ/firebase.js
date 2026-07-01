import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";

import {
  getAuth,
  signOut,
  onAuthStateChanged,
  deleteUser,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  reauthenticateWithCredential,
  EmailAuthProvider
} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";

import {
  getFirestore,
  doc,
  getDoc,
  getDocs,
  setDoc,
  updateDoc,
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

window.signOut = signOut;
window.onAuthStateChanged = onAuthStateChanged;
window.doc = doc;
window.getDoc = getDoc;
window.getDocs = getDocs;
window.setDoc = setDoc;
window.updateDoc = updateDoc;
window.deleteDoc = deleteDoc;
window.runTransaction = runTransaction;
window.deleteUser = deleteUser;
window.onSnapshot = onSnapshot;
window.collection = collection;
window.createUserWithEmailAndPassword = createUserWithEmailAndPassword;
window.signInWithEmailAndPassword = signInWithEmailAndPassword;
window.EmailAuthProvider = EmailAuthProvider;
window.reauthenticateWithCredential = reauthenticateWithCredential;

console.log("deleteUser =", deleteUser);
console.log("reauthenticateWithPopup =", reauthenticateWithPopup);