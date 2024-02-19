import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Authenticate with Firebase
cred = credentials.Certificate(' E:\Solution_Challenge\google_solution_challenge\frontend\serviceAccountKey.json')  # Path to your service account key file
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Function to store data in Firestore
def store_data(user_id, potability_data):
    # Reference to the user's document
    user_ref = db.collection('users').document(user_id)

    # Update or set data in the user's document
    user_ref.set({
        'water_potability_data': potability_data
    })

# Example usage
if __name__ == "__main__":
    # Assuming you have user_id and potability_data
    user_id = "unique_user_id"
    potability_data = {
        'parameter1': value1,
        'parameter2': value2,
        # Add more parameters as needed
    }

    # Store data in Firestore
    store_data(user_id, potability_data)
