#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Readmoo 網頁閱讀器：階段一 — 僅擷取 viewport 截圖並寫入 manifest.json。

本檔與 Cursor skill「readmoo-capture」同捆，路徑為：
  ~/.cursor/skills/readmoo-capture/scripts/readmoo_capture_snapshots.py
執行時請在已 `uv sync` 且含 playwright 的專案根目錄（例如 datascience）使用
`uv run` ＋ 本檔絕對路徑（見同目錄上層之 SKILL.md）。

前置：依 wiki《Readmoo-網頁版匯出-Playwright流程》以 playwright-cli 登入並
     state-save readmoo-auth.json，且先手動翻到要當起點的第一頁再存 state。

階段二、三請使用 readmoo_ocr_pages.py、readmoo_assemble_markdown.py。
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Page, sync_playwright


def _book_id_from_url(url: str) -> str:
    parts = urlparse(url).path.strip("/").split("/")
    if parts and parts[-1].isdigit():
        return parts[-1]
    return "unknown"


def _default_out_root() -> Path:
    """未指定 --out-dir 時，為目前工作目錄下的 readmoo_exports（Cursor 終端通常即 workspace 根）。"""
    return Path.cwd() / "readmoo_exports"


def _md5(data: bytes) -> str:
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


def _viewport_visual_fingerprint(png_bytes: bytes, *, side: int = 48) -> str:
    try:
        from PIL import Image

        im = Image.open(io.BytesIO(png_bytes)).convert("L")
        im = im.resize((side, side), Image.Resampling.LANCZOS)
        return hashlib.md5(im.tobytes(), usedforsecurity=False).hexdigest()
    except Exception:
        return _md5(png_bytes)


def dismiss_readmoo_modal_overlays(
    page: Page,
    *,
    settle_ms: int = 450,
    max_rounds: int = 10,
) -> None:
    preferred_buttons = (
        "取消",
        "稍後再說",
        "稍後",
        "關閉",
        "我知道了",
        "略過",
        "不要同步",
        "Not now",
        "Cancel",
        "Close",
    )

    def click_visible_button(name: str, *, exact: bool) -> bool:
        try:
            loc = page.get_by_role("button", name=name, exact=exact)
            n = loc.count()
            for i in range(min(n, 8)):
                btn = loc.nth(i)
                if btn.is_visible(timeout=500):
                    btn.click(timeout=15_000)
                    page.wait_for_timeout(settle_ms)
                    return True
        except Exception:
            pass
        return False

    for _ in range(max_rounds):
        clicked = False
        for label in preferred_buttons:
            if click_visible_button(label, exact=True):
                clicked = True
                break
        if clicked:
            continue

        try:
            cancel_any = page.get_by_role("button", name="取消", exact=True)
            cancel_visible = False
            for i in range(min(cancel_any.count(), 4)):
                if cancel_any.nth(i).is_visible(timeout=200):
                    cancel_visible = True
                    break
            if not cancel_visible:
                ok = page.get_by_role("button", name="確定", exact=True)
                for i in range(min(ok.count(), 4)):
                    if ok.nth(i).is_visible(timeout=400):
                        ok.nth(i).click(timeout=15_000)
                        page.wait_for_timeout(settle_ms)
                        clicked = True
                        break
        except Exception:
            pass
        if clicked:
            continue

        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(280)
        except Exception:
            pass
        break


def _pick_text_root_js() -> str:
    return """
    () => {
      const candidates = [
        '[class*="reading"]', '[class*="Reading"]',
        '[class*="reader"]', '[class*="Reader"]',
        '[class*="content"]', '[class*="textLayer"]',
        'article', '[role="main"]', 'main',
      ];
      for (const sel of candidates) {
        const el = document.querySelector(sel);
        if (el) {
          const t = (el.innerText || '').trim();
          if (t.length > 40) return t;
        }
      }
      return (document.body && document.body.innerText || '').trim();
    }
    """


def _first_meaningful_line(text: str) -> str:
    for line in text.splitlines():
        t = line.strip()
        if t:
            return t
    return ""


def _viewport_png_after_dismissing(page: Page) -> bytes:
    """先關閱讀器浮層／對話框再截 viewport；存檔與末頁指紋比對皆走此路徑。"""
    dismiss_readmoo_modal_overlays(page)
    return page.screenshot(full_page=False, type="png")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Readmoo 階段一：逐頁 viewport 截圖 + manifest.json",
    )
    parser.add_argument("--storage-state", required=True, help="playwright-cli state-save 產生的 json")
    parser.add_argument("--url", required=True, help="閱讀器網址（含書籍 ID）")
    parser.add_argument(
        "--out-dir",
        default=None,
        help="輸出根目錄；預設為目前工作目錄下的 readmoo_exports/（建議在 workspace 根執行）",
    )
    parser.add_argument("--headless", action="store_true", help="無頭模式")
    parser.add_argument("--pause-ms", type=int, default=900, help="每步驟等待毫秒")
    parser.add_argument(
        "--same-streak",
        type=int,
        default=1,
        help="連續翻頁後畫面指紋相同達此值則視為末頁",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=8000,
        help="最多擷取幾張截圖",
    )
    args = parser.parse_args()

    storage = Path(args.storage_state)
    if not storage.is_file():
        print(f"找不到 storage state：{storage}", file=sys.stderr)
        return 1

    book_id = _book_id_from_url(args.url)
    out_root = Path(args.out_dir) if args.out_dir else _default_out_root()
    book_dir = out_root / f"readmoo_{book_id}"
    assets_dir = book_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    run_started = datetime.now(timezone.utc).isoformat()
    pages_manifest: list[dict] = []
    stop_reason: str | None = None
    snapshot_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(storage_state=str(storage))
        page = context.new_page()
        page.set_viewport_size({"width": 1280, "height": 900})

        page.goto(args.url, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2500)

        if "signin" in page.url.lower():
            print(
                "目前網址仍為登入頁。請依 wiki 用 playwright-cli 登入後再 state-save。",
                file=sys.stderr,
            )
            browser.close()
            return 2

        dismiss_readmoo_modal_overlays(page)

        same_streak = 0
        page_seq = 0

        while page_seq < args.max_pages:
            page.wait_for_timeout(args.pause_ms)
            before_png = _viewport_png_after_dismissing(page)
            before_fp = _viewport_visual_fingerprint(before_png)

            text = page.evaluate(_pick_text_root_js())
            first_line = _first_meaningful_line(text)

            page_seq += 1
            snapshot_count += 1
            fname = f"p{page_seq:05d}.png"
            rel_image = f"assets/{fname}"
            (assets_dir / fname).write_bytes(before_png)
            cap_at = datetime.now(timezone.utc).isoformat()
            pages_manifest.append(
                {
                    "index": page_seq,
                    "image_path": rel_image,
                    "fingerprint": before_fp,
                    "file_md5": _md5(before_png),
                    "captured_at": cap_at,
                    "dom_heading_hint": (first_line[:200] if first_line else None),
                }
            )

            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(max(200, args.pause_ms // 2))
            after_png = _viewport_png_after_dismissing(page)
            after_fp = _viewport_visual_fingerprint(after_png)

            if after_fp == before_fp:
                same_streak += 1
                if same_streak >= args.same_streak:
                    stop_reason = "連續多次翻頁畫面未變，視為已到末頁。"
                    break
            else:
                same_streak = 0

        browser.close()

    if snapshot_count == args.max_pages and stop_reason is None:
        stop_reason = f"已達 --max-pages {args.max_pages}。"

    run_finished = datetime.now(timezone.utc).isoformat()
    manifest = {
        "book_id": book_id,
        "source_url": args.url,
        "captured_at": run_started,
        "finished_at": run_finished,
        "start_mode": "manual-first-page",
        "stop_reason": stop_reason,
        "max_pages_arg": args.max_pages,
        "snapshot_count": snapshot_count,
        "capture_script": "readmoo-capture/scripts/readmoo_capture_snapshots.py",
        "pages": pages_manifest,
    }
    manifest_path = book_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    log_lines = [
        "readmoo-capture/scripts/readmoo_capture_snapshots.py（階段一）",
        f"book_id={book_id}",
        f"started={run_started}",
        f"finished={run_finished}",
        f"snapshot_count={snapshot_count}",
        f"manifest={manifest_path}",
        f"stop_reason={stop_reason!r}",
    ]
    (book_dir / "run.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(
        f"完成：共擷取 {snapshot_count} 張 snapshot，輸出於 {book_dir}（manifest.json、run.log）"
    )
    if stop_reason:
        print(stop_reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
