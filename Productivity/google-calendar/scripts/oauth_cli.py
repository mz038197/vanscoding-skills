"""
OAuth CLI for Google Calendar (installed app flow)

Usage:
  python oauth_cli.py authorize
  python oauth_cli.py create --calendar primary --start 2026-02-27T18:00:00+08:00 --end 2026-02-27T19:00:00+08:00 --summary "標題" --attendees a@example.com,b@example.com --location "地點"
  python oauth_cli.py list --calendar primary --time-min 2026-02-27T17:00:00+08:00 --time-max 2026-02-27T20:00:00+08:00

Place your OAuth client secret at:
  C:/Users/<user>/.nanobot/workspace/client_secret.json

Authorize will open a browser to let you login and consent; token.json will be saved to the same workspace.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

WORKSPACE = os.path.join(os.path.expanduser('~'), '.nanobot', 'workspace')
CLIENT_SECRET_PATH = os.path.join(WORKSPACE, 'client_secret.json')
TOKEN_PATH = os.path.join(WORKSPACE, 'token.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def authorize():
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise SystemExit(f'找不到 OAuth client_secret.json，請放到: {CLIENT_SECRET_PATH}')
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    try:
        creds = flow.run_local_server(port=0)
    except Exception as e:
        # fallback to console flow
        print('無法使用 run_local_server（可能無法開啟瀏覽器），改用 console flow，請在終端貼上授權 url 並輸入 code。')
        creds = flow.run_console()
    with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
        f.write(creds.to_json())
    print('授權完成，token 已儲存至', TOKEN_PATH)


def print_auth_url():
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise SystemExit(f'找不到 OAuth client_secret.json，請放到: {CLIENT_SECRET_PATH}')
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    auth_url, _ = flow.authorization_url(prompt='consent')
    print('請在本機瀏覽器開啟以下 URL，完成授權後會取得 code:')
    print(auth_url)


def finish_with_code(code: str):
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise SystemExit(f'找不到 OAuth client_secret.json，請放到: {CLIENT_SECRET_PATH}')
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    try:
        creds = flow.fetch_token(code=code)
    except Exception as e:
        raise SystemExit(f'用 code 換 token 失敗: {e}')
    # InstalledAppFlow.fetch_token returns a dict; construct Credentials
    creds_obj = Credentials.from_authorized_user_info(creds, SCOPES)
    with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
        f.write(creds_obj.to_json())
    print('授權完成，token 已儲存至', TOKEN_PATH)


def load_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
                f.write(creds.to_json())
        except Exception as e:
            print('刷新 token 失敗，需重新授權:', e)
            creds = None
    return creds


def build_service(creds):
    return build('calendar', 'v3', credentials=creds)


def cmd_list(args):
    creds = load_credentials()
    if not creds:
        raise SystemExit('未授權，請先執行: python oauth_cli.py authorize')
    service = build_service(creds)
    time_min = args.time_min or datetime.utcnow().isoformat() + 'Z'
    time_max = args.time_max or (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
    resp = service.events().list(calendarId=args.calendar, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
    items = resp.get('items', [])
    print(json.dumps(items, ensure_ascii=False, indent=2))


def cmd_create(args):
    creds = load_credentials()
    if not creds:
        raise SystemExit('未授權，請先執行: python oauth_cli.py authorize')
    service = build_service(creds)
    if not args.start or not args.end or not args.summary:
        raise SystemExit('請提供 --start --end --summary')
    event = {
        'summary': args.summary,
        'description': args.description or '',
        'start': {'dateTime': args.start, 'timeZone': args.timezone},
        'end': {'dateTime': args.end, 'timeZone': args.timezone},
    }
    if args.location:
        event['location'] = args.location
    if args.attendees:
        event['attendees'] = [{'email': e.strip()} for e in args.attendees.split(',') if e.strip()]
    # sendUpdates='all' will send invitations/updates to attendees
    created = service.events().insert(calendarId=args.calendar, body=event, sendUpdates='all').execute()
    print(json.dumps(created, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(prog='oauth_cli')
    sub = p.add_subparsers(dest='cmd')

    a = sub.add_parser('authorize')
    a.set_defaults(func=lambda args: authorize())

    au = sub.add_parser('auth_url')
    au.set_defaults(func=lambda args: print_auth_url())

    f = sub.add_parser('finish')
    f.add_argument('--code', required=True)
    f.set_defaults(func=lambda args: finish_with_code(args.code))

    l = sub.add_parser('list')
    l.add_argument('--calendar', default='primary')
    l.add_argument('--time-min')
    l.add_argument('--time-max')
    l.set_defaults(func=cmd_list)

    c = sub.add_parser('create')
    c.add_argument('--calendar', default='primary')
    c.add_argument('--start', required=True)
    c.add_argument('--end', required=True)
    c.add_argument('--summary', required=True)
    c.add_argument('--description')
    c.add_argument('--attendees')
    c.add_argument('--location')
    c.add_argument('--timezone', default='Asia/Taipei')
    c.set_defaults(func=cmd_create)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    try:
        args.func(args)
    except Exception as e:
        raise SystemExit(f'錯誤: {e}')

if __name__ == '__main__':
    main()
