
const firebaseConfig = {
  apiKey: "AIzaSyBKS7n7FANYjS-fKhS25VcgP1vVzPuS9bQ",
  authDomain: "aquacare-88fdc.firebaseapp.com",
  projectId: "aquacare-88fdc",
  storageBucket: "aquacare-88fdc.appspot.com",
  messagingSenderId: "443735296838",
  appId: "1:443735296838:web:e2ebacb727dbb614e2f347",
  measurementId: "G-8DJK221G6M"
};

// Initialize Firebase

firebase.initializeApp(firebaseConfig);

// Reference to Firestore database
const db = firebase.firestore();

// Get references to your buttons
const monitoringButton = document.querySelector('.option2'); // Assuming option2 is your Monitoring button
const mapViewButton = document.querySelector('.option3'); // Assuming option3 is your Map view button

// Event listener for Monitoring button
monitoringButton.addEventListener('click', function() {
  // Here you can add code to perform actions related to monitoring
  // For example, you can retrieve data from Firestore or perform other actions
  console.log('Monitoring button clicked');
});

// Event listener for Map view button
mapViewButton.addEventListener('click', function() {
  // Here you can add code to perform actions related to map view
  // For example, you can navigate to a different page or perform other actions
  console.log('Map view button clicked');
});