import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getAuth, GoogleAuthProvider } from "firebase/auth";


const firebaseConfig = {
  apiKey: "AIzaSyCJYeCBWwTbQPUm98tAm5tfJ2trtv31pGA",
  authDomain: "ai-fake-profile-detection-fd68f.firebaseapp.com",
  databaseURL: "https://ai-fake-profile-detectio-fd68f-default-rtdb.firebaseio.com/",
  projectId: "ai-fake-profile-detection-fd68f",
  storageBucket: "ai-fake-profile-detection-fd68f.appspot.com",
  messagingSenderId: "849158737028",
  appId: "1:849158737028:web:cafa478acd73818d78c6d1"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { db, auth, provider };