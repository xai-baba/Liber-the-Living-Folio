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
# Ensure these are exactly correct
FOLDER_ID = '16cXE3sTts9wgW17XkwYbm7cz21P9KKno' 
MY_EMAIL = 'xaibaba692@gmail.com' 

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Create the Doc metadata
# We REMOVE the robot as the potential owner here
file_metadata = {
    'name': 'Liber Draft: New Outline',
    'mimeType': 'application/vnd.google-apps.document',
    'parents': [FOLDER_ID]
}

try:
    # 4. Create the file - FORCING it to use the Parent Folder's quota
    doc_file = drive_service.files().create(
        body=file_metadata, 
        fields='id',
        supportsAllDrives=True,
        # This tells Google to use YOUR storage quota, not the robot's
        enforceSingleParent=True 
    ).execute()
    doc_id = doc_file.get('id')

    # 5. Insert the Text
    requests = [{'insertText': {'location': {'index': 1}, 'text': text_content}}]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

    print(f"Success! Document created. Check your Google Drive folder.")

except Exception as e:
    print(f"Sync failed: {e}")
    raise
