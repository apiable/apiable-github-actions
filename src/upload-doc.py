import sys
import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_access_token(client_id, client_secret):
    url = "https://developer.apiable.io/api/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    logging.info(f"send request url={url}, client_id={client_id}")
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        logging.info("Access token retrieved successfully.")
        return response.json().get("access_token")
    else:
        logging.error(f"Failed to get access token: {response.text}")
        raise Exception(f"Failed to get access token: {response.text}")

def download_openapi_spec(open_api_spec_url):
    response = requests.get(open_api_spec_url)
    if response.status_code == 200:
        with open("temp.json", "w") as file:
            file.write(response.text)
        logging.info("OpenAPI spec downloaded successfully.")
        return "temp.json"
    else:
        logging.error(f"Failed to download OpenAPI spec: {response.text}")
        raise Exception(f"Failed to download OpenAPI spec: {response.text}")

def upload_openapi_spec(api_url, token):
    url = f"{api_url}/api/files/upload"
    headers = {
        "X-API-Version": "latest",
        "Authorization": f"Bearer {token}"
    }
    with open("temp.json", "rb") as file:
        files = {"file": ("temp.json", file, "application/json")}
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 202:
            logging.info("OpenAPI spec uploaded successfully.")
            return response.json().get("url")
        else:
            logging.error(f"Failed to upload OpenAPI spec: {response.text}")
            raise Exception(f"Failed to upload OpenAPI spec: {response.text}")

def update_documentation(api_url, token, open_api_url, planid):
    version = os.popen("date +%Y-%m-%d").read().strip()
    url = f"{api_url}/api/plans/{planid}/docs"
    headers = {
        "accept": "application/json",
        "X-API-Version": "latest",
        "Authorization": f"Bearer {token}",
        "content-type": "application/json"
    }
    data = {
        "version": version,
        "active": True,
        "retrievalType": "CICD",
        "url": open_api_url,
        "name": f"Documentation v{version}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        logging.info("Documentation updated successfully.")
        return response.json()
    else:
        logging.error(f"Failed to update documentation: {response.text}")
        raise Exception(f"Failed to update documentation: {response.text}")

def main():
    api_key = os.environ.get("api_key")
    api_secret = os.environ.get("api_secret")
    api_url = os.environ.get("api_url")
    open_api_spec_url = os.environ.get("open_api_spec_url")
    planid = os.environ.get("planid")

    try:
        # Step 1: Generate JWT
        token = get_access_token(api_key, api_secret)

        # Step 2: Download and Upload OpenAPI Spec
        download_openapi_spec(open_api_spec_url)
        open_api_url = upload_openapi_spec(api_url, token)

        # Step 3: Update Documentation
        response = update_documentation(api_url, token, open_api_url, planid)

        # Log the response to the GitHub Actions output
        logging.info(f"::set-output name=response::{response}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()