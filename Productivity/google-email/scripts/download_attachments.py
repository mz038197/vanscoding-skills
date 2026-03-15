"""Download attachments from a message
Usage: python download_attachments.py MESSAGE_ID --outdir ./attachments
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64, os, sys
from pathlib import Path

TOKEN = Path(r'C:/Users/mz038/.nanobot/workspace/token.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
if not TOKEN.exists():
    print('token.json not found at', TOKEN)
    sys.exit(1)
creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
service = build('gmail', 'v1', credentials=creds)

if len(sys.argv) < 2:
    print('Usage: python download_attachments.py MESSAGE_ID [OUTDIR]')
    sys.exit(1)
msg_id = sys.argv[1]
outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('./attachments')
outdir.mkdir(parents=True, exist_ok=True)

msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
parts = msg.get('payload', {}).get('parts', [])
for part in parts:
    if part.get('filename') and part.get('body', {}).get('attachmentId'):
        att_id = part['body']['attachmentId']
        att = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
        data = base64.urlsafe_b64decode(att['data'].encode('ASCII'))
        fn = part['filename']
        p = outdir / fn
        p.write_bytes(data)
        print('Wrote', p)
