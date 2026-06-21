# Install git pre-commit hook for vanscoding-skills
$ErrorActionPreference = "Stop"

$Root = git rev-parse --show-toplevel
if (-not $Root) {
    Write-Error "Not inside a git repository."
}

$HookSrc = Join-Path $Root "scripts/hooks/pre-commit"
$HookDst = Join-Path $Root ".git/hooks/pre-commit"

if (-not (Test-Path $HookSrc)) {
    Write-Error "Missing hook template: $HookSrc"
}

Copy-Item -Force $HookSrc $HookDst
Write-Host "Installed pre-commit hook -> $HookDst"
Write-Host "Run git commit in this repo to enforce SKILL.md version bumps on skill changes."
