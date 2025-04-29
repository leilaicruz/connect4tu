import requests
import json
import yaml
import os
from .env_utils import load_env_from_script

def upload_dataset(metadata, api_token, base_url="https://next.data.4tu.nl", endpoint="/v2/account/articles"):
    url = base_url + endpoint
    headers = {
        "Authorization": f"Bearer {api_token}",  # <-- FIX: should be Bearer, not token
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=metadata, timeout=60)

    if response.ok:
        print("✅ Upload successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)

def upload_main(yaml_file, base_url="https://next.data.4tu.nl", endpoint="/v2/account/articles"):
    # Load environment variables
    load_env_from_script()

    # Get the token
    api_token = os.getenv("NEXT_API_TOKEN")
    if not api_token:
        raise ValueError("Environment variable NEXT_API_TOKEN not set. Make sure your .env file defines it.")

    try:
        with open(yaml_file, "r") as f:
            metadata = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading YAML file: {e}")
        return

    print("📦 Loaded metadata:")
    print(json.dumps(metadata, indent=2))

    # Upload
    upload_dataset(metadata, api_token, base_url, endpoint)
    print("🚀 Uploading dataset...")