#!/usr/bin/env python3
"""Pre-commit check: skill directory changes require SKILL.md version bump."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

SKILL_CATEGORIES = frozenset(
    {
        "Browser",
        "Developer",
        "Documents",
        "Media",
        "nanobot",
        "Productivity",
        "Search",
        "Teacher",
        "Vision",
    }
)

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git(*args: str) -> str:
    result = _run_git(*args)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def _staged_files() -> list[str]:
    output = _git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return [line.strip() for line in output.splitlines() if line.strip()]


def _skill_path_for_file(repo_root: Path, posix_path: str) -> str | None:
    parts = PurePosixPath(posix_path).parts
    if len(parts) < 2 or parts[0] not in SKILL_CATEGORIES:
        return None

    current = repo_root.joinpath(*parts)
    while current != repo_root / parts[0]:
        if (current / "SKILL.md").is_file():
            return current.relative_to(repo_root).as_posix()
        if current.parent == current:
            break
        current = current.parent
    return None


def _read_skill_md_from_git(spec: str) -> str | None:
    result = _run_git("show", spec)
    if result.returncode != 0:
        return None
    return result.stdout


def _extract_version(content: str) -> str | None:
    if not content.startswith("---"):
        return None
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    frontmatter_text = match.group(1)
    version_match = re.search(
        r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$',
        frontmatter_text,
        re.MULTILINE,
    )
    if version_match:
        return version_match.group(1).strip()
    return None


def _leaf_name(skill_path: str) -> str:
    return PurePosixPath(skill_path).name


def _format_block(
    skill: str,
    skill_path: str,
    skill_md: str,
    current_version: str | None,
    changed_files: list[str],
    message: str,
) -> str:
    lines = [
        message,
        f"skill: {skill}",
        f"skill_path: {skill_path}",
        f"skill_md: {skill_md}",
        f'current_version: "{current_version or ""}"',
        "changed_files:",
    ]
    lines.extend(f"  - {path}" for path in sorted(changed_files))
    lines.append("hint: Bump version in SKILL.md frontmatter, git add, then commit again.")
    return "\n".join(lines)


def main() -> int:
    try:
        repo_root = Path(_git("rev-parse", "--show-toplevel").strip())
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    staged = _staged_files()
    if not staged:
        return 0

    skill_changes: dict[str, list[str]] = {}
    for path in staged:
        skill_path = _skill_path_for_file(repo_root, path.replace("\\", "/"))
        if skill_path is None:
            continue
        skill_changes.setdefault(skill_path, []).append(path.replace("\\", "/"))

    if not skill_changes:
        return 0

    failures: list[str] = []

    for skill_path, changed_files in sorted(skill_changes.items()):
        skill_md = f"{skill_path}/SKILL.md"
        skill = _leaf_name(skill_path)

        staged_content = _read_skill_md_from_git(f":{skill_md}")
        head_content = _read_skill_md_from_git(f"HEAD:{skill_md}")

        if staged_content is None:
            failures.append(
                _format_block(
                    skill,
                    skill_path,
                    skill_md,
                    _extract_version(head_content or ""),
                    changed_files,
                    "SKILL_MD_MISSING_IN_INDEX",
                )
            )
            continue

        staged_version = _extract_version(staged_content)
        head_version = _extract_version(head_content) if head_content else None

        if not staged_version:
            failures.append(
                _format_block(
                    skill,
                    skill_path,
                    skill_md,
                    head_version,
                    changed_files,
                    "SKILL_VERSION_MISSING",
                )
            )
            continue

        if not SEMVER_RE.match(staged_version):
            failures.append(
                _format_block(
                    skill,
                    skill_path,
                    skill_md,
                    staged_version,
                    changed_files,
                    "SKILL_VERSION_INVALID_SEMVER",
                )
            )
            continue

        only_skill_md = set(changed_files) == {skill_md}
        version_changed = staged_version != head_version

        if only_skill_md and version_changed:
            continue

        if not version_changed:
            failures.append(
                _format_block(
                    skill,
                    skill_path,
                    skill_md,
                    head_version or staged_version,
                    changed_files,
                    "SKILL_VERSION_BUMP_REQUIRED",
                )
            )

    if failures:
        print("\n\n".join(failures), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
