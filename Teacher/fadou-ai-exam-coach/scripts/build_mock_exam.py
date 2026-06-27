#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build mock exam HTML from questions.json and optionally open in browser."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import webbrowser
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets" / "mock-exam"
TEMPLATE = ASSETS / "index.template.html"


def load_questions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    if len(questions) != 50:
        raise ValueError(f"Expected 50 questions, got {len(questions)}")
    for i, q in enumerate(questions, start=1):
        if q.get("id") != i:
            raise ValueError(f"Question id mismatch at index {i}: {q.get('id')}")
        ans = (q.get("answer") or "").lower()
        if ans not in ("a", "b", "c", "d"):
            raise ValueError(f"Question {i}: invalid answer {q.get('answer')!r}")
    return data


def embed_payload(data: dict, session_id: str) -> dict:
    """Strip agent-only _meta; inject sessionId for exam.js."""
    payload = {k: v for k, v in data.items() if k != "_meta"}
    payload["sessionId"] = session_id
    return payload


def build_html(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    json_str = json.dumps(data, ensure_ascii=False)
    json_str = json_str.replace("</", "<\\/")
    return template.replace("__EXAM_DATA__", json_str)


def open_in_browser(html_path: Path) -> bool:
    uri = html_path.resolve().as_uri()
    try:
        if sys.platform == "win32":
            import os

            os.startfile(str(html_path.resolve()))  # noqa: S606
            return True
        return webbrowser.open(uri, new=2)
    except OSError:
        return webbrowser.open(uri, new=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build fadou mock exam HTML")
    parser.add_argument("questions", type=Path, help="Path to questions.json")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open index.html in default browser after build",
    )
    args = parser.parse_args()

    if not TEMPLATE.is_file():
        print(f"Template not found: {TEMPLATE}", file=sys.stderr)
        return 1

    raw = load_questions(args.questions)
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    session_id = out_dir.name

    embed = embed_payload(raw, session_id)
    html = build_html(embed)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    shutil.copy2(ASSETS / "styles.css", out_dir / "styles.css")
    shutil.copy2(ASSETS / "exam.js", out_dir / "exam.js")
    if args.questions.resolve() != (out_dir / "questions.json").resolve():
        shutil.copy2(args.questions, out_dir / "questions.json")

    readme = out_dir / "README.txt"
    readme.write_text(
        "交卷後可在此資料夾保存「錯題檢討.md」（從瀏覽器下載）。\n",
        encoding="utf-8",
    )

    index_path = out_dir / "index.html"
    print(f"Built: {index_path} (sessionId={session_id})")

    if args.open:
        if open_in_browser(index_path):
            print("Opened in browser.")
        else:
            print(f"Could not open browser. Open manually: {index_path.resolve().as_uri()}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
