import os
import json
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2 import service_account

# 1. Setup Credentials
info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
creds = service_account.Credentials.from_service_account_info(info)
drive_service = build('drive', 'v3', credentials=creds)

# --- CONFIGURATION ---
FOLDER_ID = '16cXE3sTts9wgW17XkwYbm7cz21P9KKno' 
MY_EMAIL = 'xaibaba692@gmail.com'

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

try:
    # STEP A: Create an EMPTY file metadata (0 bytes)
    file_metadata = {
        'name': 'Liber Draft: New Outline',
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [FOLDER_ID]
    }
    
    # STEP B: Create the empty file
    file = drive_service.files().create(
        body=file_metadata,
        fields='id',
        supportsAllDrives=True
    ).execute()
    doc_id = file.get('id')
    
    # STEP C: Give YOU permission immediately
    # This links the file to your 15GB quota
    drive_service.permissions().create(
        fileId=doc_id,
        body={'type': 'user', 'role': 'writer', 'emailAddress': MY_EMAIL},
        supportsAllDrives=True
    ).execute()

    # STEP D: Now UPLOAD the content to the existing ID
    media = MediaInMemoryUpload(text_content.encode('utf-8'), mimetype='text/plain')
    drive_service.files().update(
        fileId=doc_id,
        media_body=media,
        supportsAllDrives=True
    ).execute()
    
    print(f"Success! Quota bypassed. Doc ID: {doc_id}")

except Exception as e:
    print(f"Bypass failed: {e}")
    raise
