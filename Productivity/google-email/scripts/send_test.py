"""Send a simple test email using Gmail API
Usage: python send_test.py recipient@example.com
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import sys
from pathlib import Path

TOKEN = Path(r'C:/Users/mz038/.nanobot/workspace/token.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

if not TOKEN.exists():
    print('token.json not found at', TOKEN)
    sys.exit(1)
creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
service = build('gmail', 'v1', credentials=creds)

recipient = sys.argv[1] if len(sys.argv) > 1 else None
if not recipient:
    print('Usage: python send_test.py recipient@example.com')
    sys.exit(1)

msg = MIMEText('這是一封測試郵件。','plain','utf-8')
msg['to'] = recipient
msg['from'] = 'me'
msg['subject'] = '測試郵件'
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
res = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print('Sent message id:', res.get('id'))
