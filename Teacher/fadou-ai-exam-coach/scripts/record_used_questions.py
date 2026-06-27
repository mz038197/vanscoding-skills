#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Record used bank IDs into mock-exam/.fadou-exam-used.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

POOL_PREFIX = {"1": "ethics", "2": "python", "3": "theory", "4": "tech"}


def slug_scope(scope: str) -> str:
    s = scope.strip().replace(" ", "").replace("　", "")
    s = s.replace("/", "-").replace("：", "-").replace(":", "-")
    return f"drill:{s}"


def load_history(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"version": 1, "pools": {}, "sessions": [], "updated_at": None}


def save_history(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def pool_for_id(bank_id: str) -> str:
    m = re.match(r"^(\d)-", bank_id)
    if not m:
        return "unknown"
    return POOL_PREFIX.get(m.group(1), "unknown")


def merge_ids(history: dict, mode: str, scope: str | None, bank_ids: list[str]) -> None:
    pools = history.setdefault("pools", {})
    if mode == "drill" and scope:
        key = slug_scope(scope)
        entry = pools.setdefault(key, {"used": [], "last_reset": None})
        entry["used"] = sorted(set(entry["used"]) | set(bank_ids))
    else:
        by_pool: dict[str, list[str]] = {}
        for bid in bank_ids:
            p = pool_for_id(bid)
            by_pool.setdefault(p, []).append(bid)
        for p, ids in by_pool.items():
            if p == "unknown":
                continue
            entry = pools.setdefault(p, {"used": [], "last_reset": None})
            entry["used"] = sorted(set(entry["used"]) | set(ids))

    history.setdefault("sessions", []).append(
        {
            "at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "mode": mode,
            "scope": scope,
            "bankIds": bank_ids,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Record fadou used bank IDs")
    parser.add_argument("questions", type=Path, nargs="?", help="questions.json with _meta.bankIds")
    parser.add_argument("--history", type=Path, default=Path("mock-exam/.fadou-exam-used.json"))
    parser.add_argument("--bank-ids", type=str, default="", help="Comma-separated IDs (drill)")
    parser.add_argument("--mode", choices=("mock", "drill"), default="mock")
    parser.add_argument("--scope", type=str, default="")
    args = parser.parse_args()

    bank_ids: list[str] = []
    mode = args.mode
    scope: str | None = args.scope or None

    if args.questions and args.questions.is_file():
        data = json.loads(args.questions.read_text(encoding="utf-8"))
        meta = data.get("_meta") or {}
        bank_ids = meta.get("bankIds") or []
        mode = meta.get("mode") or mode
        scope = meta.get("scope") or scope
    elif args.bank_ids.strip():
        bank_ids = [x.strip() for x in args.bank_ids.split(",") if x.strip()]
    else:
        print("ERROR: provide questions.json with _meta.bankIds or --bank-ids", file=sys.stderr)
        return 1

    if not bank_ids:
        print("ERROR: empty bankIds", file=sys.stderr)
        return 1

    history = load_history(args.history)
    merge_ids(history, mode, scope, bank_ids)
    save_history(args.history, history)
    print(f"OK: recorded {len(bank_ids)} ids -> {args.history}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
