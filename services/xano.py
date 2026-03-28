import requests
import os

# Get API details from environment variables
XANO_API_URL = os.environ.get("XANO_API_URL")
XANO_API_KEY = os.environ.get("XANO_API_KEY")

def get_subjects():
    """
    Fetches all subjects from the Xano database.
    """
    if not XANO_API_URL or not XANO_API_KEY:
        return {"error": "XANO_API_URL and XANO_API_KEY must be set as environment variables."}

    headers = {
        "Authorization": f"Bearer {XANO_API_KEY}"
    }
    try:
        response = requests.get(f"{XANO_API_URL}/subject", headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def add_subject(name, user_id=1): # Placeholder user_id
    """
    Adds a new subject to the Xano database.
    """
    if not XANO_API_URL or not XANO_API_KEY:
        return {"error": "XANO_API_URL and XANO_API_KEY must be set as environment variables."}

    headers = {
        "Authorization": f"Bearer {XANO_API_KEY}"
    }
    payload = {
        "name": name,
        "user_id": user_id
    }
    try:
        response = requests.post(f"{XANO_API_URL}/subject", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
