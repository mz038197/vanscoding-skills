"""List messages matching a query using Gmail API
Usage: python list_messages.py "subject:APCS" --max 50
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys
from pathlib import Path

TOKEN = Path(r'C:/Users/mz038/.nanobot/workspace/token.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

if not TOKEN.exists():
    print('token.json not found at', TOKEN)
    sys.exit(1)
creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
service = build('gmail', 'v1', credentials=creds)

import argparse
p=argparse.ArgumentParser()
p.add_argument('q', help='Gmail search query (quoted)')
p.add_argument('--max', type=int, default=50)
args=p.parse_args()

res = service.users().messages().list(userId='me', q=args.q, maxResults=args.max).execute()
msgs = res.get('messages', [])
print('Found', len(msgs), 'messages')
for m in msgs:
    print(m['id'])
