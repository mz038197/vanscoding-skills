#Requires -Version 5.1
<#
.SYNOPSIS
  透過 Codex 內建 imagegen 生圖，並寫入專案指定路徑。

.DESCRIPTION
  薄包裝腳本：呼叫 `codex exec` + `$imagegen`（載入官方 ~/.codex/skills/.system/imagegen/）。
  使用 Codex login 訂閱額度；不呼叫 image_gen.py Platform API。

  內建 image_gen 無 destination 參數，預設先存 ~/.codex/generated_images/。
  exec 結束後交檔順序：
  1. 目標路徑本次新寫入且 >= 100KB
  2. 從 ~/.codex/sessions/.../*.jsonl 解 image_generation_call.result（base64）
  3. 從 generated_images/{sessionId}/ 複製本次 session 新檔
  拒絕修改時間過舊的 cache 複製。

.PARAMETER ImagePrompt
  與 -PromptFile 二擇一。圖片需求（可用位置參數 0）。

.PARAMETER PromptFile
  與 -ImagePrompt 二擇一。UTF-8 prompt 檔（建議無 BOM）；中文優先。

.PARAMETER OutputPath
  相對 -Cwd 的輸出路徑；預設 assets/generated/image.png。

.PARAMETER Cwd
  專案根目錄（Codex --cd）；預設目前目錄。

.PARAMETER AspectRatio
  如 16:9、1:1。

.PARAMETER Style
  風格關鍵字，附加於 prompt。

.PARAMETER StyleFile
  UTF-8 風格檔內容（長 style guide 優先於 -Style）。

.PARAMETER DryRun
  只印將送出的 prompt，不呼叫 codex。

.NOTES
  詳見同目錄上層 SKILL.md。互動式單張可改用 Codex Desktop + 官方 skill。
#>
param(
    [string] $ImagePrompt,
    [string] $PromptFile = "",
    [string] $OutputPath = "assets/generated/image.png",
    [string] $Cwd = "",
    [string] $AspectRatio = "",
    [string] $Style = "",
    [string] $StyleFile = "",
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $utf8NoBom
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom

if ([string]::IsNullOrWhiteSpace($ImagePrompt) -and [string]::IsNullOrWhiteSpace($PromptFile)) {
    throw "ImagePrompt or PromptFile is required. Prefer -PromptFile for Chinese prompts."
}

if ([string]::IsNullOrWhiteSpace($Cwd)) {
    $Cwd = (Get-Location).Path
}

function Normalize-Separators([string] $Path) {
    return ($Path -replace '\\', '/')
}

function Resolve-ProjectPath {
    param(
        [string] $Base,
        [string] $PathOrRelative
    )
    if ([System.IO.Path]::IsPathRooted($PathOrRelative)) {
        return [System.IO.Path]::GetFullPath($PathOrRelative)
    }
    return (Join-Path -Path $Base -ChildPath $PathOrRelative)
}

function Assert-PathInBase {
    param(
        [string] $Base,
        [string] $Target
    )
    $baseFull = [IO.Path]::GetFullPath($Base).TrimEnd([char[]]@('\', '/')) + [IO.Path]::DirectorySeparatorChar
    $targetFull = [IO.Path]::GetFullPath($Target)
    if (-not $targetFull.StartsWith($baseFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "OutputPath must be inside Cwd. Cwd: $Base Output: $Target"
    }
}

function Get-RelativePathFromBase {
    param(
        [string] $Base,
        [string] $Target
    )
    $baseFull = [IO.Path]::GetFullPath($Base).TrimEnd([char[]]@('\', '/'))
    $targetFull = [IO.Path]::GetFullPath($Target)
    $sep = [IO.Path]::DirectorySeparatorChar
    foreach ($p in @("$baseFull$sep", "$baseFull/")) {
        if ($targetFull.StartsWith($p, [StringComparison]::OrdinalIgnoreCase)) {
            return $targetFull.Substring($p.Length)
        }
    }
    return [IO.Path]::GetFileName($targetFull)
}

function Test-FreshOutput {
    param(
        [string] $Path,
        [datetime] $NotBefore,
        [int] $MinBytes = 100000
    )
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    $item = Get-Item -LiteralPath $Path
    if ($item.LastWriteTime -lt $NotBefore.AddSeconds(-5)) { return $false }
    if ($item.Length -lt $MinBytes) { return $false }
    return $true
}

function Assert-CodexAvailable {
    $cmd = Get-Command -Name 'codex' -ErrorAction SilentlyContinue
    if (-not $cmd) {
        throw @'
Codex CLI not found. Install and log in:
  npm install -g @openai/codex
  codex --version
  codex login
'@
    }
}

function Get-CodexSessionIdFromOutput {
    param([string] $Text)
    if ($Text -match 'session id:\s*(\S+)') {
        return $Matches[1].Trim()
    }
    return $null
}

function Find-CodexSessionLog {
    param([string] $SessionId)
    if ([string]::IsNullOrWhiteSpace($SessionId)) { return $null }
    $root = Join-Path $env:USERPROFILE '.codex\sessions'
    if (-not (Test-Path -LiteralPath $root)) { return $null }
    return Get-ChildItem -LiteralPath $root -Recurse -Filter "*$SessionId*.jsonl" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

function Get-ImageBase64FromSessionLog {
    param([string] $SessionLogPath)
    if (-not (Test-Path -LiteralPath $SessionLogPath)) { return $null }
    $lastB64 = $null
    foreach ($line in [System.IO.File]::ReadLines($SessionLogPath)) {
        if ($line -notmatch 'image_generation_call') { continue }
        try {
            $obj = $line | ConvertFrom-Json
            $payload = $obj.payload
            if ($null -eq $payload) { continue }
            if ($payload.type -ne 'image_generation_call') { continue }
            if (-not [string]::IsNullOrWhiteSpace($payload.result)) {
                $lastB64 = $payload.result
            }
        } catch {
            continue
        }
    }
    return $lastB64
}

function Write-PngFromSessionLog {
    param(
        [string] $SessionLogPath,
        [string] $Destination
    )
    $b64 = Get-ImageBase64FromSessionLog -SessionLogPath $SessionLogPath
    if ([string]::IsNullOrWhiteSpace($b64)) { return $false }
    $bytes = [Convert]::FromBase64String($b64)
    if ($bytes.Length -lt 8 -or $bytes[0] -ne 0x89 -or $bytes[1] -ne 0x50) {
        throw "Session log image payload is not a valid PNG."
    }
    [System.IO.File]::WriteAllBytes($Destination, $bytes)
    return $true
}

function Try-RecoverFreshGeneratedImage {
    param(
        [string] $Destination,
        [datetime] $NotBefore,
        [string] $SessionId = "",
        [object] $BeforeLatest = $null
    )
    $genRoot = Join-Path $env:USERPROFILE '.codex\generated_images'
    if (-not (Test-Path -LiteralPath $genRoot)) { return $false }

    $searchRoots = @()
    if ($SessionId) {
        $sessionDir = Join-Path $genRoot $SessionId
        if (Test-Path -LiteralPath $sessionDir) {
            $searchRoots += $sessionDir
        }
    }
    $searchRoots += $genRoot

    foreach ($root in $searchRoots) {
        $candidates = Get-ChildItem -LiteralPath $root -Recurse -Filter '*.png' -ErrorAction SilentlyContinue |
            Where-Object {
                $_.LastWriteTime -ge $NotBefore.AddSeconds(-30) -and
                (-not $BeforeLatest -or $_.FullName -ne $BeforeLatest.FullName -or $_.LastWriteTime -gt $BeforeLatest.LastWriteTime)
            } |
            Sort-Object LastWriteTime -Descending
        $fresh = $candidates | Select-Object -First 1
        if ($fresh) {
            Copy-Item -LiteralPath $fresh.FullName -Destination $Destination -Force
            if (Test-FreshOutput -Path $Destination -NotBefore $NotBefore) {
                return $true
            }
            Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
        }
    }
    return $false
}

if (-not (Test-Path -LiteralPath $Cwd)) {
    throw "Working directory not found: $Cwd"
}
$CwdResolved = (Resolve-Path -LiteralPath $Cwd).Path
Assert-CodexAvailable

$fullOut = Resolve-ProjectPath -Base $CwdResolved -PathOrRelative $OutputPath
Assert-PathInBase -Base $CwdResolved -Target $fullOut
$outDir = [System.IO.Path]::GetDirectoryName($fullOut)
if (-not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

$relForPrompt = Normalize-Separators (Get-RelativePathFromBase -Base $CwdResolved -Target $fullOut)

$promptText = $ImagePrompt
if (-not [string]::IsNullOrWhiteSpace($PromptFile)) {
    if (-not (Test-Path -LiteralPath $PromptFile)) {
        throw "PromptFile not found: $PromptFile"
    }
    $promptText = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $PromptFile).Path, $utf8NoBom)
}
if ([string]::IsNullOrWhiteSpace($promptText)) {
    throw "Prompt text is empty."
}

$styleText = $Style
if (-not [string]::IsNullOrWhiteSpace($StyleFile)) {
    if (-not (Test-Path -LiteralPath $StyleFile)) {
        throw "StyleFile not found: $StyleFile"
    }
    $fromFile = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $StyleFile).Path, $utf8NoBom).Trim()
    if ([string]::IsNullOrWhiteSpace($styleText)) {
        $styleText = $fromFile
    } else {
        $styleText = ($styleText.Trim() + [Environment]::NewLine + $fromFile).Trim()
    }
}

$parts = New-Object System.Collections.Generic.List[string]
$parts.Add($promptText.Trim())
if ($AspectRatio) {
    $parts.Add(('Aspect ratio: {0}' -f $AspectRatio.Trim()))
}
if ($styleText) {
    $parts.Add(('Style: {0}' -f $styleText.Trim()))
}
$parts.Add(@(
    'Content constraints',
    'The visual MUST match the topic in the prompt exactly.',
    'Use Traditional Chinese for all visible labels and titles when the prompt is in Chinese.',
    'Do NOT depict unrelated topics unless explicitly requested.'
) -join '. ')
$parts.Add(@(
    'Generation rules',
    'Use ONLY the built-in image_gen tool to create a brand-new image.',
    'Save the newly generated image directly to the project path below.',
    'Do NOT copy any pre-existing PNG from disk or from ~/.codex/generated_images.',
    'Do NOT draw or compose the image with Python, PowerShell, or other code.'
) -join '. ')
$parts.Add(('Save the image to {0}' -f $relForPrompt))

$instructionBody = ($parts -join '; ')
$codexPrompt = ([char]36).ToString() + 'imagegen ' + $instructionBody

Write-Host "[codex-imagegen] Cwd: $CwdResolved"
Write-Host "[codex-imagegen] Output: $fullOut"
Write-Host "[codex-imagegen] codex exec + built-in imagegen (Codex login quota)..."

if ($DryRun) {
    Write-Host "[codex-imagegen] Prompt preview:"
    Write-Host $codexPrompt
    Write-Host "[codex-imagegen] Dry run only; no image was generated."
    exit 0
}

if (Test-Path -LiteralPath $fullOut) {
    Remove-Item -LiteralPath $fullOut -Force
}

$runStarted = Get-Date
$genRoot = Join-Path $env:USERPROFILE '.codex\generated_images'
$beforeLatest = $null
if (Test-Path -LiteralPath $genRoot) {
    $beforeLatest = Get-ChildItem -LiteralPath $genRoot -Recurse -Filter '*.png' -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

$tmpPrompt = Join-Path $outDir ('._codex-prompt-' + [guid]::NewGuid().ToString('n') + '.txt')
[System.IO.File]::WriteAllText($tmpPrompt, $codexPrompt, $utf8NoBom)

$codexArgs = @(
    'exec',
    '--sandbox', 'workspace-write',
    '-c', 'service_tier=fast',
    '--cd', $CwdResolved,
    '-'
)
try {
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $codexOutputLines = @(
            Get-Content -LiteralPath $tmpPrompt -Raw -Encoding UTF8 | & codex @codexArgs 2>&1
        )
    } finally {
        $ErrorActionPreference = $prevEap
    }

    foreach ($line in $codexOutputLines) {
        if ($null -eq $line) { continue }
        if ($line -is [System.Management.Automation.ErrorRecord]) {
            Write-Host $line.ToString()
        } else {
            Write-Host $line
        }
    }
    if ($LASTEXITCODE -ne 0) {
        throw ("codex exited with code {0}" -f $LASTEXITCODE)
    }

    $codexOutput = (
        $codexOutputLines | ForEach-Object {
            if ($_ -is [System.Management.Automation.ErrorRecord]) { $_.ToString() } else { "$_" }
        } | Out-String
    )
    $sessionId = Get-CodexSessionIdFromOutput -Text $codexOutput
    if ($sessionId) {
        Write-Host "[codex-imagegen] Session: $sessionId"
    }

    if (Test-FreshOutput -Path $fullOut -NotBefore $runStarted) {
        Write-Host "[codex-imagegen] Done: $fullOut ($((Get-Item -LiteralPath $fullOut).Length) bytes)"
        exit 0
    }

    if (Test-Path -LiteralPath $fullOut) {
        Remove-Item -LiteralPath $fullOut -Force
    }

    $sessionLog = $null
    if ($sessionId) {
        for ($i = 0; $i -lt 15 -and -not $sessionLog; $i++) {
            $sessionLog = Find-CodexSessionLog -SessionId $sessionId
            if (-not $sessionLog) {
                Start-Sleep -Seconds 1
            }
        }
    }

    if ($sessionLog) {
        Write-Host "[codex-imagegen] Recovering PNG from session log: $($sessionLog.FullName)"
        if (Write-PngFromSessionLog -SessionLogPath $sessionLog.FullName -Destination $fullOut) {
            if (Test-FreshOutput -Path $fullOut -NotBefore $runStarted) {
                Write-Host "[codex-imagegen] Done (from session log): $fullOut ($((Get-Item -LiteralPath $fullOut).Length) bytes)"
                exit 0
            }
            Remove-Item -LiteralPath $fullOut -Force -ErrorAction SilentlyContinue
        }
    }

    if (Try-RecoverFreshGeneratedImage -Destination $fullOut -NotBefore $runStarted -SessionId $sessionId -BeforeLatest $beforeLatest) {
        Write-Host "[codex-imagegen] Done (from generated_images): $fullOut ($((Get-Item -LiteralPath $fullOut).Length) bytes)"
        exit 0
    }

    throw @"
Output missing or stale after codex exec.
Expected a fresh PNG at: $fullOut
Built-in imagegen ran, but the agent did not save the PNG correctly.
Session log recovery also failed.
Try: codex login, then re-run.
"@
}
finally {
    Remove-Item -LiteralPath $tmpPrompt -Force -ErrorAction SilentlyContinue
}
