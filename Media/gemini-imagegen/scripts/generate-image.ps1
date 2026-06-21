#Requires -Version 5.1
<#
.SYNOPSIS
  Generate an image with Google Gemini CLI (headless) and save it under the project tree.

.DESCRIPTION
  Runs `gemini -p` from the workspace root (-Cwd) with --skip-trust and --approval-mode so tool calls can complete non-interactively.
  Do not pass both -y and --approval-mode to gemini (CLI rejects that combination).

.PARAMETER ImagePrompt
  Required unless -PromptFile is set. What to draw. Also accepts positional argument 0.

.PARAMETER PromptFile
  Optional. UTF-8 text file containing the prompt. Prefer this for Chinese prompts.

.PARAMETER OutputPath
  Optional. Path relative to -Cwd; default assets/generated/image.png.

.PARAMETER Cwd
  Optional. Project root (Gemini workspace); defaults to current directory.

.PARAMETER AspectRatio
  Optional. e.g. 16:9, 1:1; included in the prompt.

.PARAMETER Style
  Optional. Style keywords; included in the prompt.

.PARAMETER Model
  Strongly recommended: image-capable / native image Gemini model id for your account (see Google model docs). Passed to gemini -m/--model when non-empty.

.PARAMETER ApprovalMode
  Optional. default yolo. Values: default | auto_edit | yolo | plan

.PARAMETER DryRun
  If set, print prompt and arguments without running gemini.
#>
param(
    [string] $ImagePrompt,
    [string] $PromptFile = "",
    [string] $OutputPath = "assets/generated/image.png",
    [string] $Cwd = "",
    [string] $AspectRatio = "",
    [string] $Style = "",
    [string] $Model = "",
    [ValidateSet("default", "auto_edit", "yolo", "plan")]
    [string] $ApprovalMode = "yolo",
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

function Test-GeminiAvailable {
    $cmd = Get-Command -Name 'gemini' -ErrorAction SilentlyContinue
    if (-not $cmd) {
        throw @'
Gemini CLI not found. Install and authenticate:
  npm install -g @google/gemini-cli
  gemini --version
See: https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html
'@
    }
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

Test-GeminiAvailable

if (-not (Test-Path -LiteralPath $Cwd)) {
    throw "Working directory not found: $Cwd"
}
$CwdResolved = (Resolve-Path -LiteralPath $Cwd).Path

$fullOut = Resolve-ProjectPath -Base $CwdResolved -PathOrRelative $OutputPath
Assert-PathInBase -Base $CwdResolved -Target $fullOut
$outDir = [System.IO.Path]::GetDirectoryName($fullOut)
if (-not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

$relForPrompt = Get-RelativePathFromBase -Base $CwdResolved -Target $fullOut
$relForPrompt = Normalize-Separators $relForPrompt

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

$parts = New-Object System.Collections.Generic.List[string]
$parts.Add('[gemini-imagegen] Single task: output exactly one raster image file at the path below.')
$parts.Add('HARD RULE — what counts as image generation here: pixels must come from (A) native Gemini / Google image model output (IMAGE modality or equivalent returned in-session) that you persist as PNG or JPEG, OR (B) an official first-party image-generation MCP tool already configured (e.g. Imagen), saving that tool''s image output.')
$parts.Add('FORBIDDEN: creating the artwork by writing or running procedural graphics code or raster tools — including Python+Pillow/PIL/matplotlib/cairo/skimage, Node canvas, ImageMagick/GraphicsMagick/gmagick CLI to compose or draw, hand-made minimal/placeholder PNGs, or using SVG render pipelines as the creative image source. A tiny decoder that only writes bytes already produced by (A) or (B) is OK.')
$parts.Add('Do not add unrelated files (no philosophy.md, design notes, or extra docs). Only create/update the single image file unless an MCP strictly requires a temp artifact in-workspace.')
$parts.Add(('Image description: {0}' -f $promptText.Trim()))
if ($AspectRatio) {
    $parts.Add(('Target aspect ratio: {0}' -f $AspectRatio.Trim()))
}
if ($Style) {
    $parts.Add(('Style: {0}' -f $Style.Trim()))
}
$parts.Add(('Save the image exactly at this relative path (forward slashes ok): {0}' -f $relForPrompt))
$parts.Add('Do not ask questions; finish in this non-interactive run.')

$geminiPrompt = ($parts -join ' ')

if ([string]::IsNullOrWhiteSpace($Model)) {
    Write-Warning '[gemini-imagegen] -Model is empty. Default CLI model often cannot emit native images; the agent may try forbidden procedural drawing. Prefer -Model with a native image id from Google docs, e.g. gemini-2.5-flash-image, gemini-3.1-flash-image-preview, or gemini-3-pro-image-preview (404 means your key/project lacks access, not necessarily a typo).'
}

Write-Host "[gemini-imagegen] Cwd: $CwdResolved"
Write-Host "[gemini-imagegen] Output: $fullOut"

$geminiArgs = [System.Collections.Generic.List[string]]::new()
if (-not [string]::IsNullOrWhiteSpace($Model)) {
    $geminiArgs.Add('-m')
    $geminiArgs.Add($Model.Trim())
}
$geminiArgs.Add('-p')
$geminiArgs.Add($geminiPrompt)
$geminiArgs.Add('--skip-trust')
$geminiArgs.Add('--approval-mode')
$geminiArgs.Add($ApprovalMode)

if ($DryRun) {
    Write-Host "[gemini-imagegen] Dry run — gemini arguments:"
    Write-Host ($geminiArgs -join ' ')
    Write-Host "[gemini-imagegen] Prompt length: $($geminiPrompt.Length) chars"
    Write-Host "[gemini-imagegen] Dry run only; gemini was not executed."
    exit 0
}

Write-Host "[gemini-imagegen] Running gemini (headless)..."

$beforeExists = Test-Path -LiteralPath $fullOut
$beforeWriteTimeUtc = $null
$beforeLength = $null
if ($beforeExists) {
    $beforeItem = Get-Item -LiteralPath $fullOut
    $beforeWriteTimeUtc = $beforeItem.LastWriteTimeUtc
    $beforeLength = $beforeItem.Length
}

Push-Location -LiteralPath $CwdResolved
try {
    & gemini @geminiArgs
    $exit = $LASTEXITCODE
}
finally {
    Pop-Location
}

if ($exit -ne 0) {
    throw ('gemini exited with code {0}. Check auth, model name (-Model), and CLI output.' -f $exit)
}

if (-not (Test-Path -LiteralPath $fullOut)) {
    Write-Warning ("gemini finished but output file is missing: {0}. Check the prompt path or try again." -f $fullOut)
    exit 2
}

$afterItem = Get-Item -LiteralPath $fullOut
if ($beforeExists -and $afterItem.LastWriteTimeUtc -le $beforeWriteTimeUtc -and $afterItem.Length -eq $beforeLength) {
    Write-Warning ("gemini finished but output file was not updated: {0}. Try a new OutputPath or inspect gemini output." -f $fullOut)
    exit 3
}

Write-Host "[gemini-imagegen] Done: $fullOut"
exit 0
