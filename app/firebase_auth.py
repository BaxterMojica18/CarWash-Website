import firebase_admin
from firebase_admin import credentials, auth
import os
import json

try:
    if not firebase_admin._apps:
        firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "app/firebase-credentials.json")

        if firebase_creds_json:
            creds_dict = json.loads(firebase_creds_json)
            # Fix escaped newlines in private key
            if 'private_key' in creds_dict:
                creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from FIREBASE_CREDENTIALS_JSON env var")
        elif os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from credentials file")
        else:
            print("ERROR: No Firebase credentials found!")
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
