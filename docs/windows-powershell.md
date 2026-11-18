# Windows: PowerShell 7

Requirements: PowerShell 7 (MSIX/Store version) and oh-my-posh via winget.

```powershell
winget install --id Microsoft.PowerShell --source winget     # if not installed yet
winget install --id JanDeDobbeleer.OhMyPosh --source winget
```

## 1. Install or update the theme

Installs a tagged release directly from GitHub. To update, just change `$tag`.

```powershell
$tag  = "v2.0.0"
$dest = "D:\usr\local\share\oh-my-posh\themes"
New-Item -ItemType Directory -Force $dest | Out-Null
Invoke-WebRequest "https://raw.githubusercontent.com/mw88-personal/oh-my-posh-theme/$tag/mw88.omp.json" -OutFile "$dest\mw88.omp.json"
```

## 2. Profile

`notepad $PROFILE` (PowerShell 7: `…\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`):

```powershell
# --- Prompt: oh-my-posh with the system-wide theme ---
oh-my-posh init pwsh --config "D:\usr\local\share\oh-my-posh\themes\mw88.omp.json" | Invoke-Expression

# The prompt ends with "» " – on syntax errors PSReadLine should only recolour the invisible space
Set-PSReadLineOption -PromptText ' '

# --- Syntax colours while typing (RWTH palette, no yellow) ---
Set-PSReadLineOption -Colors @{
    Command          = "`e[1;38;2;255;255;255m"   # commands: bold white
    Parameter        = "`e[38;2;122;111;172m"     # -parameters: violet
    Keyword          = "`e[38;2;122;111;172m"     # if, foreach: violet
    String           = "`e[38;2;246;168;0m"       # "strings": orange
    Variable         = "`e[38;2;230;230;230m"
    Number           = "`e[38;2;230;230;230m"
    Operator         = "`e[38;2;139;145;154m"     # | ; = : grey
    Comment          = "`e[3;38;2;107;114;128m"   # comments: grey italic
    InlinePrediction = "`e[3;38;2;107;114;128m"   # suggestions from history
    Error            = "`e[4;38;2;246;168;0m"     # syntax errors: orange, underlined
}

# --- Output colours ---
$PSStyle.Formatting.Error       = "`e[38;2;246;168;0m"                    # errors: orange
$PSStyle.Formatting.ErrorAccent = "`e[1;38;2;27;29;35;48;2;246;168;0m"    # accent: dark bold on orange
$PSStyle.Formatting.Warning     = "`e[38;2;102;152;197m"                  # warnings: blue, lightened
$PSStyle.Formatting.Verbose     = "`e[38;2;139;145;154m"
$PSStyle.Formatting.Debug       = "`e[38;2;139;145;154m"

# --- Load Terminal-Icons lazily (saves ~0.6 s at startup) ---
# "PowerShell.OnIdle" fires once the prompt is shown; -Global because the action block has its own scope.
$null = Register-EngineEvent -SourceIdentifier PowerShell.OnIdle -MaxTriggerCount 1 -Action {
    Import-Module Terminal-Icons -Global
}
```

Install Terminal-Icons once: `Install-Module Terminal-Icons -Scope CurrentUser`.

## 3. Windows PowerShell 5.1 (optional)

Prompt only, without colour settings (old PSReadLine 2.0, no `$PSStyle`):

```powershell
Set-Content (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'WindowsPowerShell\Microsoft.PowerShell_profile.ps1') `
  'oh-my-posh init pwsh --config "D:\usr\local\share\oh-my-posh\themes\mw88.omp.json" | Invoke-Expression'
```

## Test

New tab in Windows Terminal:

- The prompt appears, without a message about how long loading the profiles took.
- After 1–2 s, `ls` shows icons.
- `cmd /c exit 3` → `✘ 3`; `Start-Sleep 3` → `3s`.
- In a repository with changes, the annotation hook `╭` sits above the branch – also under `~\…`
  (home) and in paths with drive letters.
- `Get-Item C:\doesnotexist` → error in orange; `Write-Warning "Test"` → blue.
- After the next command, the previous prompt has shrunk to one line (transient prompt).

## Troubleshooting

- **An old version is used:** `oh-my-posh version; (Get-Command oh-my-posh).Source` – only the path
  under `…\WindowsApps\` should remain.
- **Cursor in the wrong place, prompt shifted:** Is it really PowerShell 7?
  `$PSVersionTable.PSVersion`, `(Get-Module PSReadLine).Version` (≥ 2.3).
- **Download fails (404):** tag misspelled or repository not public.
