import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
# For development/local testing, you can download a service account JSON file
# from the Firebase Console (Project Settings > Service Accounts)
# and set GOOGLE_APPLICATION_CREDENTIALS in your .env
# If deployed on GCP, it will automatically use default credentials.

try:
    if not firebase_admin._apps:
        # If GOOGLE_APPLICATION_CREDENTIALS is not set, this will attempt to use
        # Application Default Credentials (ADC) or run unauthenticated.
        # The Firebase Admin SDK requires a Service Account JSON for full token verification
        # outside of Google Cloud.
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "app/firebase-credentials.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            print("ERROR: firebase-credentials.json not found! Firebase Auth will fail.")
            # Explicitly provide the project ID as a last resort
            firebase_admin.initialize_app(options={'projectId': 'carwash-mgmt-system-41402'})
except Exception as e:
    print(f"Warning: Failed to initialize Firebase Admin SDK: {e}")

def verify_firebase_token(id_token: str):
    """
    Verifies a Firebase ID token.
    Returns the decoded token dictionary if valid.
    Raises an exception if invalid.
    """
    try:
        # Added clock_skew_seconds to fix issues with local time syncing slightly behind Google's servers
        decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=60)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid Firebase ID token: {e}")
