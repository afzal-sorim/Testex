import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import httpx

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your_google_client_id_here")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "your_github_client_id")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "your_github_client_secret")
MICROSOFT_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "your_azure_client_id")
MICROSOFT_TENANT_ID = os.getenv("AZURE_TENANT_ID", "common")

def verify_google_token(token: str) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError as e:
        raise ValueError(f"Invalid Google token: {str(e)}")

def verify_microsoft_token(token: str) -> dict:
    # Minimal decoding for MSAL React token (since backend gets access token, but frontend could also send id_token).
    # We will fetch user info from Microsoft Graph API
    import requests
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError("Invalid Microsoft token")

async def get_github_access_token(code: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code
            }
        )
        data = response.json()
        if "access_token" in data:
            return data["access_token"]
        raise ValueError("Failed to get GitHub access token")

async def get_github_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        # Get user profile
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        
        # Get emails (since public profile might not have it)
        emails_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        emails_data = emails_response.json()
        
        primary_email = None
        for email in emails_data:
            if email.get("primary") and email.get("verified"):
                primary_email = email.get("email")
                break
                
        if not primary_email and len(emails_data) > 0:
            primary_email = emails_data[0].get("email")
            
        user_data["email"] = primary_email
        return user_data
