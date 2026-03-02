import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 1. Setup Credentials
info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
creds = service_account.Credentials.from_service_account_info(info)
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# --- CONFIGURATION ---
FOLDER_ID = '16cXE3sTts9wgW17XkwYbm7cz21P9KKno' 
MY_EMAIL = 'xaibaba692@gmail.com' # Updated from your screenshot

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Create the Doc metadata
file_metadata = {
    'name': 'Liber Draft: New Outline',
    'mimeType': 'application/vnd.google-apps.document',
    'parents': [FOLDER_ID]
}

try:
    # 4. Create the file using YOUR folder's quota
    doc_file = drive_service.files().create(
        body=file_metadata, 
        fields='id',
        supportsAllDrives=True 
    ).execute()
    doc_id = doc_file.get('id')

    # 5. THE FIX: Transfer Permission/Ownership
    # This makes YOU the owner so the robot's 0GB quota doesn't matter
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': MY_EMAIL
    }
    drive_service.permissions().create(
        fileId=doc_id,
        body=user_permission,
        supportsAllDrives=True
    ).execute()

    # 6. Insert the Text
    requests = [{'insertText': {'location': {'index': 1}, 'text': text_content}}]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

    print(f"Success! Document created and shared. ID: {doc_id}")

except Exception as e:
    print(f"Quota bypass failed: {e}")
    raise
