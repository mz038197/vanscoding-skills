# Forward-sync a skill from repo to Cursor + Codex with .skill-sync.json
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath
)

$ErrorActionPreference = "Stop"
$RepoRoot = git rev-parse --show-toplevel
if (-not $RepoRoot) { throw "Not in a git repository." }

$Src = Join-Path $RepoRoot ($SourcePath -replace '/', '\')
if (-not (Test-Path (Join-Path $Src "SKILL.md"))) {
    throw "SKILL.md not found under $Src"
}

$parts = $SourcePath -split '/'
if ($parts.Length -lt 2) { throw "SourcePath must include Category/skill, got: $SourcePath" }
$Relative = ($parts[1..($parts.Length - 1)] -join '/')
$Leaf = $parts[-1]

$Commit = git -C $RepoRoot rev-parse HEAD
$Version = $null
$SkillMd = Join-Path $Src "SKILL.md"
$content = Get-Content $SkillMd -Raw
if ($content -match '(?m)^version:\s*"?([^"\r\n]+)"?') {
    $Version = $Matches[1].Trim()
}

$Meta = @{
    skill         = $Leaf
    version       = $Version
    source_repo   = "vanscoding-skills"
    source_path   = $SourcePath.Replace('\', '/')
    source_commit = $Commit.Trim()
    synced_at     = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
} | ConvertTo-Json

foreach ($Agent in @(".cursor", ".codex")) {
    $Dst = Join-Path $env:USERPROFILE "$Agent\skills\$($Relative -replace '/', '\')"
    if (Test-Path $Dst) { Remove-Item -Recurse -Force $Dst }
    $Parent = Split-Path $Dst -Parent
    if (-not (Test-Path $Parent)) { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
    Copy-Item -Recurse -Force $Src $Dst
    Set-Content -Path (Join-Path $Dst ".skill-sync.json") -Value $Meta -Encoding utf8
    Write-Host "Synced -> $Dst"
}
