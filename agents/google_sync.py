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
# Replace this with the Folder ID you copied from your browser URL
FOLDER_ID = '16cXE3sTts9wgW17XkwYbm7cz21P9KKno' 

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Create the Doc and PLACE it in your shared folder
file_metadata = {
    'name': 'Liber Draft: New Outline',
    'mimeType': 'application/vnd.google-apps.document',
    'parents': [FOLDER_ID] # This ensures it goes to YOUR folder
}

# Use the Drive API to create the file in the specific folder
doc_file = drive_service.files().create(body=file_metadata, fields='id').execute()
doc_id = doc_file.get('id')

# 4. Insert the Text into the new Doc
requests = [{'insertText': {'location': {'index': 1}, 'text': text_content}}]
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

print(f"Success! Document created in your folder. ID: {doc_id}")
