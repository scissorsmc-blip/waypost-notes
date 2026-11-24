<#
.SYNOPSIS
    Calm Slate - Guided Windows Installer (Core Kit & Full Kit)

.DESCRIPTION
    Installs Obsidian and Google Antigravity, creates your PARA + AI Memory vault
    (06_Metadata/Gemini/), registers the vault inside Obsidian, and links all
    rules and skills automatically.

.EXAMPLE
    # Interactive setup (recommended for beginners):
    .\install-windows.ps1

    # Direct Full Kit install into a custom folder:
    .\install-windows.ps1 -Kit full -VaultPath "$env:USERPROFILE\Documents\CalmSlate"
#>

[CmdletBinding()]
param(
    [ValidateSet("", "core", "full")]
    [string]$Kit = "",
    [string]$VaultPath = "",
    [string]$RepoOwner = "scissorsmc-blip",
    [string]$RepoName = "calm-slate",
    [string]$Branch = "main",
    [switch]$SkipAppInstall
)

$ErrorActionPreference = "Stop"

function Write-Header($Text) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Copy-FolderSafe($Source, $Destination) {
    if (-not (Test-Path $Source)) { return }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -Path $Source -Force | ForEach-Object {
        $target = Join-Path $Destination $_.Name
        if ($_.PSIsContainer) {
            Copy-FolderSafe $_.FullName $target
        } else {
            if ($_.Name -eq ".gitkeep") { return }
            if (-not (Test-Path $target)) {
                Copy-Item -Path $_.FullName -Destination $target -Force
            }
        }
    }
}

Write-Header "Calm Slate - Windows Setup"
Write-Host "This installer sets up Obsidian + Google Antigravity with a ready-to-use"
Write-Host "vault and persistent AI memory (06_Metadata\Gemini)."
Write-Host ""

# 1. Choose Core Kit vs Full Kit
if (-not $Kit) {
    Write-Host "Choose which kit to install:" -ForegroundColor Yellow
    Write-Host "  [1] Core Kit (Recommended for Beginners)"
    Write-Host "      - Obsidian + Google Antigravity + Granola meeting auto-sync + PARA vault"
    Write-Host "      - AI memory + 12 everyday skills + Calm Slate dark theme. Zero Python needed."
    Write-Host ""
    Write-Host "  [2] Full Kit (Power-Up Bundle)"
    Write-Host "      - Everything in Core Kit PLUS 12 extended skills and optional add-on scripts"
    Write-Host "        for Calendar (ICS), Granola meetings, Google Tasks, YNAB, and Android Termux."
    Write-Host ""
    $choice = Read-Host "Enter 1 for Core Kit or 2 for Full Kit [Default: 1]"
    if ($choice -eq "2") { $Kit = "full" } else { $Kit = "core" }
}
Write-Host "[+] Selected: $($Kit.ToUpper()) KIT" -ForegroundColor Green

# 2. Pick Vault Folder (prefer OneDrive for automatic backup/sync)
if (-not $VaultPath) {
    $defaultRoot = if ($env:OneDrive -and (Test-Path $env:OneDrive)) {
        Join-Path $env:OneDrive "Obsidian\CalmSlate"
    } else {
        Join-Path $env:USERPROFILE "Documents\CalmSlate"
    }
    Write-Host ""
    Write-Host "Where should your Calm Slate vault folder be created?" -ForegroundColor Yellow
    Write-Host "  Recommended (auto-detected): $defaultRoot"
    $custom = Read-Host "Press Enter to accept recommended location, or paste another path"
    $VaultPath = if ([string]::IsNullOrWhiteSpace($custom)) { $defaultRoot } else { $custom.Trim('"').Trim() }
}
Write-Host "[+] Vault folder: $VaultPath" -ForegroundColor Green

# 3. Install Obsidian & Google Antigravity via winget
if (-not $SkipAppInstall) {
    Write-Header "Step 1 of 4: Installing Obsidian & Google Antigravity"
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "[*] Checking/installing Obsidian..."
        winget install --id Obsidian.Obsidian -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
        Write-Host "[+] Obsidian ready." -ForegroundColor Green

        Write-Host "[*] Checking/installing Google Antigravity..."
        winget install --id Google.Antigravity -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
        Write-Host "[+] Google Antigravity ready." -ForegroundColor Green

        Write-Host "[*] Checking/installing Granola (AI meeting notepad)..."
        try {
            winget install --name "Granola" --accept-source-agreements --accept-package-agreements --silent | Out-Null
            Write-Host "[+] Granola ready." -ForegroundColor Green
        } catch {
            Write-Host "[i] Download free Granola desktop app from: https://www.granola.ai" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[!] Windows Package Manager (winget) was not found on this PC." -ForegroundColor Yellow
        Write-Host "    Please install these free apps manually, then return here:"
        Write-Host "      1. Obsidian:           https://obsidian.md"
        Write-Host "      2. Google Antigravity: https://antigravity.google"
        Write-Host "      3. Granola (meetings): https://www.granola.ai"
        Read-Host "Press Enter once installed (or to continue creating the vault now)"
    }
}

# 4. Locate local repo files or download from GitHub
Write-Header "Step 2 of 4: Preparing Starter Vault Files"
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$localRepoRoot = Split-Path -Parent $scriptDir
$tempRoot = $null

if ((Test-Path (Join-Path $localRepoRoot "core-kit\AGENTS.md"))) {
    $sourceRoot = $localRepoRoot
    Write-Host "[+] Using local Starter Kit files from: $sourceRoot" -ForegroundColor Green
} else {
    if ($RepoOwner -eq "YOUR_GITHUB_USERNAME") {
        throw "RepoOwner is still set to YOUR_GITHUB_USERNAME. Update RepoOwner in install-windows.ps1 or run from an unzipped repo folder."
    }
    $tempRoot = Join-Path $env:TEMP ("calm-slate-kit-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
    $zipPath = Join-Path $tempRoot "kit.zip"
    $zipUrl = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"
    Write-Host "[*] Downloading Starter Kit from $zipUrl ..."
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
    Expand-Archive -Path $zipPath -DestinationPath $tempRoot -Force
    $extracted = Get-ChildItem -Path $tempRoot -Directory | Select-Object -First 1
    $sourceRoot = $extracted.FullName
    Write-Host "[+] Downloaded and unpacked Starter Kit." -ForegroundColor Green
}

# 5. Build Vault (Core Kit + optional Full Kit overlay)
New-Item -ItemType Directory -Force -Path $VaultPath | Out-Null
Copy-FolderSafe (Join-Path $sourceRoot "core-kit") $VaultPath
Write-Host "[+] Installed Core Kit vault structure, templates, dark theme, and 12 core skills." -ForegroundColor Green

if ($Kit -eq "full") {
    Copy-FolderSafe (Join-Path $sourceRoot "full-kit-addons") $VaultPath
    Write-Host "[+] Installed Full Kit add-ons (sync scripts, mobile pack, and 12 extended skills)." -ForegroundColor Green
}

# Mirror all skills into .agents\skills and global Antigravity plugin dir
Write-Header "Step 3 of 4: Linking Vault Rules, Skills & Obsidian"
$vaultSkills = Join-Path $VaultPath "06_Metadata\Gemini\Skills"
$workspaceSkills = Join-Path $VaultPath ".agents\skills"
$workspaceRules = Join-Path $VaultPath ".agents\rules"
$globalPlugin = Join-Path $env:USERPROFILE ".gemini\config\plugins\user-profile"
$globalRules = Join-Path $globalPlugin "rules"
$globalSkills = Join-Path $globalPlugin "skills"

New-Item -ItemType Directory -Force -Path $workspaceSkills, $workspaceRules, $globalRules, $globalSkills | Out-Null
Copy-Item -Path (Join-Path $VaultPath "AGENTS.md") -Destination (Join-Path $workspaceRules "AGENTS.md") -Force
Copy-Item -Path (Join-Path $VaultPath "AGENTS.md") -Destination (Join-Path $globalRules "AGENTS.md") -Force
Copy-Item -Path (Join-Path $vaultSkills "*") -Destination $workspaceSkills -Recurse -Force
Copy-Item -Path (Join-Path $vaultSkills "*") -Destination $globalSkills -Recurse -Force
Write-Host "[+] Linked AGENTS.md and all skills into workspace and Antigravity." -ForegroundColor Green

# Download official Granola Meetings Simple Sync plugin (free Granola MCP sync)
$granolaDir = Join-Path $VaultPath ".obsidian\plugins\granola-meetings-simple-sync"
New-Item -ItemType Directory -Force -Path $granolaDir | Out-Null
$granolaBase = "https://github.com/philfreo/obsidian-granola-plugin/releases/latest/download"
try {
    foreach ($asset in @("manifest.json", "main.js")) {
        Invoke-WebRequest -Uri "$granolaBase/$asset" -OutFile (Join-Path $granolaDir $asset) -UseBasicParsing
    }
    Write-Host "[+] Installed official Granola Meetings Simple Sync plugin (pre-configured for 00_Inbox\Granola)." -ForegroundColor Green
} catch {
    Write-Host "[i] Inside Obsidian: Settings > Community Plugins > Browse > install 'Granola Meetings Simple Sync'." -ForegroundColor Yellow
}

# Auto-register vault in Obsidian's obsidian.json
try {
    $obsDir = Join-Path $env:APPDATA "obsidian"
    $obsCfgPath = Join-Path $obsDir "obsidian.json"
    New-Item -ItemType Directory -Force -Path $obsDir | Out-Null
    $cfg = if (Test-Path $obsCfgPath) {
        Get-Content $obsCfgPath -Raw | ConvertFrom-Json
    } else {
        [PSCustomObject]@{ vaults = [PSCustomObject]@{} }
    }
    if (-not $cfg.vaults) {
        $cfg | Add-Member -NotePropertyName "vaults" -NotePropertyValue ([PSCustomObject]@{}) -Force
    }
    $resolvedVault = (Resolve-Path $VaultPath).Path
    $already = $false
    foreach ($prop in $cfg.vaults.PSObject.Properties) {
        if ($prop.Value.path -eq $resolvedVault) { $already = $true; break }
    }
    if (-not $already) {
        $vid = ([guid]::NewGuid().ToString("N")).Substring(0, 16)
        $ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
        $entry = [PSCustomObject]@{ path = $resolvedVault; ts = $ts; open = $true }
        $cfg.vaults | Add-Member -NotePropertyName $vid -NotePropertyValue $entry -Force
        $cfg | ConvertTo-Json -Depth 6 | Set-Content -Path $obsCfgPath -Encoding UTF8
        Write-Host "[+] Registered vault automatically inside Obsidian." -ForegroundColor Green
    }
} catch {
    Write-Host "[i] Note: Open Obsidian and click 'Open folder as vault' -> $VaultPath" -ForegroundColor Yellow
}

# Optional Python venv setup for Full Kit
if ($Kit -eq "full") {
    Write-Header "Step 4 of 4: Setting Up Optional Python Tools (Full Kit)"
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py -and (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Host "[*] Installing Python 3.12 via winget..."
        winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
        $py = Get-Command python -ErrorAction SilentlyContinue
    }
    if ($py) {
        $venvDir = Join-Path $env:USERPROFILE ".gemini\tools\.venv"
        $reqFile = Join-Path $VaultPath "03_Resources\Automation & Scripts\requirements.txt"
        New-Item -ItemType Directory -Force -Path (Split-Path $venvDir) | Out-Null
        if (-not (Test-Path (Join-Path $venvDir "Scripts\python.exe"))) {
            & $py.Source -m venv $venvDir
        }
        $venvPip = Join-Path $venvDir "Scripts\pip.exe"
        $venvPy = Join-Path $venvDir "Scripts\python.exe"
        & $venvPip install --quiet --upgrade pip
        & $venvPip install --quiet -r $reqFile
        & $venvPy (Join-Path $VaultPath "03_Resources\Automation & Scripts\brain_sync.py")
        Write-Host "[+] Full Kit Python environment ready." -ForegroundColor Green
    } else {
        Write-Host "[i] Python was not detected yet. Restart your terminal later and run:" -ForegroundColor Yellow
        Write-Host "    pip install -r `"$VaultPath\03_Resources\Automation & Scripts\requirements.txt`""
    }
}

if ($tempRoot -and (Test-Path $tempRoot)) {
    Remove-Item -Path $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Header "All Done! Calm Slate Is Ready"
Write-Host "Vault Location: $VaultPath" -ForegroundColor Green
Write-Host ""
Write-Host "Your Next 2 Steps (5 Minutes):" -ForegroundColor Yellow
Write-Host "  1. Open Google Antigravity -> click 'Open Folder' -> pick:"
Write-Host "     $VaultPath"
Write-Host "  2. In the Antigravity chat box, type:"
Write-Host "     /onboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Obsidian is ready too. Open Obsidian anytime to view your notes and 00_Start_Here.md."
if ($Kit -eq "full") {
    Write-Host "Full Kit Guide: Open FULL_KIT_GUIDE.md inside your vault whenever you want to enable add-ons."
}
Write-Host ""
