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
MY_EMAIL = 'xaibaba629@gmail.com' # Your real Gmail from the screenshot

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Create the Doc metadata
file_metadata = {
    'name': 'Liber Draft: New Outline',
    'mimeType': 'application/vnd.google-apps.document',
    'parents': [FOLDER_ID]
}

# 4. Create the file and fix the Quota issue
# We use 'supportsAllDrives=True' to ensure it can write to your shared folder
doc_file = drive_service.files().create(
    body=file_metadata, 
    fields='id',
    supportsAllDrives=True 
).execute()

doc_id = doc_file.get('id')

# 5. Insert the Text
requests = [{'insertText': {'location': {'index': 1}, 'text': text_content}}]
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

print(f"Success! Document created. ID: {doc_id}")
