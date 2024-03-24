// Importez les scripts nécessaires de Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
    import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-analytics.js";
    import { getMessaging, getToken } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-messaging.js";

// Initialisez l'application Firebase avec votre configuration

  // Initialize Firebase
initializeApp({
    apiKey: "AIzaSyBdT5JVHUcNYRub3dsFUKRiIf8Xm8ZYU6E",
    authDomain: "smart-invest-f557b.firebaseapp.com",
    projectId: "smart-invest-f557b",
    storageBucket: "smart-invest-f557b.appspot.com",
    messagingSenderId: "166471964412",
    appId: "1:166471964412:web:046e9786fa06d85cc1a979",
    measurementId: "G-TZPJBC9EGM"
});

// Récupérez une instance de Firebase Messaging pour gérer les messages en arrière-plan
