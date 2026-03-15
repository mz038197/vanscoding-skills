"""
Google Sheets CLI for nanobot skills

用法範例:
  python cli.py --sheet-id SHEETID write --range A1 --value Hello
  python cli.py read --range A1:C3
  python cli.py append --row "val1,val2,val3"
  python cli.py clear --range A1

環境變數:
  GOOGLE_APPLICATION_CREDENTIALS - path to service account json (預設: workspace/credentials.json)
  SHEET_ID - default spreadsheet id
"""
import os
import argparse
import json
from typing import List

try:
    from google.oauth2.service_account import Credentials
    import gspread
except Exception as e:
    raise SystemExit('請先安裝相依套件: pip install gspread google-auth')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']

DEFAULT_CREDS = os.path.join(os.path.expanduser('~'), '.nanobot', 'workspace', 'credentials.json')
# If running inside this workspace, also accept relative path
WORKSPACE_CREDS = os.path.join(os.getcwd(), 'credentials.json')


def get_creds(path: str = None):
    path = path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or DEFAULT_CREDS
    if not os.path.exists(path) and os.path.exists(WORKSPACE_CREDS):
        path = WORKSPACE_CREDS
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到 service account 金鑰檔，請設定 GOOGLE_APPLICATION_CREDENTIALS 或放置在 {path}")
    return Credentials.from_service_account_file(path, scopes=SCOPES)


def open_sheet(sheet_id: str, creds_path: str = None):
    creds = get_creds(creds_path)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)


def parse_row(s: str) -> List[str]:
    # 簡單以逗號分隔，保留空白
    return [c for c in [v.strip() for v in s.split(',')]]


def cmd_read(args):
    sh = open_sheet(args.sheet_id, args.creds)
    ws = sh.worksheet(args.worksheet)
    rng = args.range or 'A1:C10'
    vals = ws.get(rng)
    print(json.dumps(vals, ensure_ascii=False, indent=2))


def cmd_write(args):
    sh = open_sheet(args.sheet_id, args.creds)
    ws = sh.worksheet(args.worksheet)
    rng = args.range or 'A1'
    # 支援單一儲存格或多格 list of lists
    if args.value is None:
        raise SystemExit('請提供 --value')
    # 若 value 包含行分隔符，視為多列，否則單一值
    if '\n' in args.value:
        rows = [[c for c in row.split(',')] for row in args.value.split('\n')]
        ws.update(rng, rows)
    else:
        ws.update_acell(rng, args.value)
    print('OK')


def cmd_append(args):
    sh = open_sheet(args.sheet_id, args.creds)
    ws = sh.worksheet(args.worksheet)
    row = parse_row(args.row)
    ws.append_row(row, value_input_option='USER_ENTERED')
    print('OK')


def cmd_clear(args):
    sh = open_sheet(args.sheet_id, args.creds)
    ws = sh.worksheet(args.worksheet)
    rng = args.range or 'A1'
    ws.batch_clear([rng])
    print('OK')


def main():
    p = argparse.ArgumentParser(prog='google-sheets-cli')
    p.add_argument('--creds', help='path to service account json (optional)')
    p.add_argument('--sheet-id', help='Spreadsheet ID (or set SHEET_ID env var)', default=os.getenv('SHEET_ID'))
    p.add_argument('--worksheet', help='工作表名稱 (預設: 工作表1)', default='工作表1')

    sub = p.add_subparsers(dest='cmd')

    r = sub.add_parser('read')
    r.add_argument('--range', help='A1 範圍, e.g. A1:C10')
    r.set_defaults(func=cmd_read)

    w = sub.add_parser('write')
    w.add_argument('--range', help='A1 範圍, e.g. A1')
    w.add_argument('--value', help='要寫入的值 (單一儲存格) 或用逗號分隔/換行表示多列')
    w.set_defaults(func=cmd_write)

    a = sub.add_parser('append')
    a.add_argument('--row', required=True, help='以逗號分隔的列, e.g. "a,b,c"')
    a.set_defaults(func=cmd_append)

    c = sub.add_parser('clear')
    c.add_argument('--range', help='A1 範圍, e.g. A1')
    c.set_defaults(func=cmd_clear)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    if not args.sheet_id:
        raise SystemExit('請指定 --sheet-id 或設定 SHEET_ID 環境變數')
    try:
        args.func(args)
    except Exception as e:
        raise SystemExit(f'執行失敗: {e}')


if __name__ == '__main__':
    main()
