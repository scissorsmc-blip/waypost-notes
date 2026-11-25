<#
.SYNOPSIS
    Waypost Notes - Unified Guided Windows Installer (Copilot & Antigravity Editions)

.DESCRIPTION
    Sets up Waypost Notes on Windows with your choice of edition:
      - Copilot Edition (Single App: Obsidian + Copilot plugin for Gemini or any supported AI)
      - Antigravity Edition (Obsidian + Google Antigravity desktop workspace)
    Installs apps, configures optional free Syncthing device sync, builds your PARA + AI
    Memory vault (06_Metadata\Gemini\), and registers the vault inside Obsidian.
#>

[CmdletBinding()]
param(
    [ValidateSet("", "copilot", "antigravity")]
    [string]$Edition = "",
    [ValidateSet("", "core", "full")]
    [string]$Kit = "",
    [ValidateSet("", "syncthing", "onedrive", "local")]
    [string]$SyncMode = "",
    [string]$VaultPath = "",
    [string]$RepoOwner = "scissorsmc-blip",
    [string]$RepoName = "waypost-notes",
    [string]$Branch = "main",
    [switch]$SkipAppInstall
)

$ErrorActionPreference = "Stop"

if (-not $Edition -and $env:WAYPOST_EDITION) {
    $Edition = $env:WAYPOST_EDITION.Trim().ToLower()
    $env:WAYPOST_EDITION = $null
}

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

Write-Header "Waypost Notes - Windows Setup"
Write-Host "Local-first Obsidian PARA vault with persistent AI memory (06_Metadata\Gemini),"
Write-Host "free Granola meeting sync, Calm Slate dark theme, and automatic device sync."
Write-Host ""

# 1. Choose Edition (Copilot vs Antigravity)
if (-not $Edition) {
    Write-Host "Choose your Waypost Notes edition:" -ForegroundColor Yellow
    Write-Host "  [1] Copilot Edition (Recommended for Beginners & Mobile)"
    Write-Host "      - Everything inside ONE app: Obsidian + Copilot plugin (free Gemini default,"
    Write-Host "        or any Copilot-compatible AI: OpenAI, Claude, Groq, OpenRouter, Ollama)."
    Write-Host ""
    Write-Host "  [2] Antigravity Edition (Desktop Power Workspace)"
    Write-Host "      - Pairs Obsidian (zero plugins required) with Google Antigravity desktop/CLI."
    Write-Host ""
    $echoice = Read-Host "Enter 1 for Copilot Edition or 2 for Antigravity Edition [Default: 1]"
    if ($echoice -eq "2") { $Edition = "antigravity" } else { $Edition = "copilot" }
}
$editionLabel = if ($Edition -eq "copilot") { "Copilot Edition (Single App)" } else { "Antigravity Edition" }
Write-Host "[+] Selected Edition: $editionLabel" -ForegroundColor Green

# 2. Choose Core Kit vs Full Kit
if (-not $Kit) {
    Write-Host ""
    Write-Host "Choose which kit to install:" -ForegroundColor Yellow
    Write-Host "  [1] Core Kit (Recommended for Beginners)"
    Write-Host "      - PARA vault, persistent AI memory, Granola sync script, Calm Slate dark theme,"
    Write-Host "        and 12 everyday /commands."
    Write-Host ""
    Write-Host "  [2] Full Kit (Power-Up Bundle)"
    Write-Host "      - Everything in Core Kit PLUS 12 extended /commands, 5 Calm Slate wallpapers,"
    Write-Host "        Android theme guide, and optional Calendar/Google Tasks/YNAB sync."
    Write-Host ""
    $choice = Read-Host "Enter 1 for Core Kit or 2 for Full Kit [Default: 1]"
    if ($choice -eq "2") { $Kit = "full" } else { $Kit = "core" }
}
Write-Host "[+] Selected Kit: $($Kit.ToUpper()) KIT" -ForegroundColor Green

# 3. Choose Cross-Device Sync Mode
if (-not $SyncMode) {
    Write-Host ""
    Write-Host "How will you sync Waypost Notes with other devices?" -ForegroundColor Yellow
    Write-Host "  [1] Windows + Android Phone/Tablet (Recommended - Free Syncthing, 1 QR scan, zero zombie files)"
    Write-Host "  [2] Windows + OneDrive (Desktop / Cloud Backup, or FolderSync on Android)"
    Write-Host "  [3] This PC Only (Local Documents folder - no sync)"
    Write-Host ""
    $schoice = Read-Host "Enter 1, 2, or 3 [Default: 1]"
    switch ($schoice) {
        "2" { $SyncMode = "onedrive" }
        "3" { $SyncMode = "local" }
        default { $SyncMode = "syncthing" }
    }
}
Write-Host "[+] Sync mode: $SyncMode" -ForegroundColor Green

# 4. Pick Vault Folder
$defaultFolderName = if ($Edition -eq "copilot") { "WaypostNotesCopilot" } else { "WaypostNotes" }
if (-not $VaultPath) {
    $defaultRoot = if (($SyncMode -eq "onedrive" -or $SyncMode -eq "syncthing") -and $env:OneDrive -and (Test-Path $env:OneDrive)) {
        Join-Path $env:OneDrive "Obsidian\$defaultFolderName"
    } else {
        Join-Path $env:USERPROFILE "Documents\$defaultFolderName"
    }
    Write-Host ""
    Write-Host "Where should your Waypost Notes vault folder be created?" -ForegroundColor Yellow
    Write-Host "  Recommended: $defaultRoot"
    $custom = Read-Host "Press Enter to accept recommended location, or paste another path"
    $VaultPath = if ([string]::IsNullOrWhiteSpace($custom)) { $defaultRoot } else { $custom.Trim('"').Trim() }
}
Write-Host "[+] Vault folder: $VaultPath" -ForegroundColor Green

# 5. Install Apps via winget
if (-not $SkipAppInstall) {
    $stepTitle = if ($Edition -eq "copilot") {
        "Step 1 of 4: Installing Obsidian & Granola"
    } else {
        "Step 1 of 4: Installing Obsidian, Antigravity & Granola"
    }
    Write-Header $stepTitle
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "[*] Checking/installing Obsidian..."
        winget install --id Obsidian.Obsidian -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
        Write-Host "[+] Obsidian ready." -ForegroundColor Green

        if ($Edition -eq "antigravity") {
            Write-Host "[*] Checking/installing Google Antigravity..."
            winget install --id Google.Antigravity -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
            Write-Host "[+] Google Antigravity ready." -ForegroundColor Green
        }

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
        if ($Edition -eq "antigravity") {
            Write-Host "      2. Google Antigravity: https://antigravity.google"
            Write-Host "      3. Granola (meetings): https://www.granola.ai"
        } else {
            Write-Host "      2. Granola (meetings): https://www.granola.ai"
        }
        Read-Host "Press Enter once installed (or to continue creating the vault now)"
    }
}

# 6. Locate local repo files or download from GitHub
Write-Header "Step 2 of 4: Preparing Waypost Notes Files"
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$localRepoRoot = Split-Path -Parent $scriptDir
$tempRoot = $null

if ((Test-Path (Join-Path $localRepoRoot "core-kit\SYNC_GUIDE.md")) -and (Test-Path (Join-Path $localRepoRoot "editions\$Edition\core-kit\AGENTS.md"))) {
    $sourceRoot = $localRepoRoot
    Write-Host "[+] Using local Waypost Notes files from: $sourceRoot" -ForegroundColor Green
} else {
    $tempRoot = Join-Path $env:TEMP ("waypost-notes-kit-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
    $zipPath = Join-Path $tempRoot "kit.zip"
    $zipUrl = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"
    Write-Host "[*] Downloading Waypost Notes from $zipUrl ..."
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
    Expand-Archive -Path $zipPath -DestinationPath $tempRoot -Force
    $extracted = Get-ChildItem -Path $tempRoot -Directory | Select-Object -First 1
    $sourceRoot = $extracted.FullName
    Write-Host "[+] Downloaded and unpacked Waypost Notes." -ForegroundColor Green
}

# 7. Build Vault (Shared Core + Edition Overlay + optional Full Kit)
New-Item -ItemType Directory -Force -Path $VaultPath | Out-Null
Copy-FolderSafe (Join-Path $sourceRoot "core-kit") $VaultPath
Copy-FolderSafe (Join-Path $sourceRoot "editions\$Edition\core-kit") $VaultPath
Write-Host "[+] Installed Core Kit vault structure, templates, dark theme, Granola sync, and 12 core skills." -ForegroundColor Green

if ($Kit -eq "full") {
    Copy-FolderSafe (Join-Path $sourceRoot "full-kit-addons") $VaultPath
    Copy-FolderSafe (Join-Path $sourceRoot "editions\$Edition\full-kit-addons") $VaultPath
    Write-Host "[+] Installed Full Kit add-ons (12 extended skills, 5 wallpapers, theme guide, and sync scripts)." -ForegroundColor Green
}

# 8. Edition-Specific Wiring + Register Obsidian Vault + Auto-Sync
Write-Header "Step 3 of 4: Wiring Edition, Registering Vault & Sync"

if ($Edition -eq "copilot") {
    $copilotDir = Join-Path $VaultPath ".obsidian\plugins\copilot"
    New-Item -ItemType Directory -Force -Path $copilotDir | Out-Null
    $copilotReleaseBase = "https://github.com/logancyang/obsidian-copilot/releases/latest/download"
    try {
        foreach ($asset in @("manifest.json", "main.js", "styles.css")) {
            $destAsset = Join-Path $copilotDir $asset
            Write-Host "[*] Downloading Copilot plugin asset: $asset ..."
            Invoke-WebRequest -Uri "$copilotReleaseBase/$asset" -OutFile $destAsset -UseBasicParsing
        }
        Write-Host "[+] Installed latest official Obsidian Copilot plugin (pre-configured for Google Gemini)." -ForegroundColor Green
    } catch {
        Write-Host "[i] Could not auto-download Copilot plugin assets right now." -ForegroundColor Yellow
        Write-Host "    Inside Obsidian: Settings > Community Plugins > Browse > search 'Copilot' > Install & Enable."
    }
} else {
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
    Write-Host "[+] Linked AGENTS.md and all skills into workspace and Google Antigravity." -ForegroundColor Green
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
    Write-Host "[i] Open Obsidian and click 'Open folder as vault' -> $VaultPath" -ForegroundColor Yellow
}

# Auto-setup Syncthing if chosen
if ($SyncMode -eq "syncthing") {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "[*] Installing Syncthing (free private device-to-device sync)..."
        try {
            winget install --id Syncthing.Syncthing -e --accept-source-agreements --accept-package-agreements --silent | Out-Null
        } catch {}
    }
    $stExe = Get-Command syncthing -ErrorAction SilentlyContinue
    if ($stExe) {
        try {
            $startupLnk = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup\Syncthing.lnk"
            $wsh = New-Object -ComObject WScript.Shell
            $sc = $wsh.CreateShortcut($startupLnk)
            $sc.TargetPath = $stExe.Source
            $sc.Arguments = "--no-browser --no-console"
            $sc.Save()

            Start-Process -FilePath $stExe.Source -ArgumentList "--no-browser --no-console" -WindowStyle Hidden
            Start-Sleep -Seconds 3
            $stId = if ($Edition -eq "copilot") { "waypost-notes-copilot" } else { "waypost-notes" }
            $stLabel = if ($Edition -eq "copilot") { "Waypost Notes Copilot" } else { "Waypost Notes" }
            & $stExe.Source cli config folders add --id $stId --label $stLabel --path $VaultPath | Out-Null
            Write-Host "[+] Syncthing running in background with $stLabel folder registered (.stignore active)." -ForegroundColor Green
            Write-Host "    Opening http://127.0.0.1:8384 (Actions > Show ID -> scan QR code in Android Syncthing-Fork)." -ForegroundColor Cyan
            Start-Process "http://127.0.0.1:8384"
        } catch {
            Write-Host "[i] Syncthing installed. See SYNC_GUIDE.md inside your vault to finish the 1-minute QR scan." -ForegroundColor Yellow
        }
    } else {
        Write-Host "[i] Download free Syncthing from https://syncthing.net and follow SYNC_GUIDE.md." -ForegroundColor Yellow
    }
} elseif ($SyncMode -eq "onedrive") {
    Write-Host "[i] Tip: Right-click '$VaultPath' in File Explorer -> 'Always keep on this device'. See SYNC_GUIDE.md." -ForegroundColor Yellow
}

# 9. Optional Python venv setup for Full Kit
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
        Write-Host "[i] Python was not detected yet. You can still use Waypost Notes right away without Python." -ForegroundColor Yellow
    }
}

if ($tempRoot -and (Test-Path $tempRoot)) {
    Remove-Item -Path $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Header "All Done! Waypost Notes ($editionLabel) Is Ready"
Write-Host "Vault Location: $VaultPath" -ForegroundColor Green
Write-Host ""
Write-Host "Your Next Quick Steps (5 Minutes):" -ForegroundColor Yellow
if ($Edition -eq "copilot") {
    Write-Host "  1. Get a free Google Gemini API key at: https://aistudio.google.com/apikey"
    Write-Host "     (Or connect any AI provider supported by Obsidian Copilot.)"
    Write-Host "  2. Open Obsidian -> Settings > Community Plugins (Turn On) -> Settings > Copilot >"
    Write-Host "     Providers > Google Gemini -> paste your API key and pick a Gemini model."
    Write-Host "  3. Connect free Granola meeting sync (1-time sign-in):"
    Write-Host "     python `"$VaultPath\03_Resources\Automation & Scripts\granola_sync.py`" --auth"
    Write-Host "  4. Open the Copilot chat sidebar and type: /onboard (and see SYNC_GUIDE.md)." -ForegroundColor Cyan
} else {
    Write-Host "  1. Connect free Granola meeting sync (1-time browser sign-in):"
    Write-Host "     python `"$VaultPath\03_Resources\Automation & Scripts\granola_sync.py`" --auth"
    Write-Host "  2. Open Google Antigravity -> Open Folder -> $VaultPath -> type: /onboard" -ForegroundColor Cyan
    Write-Host "  3. Open Obsidian anytime to view 00_Start_Here.md and SYNC_GUIDE.md."
}
if ($Kit -eq "full") {
    Write-Host "  Full Kit Guide: Open FULL_KIT_GUIDE.md whenever you want optional add-ons."
}
Write-Host ""
