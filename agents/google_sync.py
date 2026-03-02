import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2 import service_account

# 1. Setup Credentials
info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
creds = service_account.Credentials.from_service_account_info(info)
drive_service = build('drive', 'v3', credentials=creds)

# --- CONFIGURATION ---
FOLDER_ID = '16cXE3sTts9wgW17XkwYbm7cz21P9KKno' 

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Use the Media Upload method
# This treats the outline as a 'file upload' which is more likely to use your quota
media = MediaInMemoryUpload(text_content.encode('utf-8'), mimetype='text/markdown')

file_metadata = {
    'name': 'Liber Draft: New Outline',
    'mimeType': 'application/vnd.google-apps.document', # Convert to Google Doc format
    'parents': [FOLDER_ID]
}

try:
    # 4. Perform the Upload
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()
    
    print(f"Success! Document created via Media Upload. ID: {file.get('id')}")

except Exception as e:
    print(f"Media Upload failed: {e}")
    raise
