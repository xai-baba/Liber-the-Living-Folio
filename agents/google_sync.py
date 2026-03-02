import os
import json
import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 1. Setup Credentials
info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
creds = service_account.Credentials.from_service_account_info(info)
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# 2. Read the Outline
with open('latest_outline.md', 'r') as f:
    text_content = f.read()

# 3. Create the Doc
doc = docs_service.documents().create(body={'title': 'Liber Draft: New Project'}).execute()
doc_id = doc.get('documentId')

# 4. Insert the Text
requests = [{'insertText': {'location': {'index': 1}, 'text': text_content}}]
docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

print(f"Document created! ID: {doc_id}")
