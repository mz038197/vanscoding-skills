#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suggest internal bank IDs for mock exam / drill, avoiding used history."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = SKILL_ROOT / "references" / "knowledge"

BANK_FILES = {
    "ethics": "AI倫理與社會影響-考古題-次層面細考點全題庫-上傳版.md",
    "python": "Python基礎運用-考古題-次層面細考點全題庫-上傳版.md",
    "theory": "人工智慧理論知識-考古題-次層面細考點全題庫-上傳版.md",
    "tech": "人工智慧技術運用-考古題-次層面細考點全題庫-上傳版.md",
}

POOL_PREFIX = {"ethics": "1-", "python": "2-", "theory": "3-", "tech": "4-"}
MOCK_COUNTS = {"ethics": 10, "python": 10, "theory": 10, "tech": 20}

EXCLUDED_IDS = frozenset({"2-9"})
BANK_ID_RE = re.compile(r"^\|\s*(\d+-\d+)\s*\|")


def slug_scope(scope: str) -> str:
    s = scope.strip().replace(" ", "").replace("　", "")
    s = s.replace("/", "-").replace("：", "-").replace(":", "-")
    return f"drill:{s}"


def parse_bank_ids(path: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = BANK_ID_RE.match(line.strip())
        if not m:
            continue
        bid = m.group(1)
        if bid in EXCLUDED_IDS or bid in seen:
            continue
        if "待核" in line or "正解待核" in line:
            continue
        seen.add(bid)
        ids.append(bid)
    return ids


def load_pools() -> dict[str, list[str]]:
    pools: dict[str, list[str]] = {}
    for name, filename in BANK_FILES.items():
        path = KNOWLEDGE_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing knowledge file: {path}")
        prefix = POOL_PREFIX[name]
        pools[name] = [i for i in parse_bank_ids(path) if i.startswith(prefix)]
    return pools


def load_history(path: Path) -> dict:
    if not path.is_file():
        return {"version": 1, "pools": {}, "sessions": [], "updated_at": None}
    return json.loads(path.read_text(encoding="utf-8"))


def pool_entry(history: dict, key: str) -> dict:
    pools = history.setdefault("pools", {})
    if key not in pools:
        pools[key] = {"used": [], "last_reset": None}
    return pools[key]


def pick_from_pool(all_ids: list[str], used: list[str], count: int) -> tuple[list[str], bool]:
    used_set = set(used)
    available = [i for i in all_ids if i not in used_set]
    reset = False
    if len(available) < count:
        reset = True
        available = list(all_ids)
        used_set.clear()
    if len(available) < count:
        raise ValueError(f"Pool too small: need {count}, have {len(available)}")
    picked = random.sample(available, count)
    return picked, reset


def suggest_mock(pools: dict[str, list[str]], history: dict) -> dict:
    by_category: dict[str, list[str]] = {}
    pool_resets: list[str] = []
    all_picked: list[str] = []

    for name, count in MOCK_COUNTS.items():
        entry = pool_entry(history, name)
        used = list(entry.get("used") or [])
        picked, reset = pick_from_pool(pools[name], used, count)
        if reset:
            pool_resets.append(name)
        by_category[name] = picked
        all_picked.extend(picked)

    return {
        "bankIds": all_picked,
        "byCategory": by_category,
        "poolResets": pool_resets,
        "mode": "mock",
    }


def suggest_drill(
    pools: dict[str, list[str]], history: dict, scope: str, count: int
) -> dict:
    pool_key = slug_scope(scope)
    entry = pool_entry(history, pool_key)
    used = list(entry.get("used") or [])

    cat = "tech"
    m = re.match(r"^(\d)", scope.strip())
    if m:
        cat_map = {"1": "ethics", "2": "python", "3": "theory", "4": "tech"}
        cat = cat_map.get(m.group(1), "tech")

    picked, reset = pick_from_pool(pools[cat], used, count)

    return {
        "bankIds": picked,
        "byCategory": {cat: picked},
        "poolResets": [pool_key] if reset else [],
        "mode": "drill",
        "scope": scope,
        "poolKey": pool_key,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest bank IDs for fadou mock/drill")
    parser.add_argument("--mode", choices=("mock", "drill"), required=True)
    parser.add_argument("--history", type=Path, default=Path("mock-exam/.fadou-exam-used.json"))
    parser.add_argument("--scope", type=str, default="", help="Drill scope label")
    parser.add_argument("--count", type=int, default=5, help="Drill question count")
    args = parser.parse_args()

    try:
        pools = load_pools()
        history = load_history(args.history)
        if args.mode == "mock":
            result = suggest_mock(pools, history)
        else:
            if not args.scope.strip():
                print("ERROR: --scope required for drill mode", file=sys.stderr)
                return 1
            result = suggest_drill(pools, history, args.scope, args.count)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
