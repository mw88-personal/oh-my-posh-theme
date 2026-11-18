# Windows: PowerShell 7

Voraussetzungen: PowerShell 7 (MSIX/Store-Version), oh-my-posh per winget, Git mit SSH-Zugang zu GitHub.

```powershell
winget install --id Microsoft.PowerShell --source winget     # falls noch nicht vorhanden
winget install --id JanDeDobbeleer.OhMyPosh --source winget
ssh -T git@github.com                                         # muss "Hi mw88-personal!" melden
```

## 1. Theme installieren bzw. aktualisieren

Installiert wird ein getaggter Stand. Für ein Update nur `$tag` ändern.

```powershell
$tag  = "v2.0.0"
$dest = "D:\usr\local\share\oh-my-posh\themes"
$tmp  = Join-Path $env:TEMP "oh-my-posh-theme-$tag"

git -c advice.detachedHead=false clone --quiet --depth 1 --branch $tag git@github.com:mw88-personal/oh-my-posh-theme.git $tmp
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item "$tmp\mw88.omp.json" $dest -Force
Remove-Item -Recurse -Force $tmp
```

Die Warnung `refs/tags/… is not a commit!` ist harmlos: Annotierte Tags sind eigene Objekte,
Git checkt trotzdem den Commit aus, auf den der Tag zeigt.

## 2. Profil

`notepad $PROFILE` (PowerShell 7: `…\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`):

```powershell
# --- Prompt: oh-my-posh mit systemweit installiertem Theme ---
oh-my-posh init pwsh --config "D:\usr\local\share\oh-my-posh\themes\mw88.omp.json" | Invoke-Expression

# Prompt endet auf "» " – PSReadLine soll bei Syntaxfehlern nur das unsichtbare Leerzeichen umfärben
Set-PSReadLineOption -PromptText ' '

# --- Syntaxfarben beim Tippen (RWTH-Palette, kein Gelb) ---
Set-PSReadLineOption -Colors @{
    Command          = "`e[1;38;2;255;255;255m"   # Befehle: fett weiß
    Parameter        = "`e[38;2;122;111;172m"     # -Parameter: Violett
    Keyword          = "`e[38;2;122;111;172m"     # if, foreach: Violett
    String           = "`e[38;2;246;168;0m"       # "Strings": Orange
    Variable         = "`e[38;2;230;230;230m"
    Number           = "`e[38;2;230;230;230m"
    Operator         = "`e[38;2;139;145;154m"     # | ; = : Grau
    Comment          = "`e[3;38;2;107;114;128m"   # Kommentare: grau kursiv
    InlinePrediction = "`e[3;38;2;107;114;128m"   # Vorschläge aus der History
    Error            = "`e[4;38;2;246;168;0m"     # Syntaxfehler: Orange, unterstrichen
}

# --- Ausgabefarben ---
$PSStyle.Formatting.Error       = "`e[38;2;246;168;0m"                    # Fehler: Orange
$PSStyle.Formatting.ErrorAccent = "`e[1;38;2;27;29;35;48;2;246;168;0m"    # Akzent: dunkel fett auf Orange
$PSStyle.Formatting.Warning     = "`e[38;2;102;152;197m"                  # Warnungen: Blau, aufgehellt
$PSStyle.Formatting.Verbose     = "`e[38;2;139;145;154m"
$PSStyle.Formatting.Debug       = "`e[38;2;139;145;154m"

# --- Terminal-Icons verzögert laden (spart ~0,6 s beim Start) ---
# "PowerShell.OnIdle" feuert, sobald der Prompt steht; -Global, weil der Action-Block einen eigenen Scope hat.
$null = Register-EngineEvent -SourceIdentifier PowerShell.OnIdle -MaxTriggerCount 1 -Action {
    Import-Module Terminal-Icons -Global
}
```

Terminal-Icons einmalig installieren: `Install-Module Terminal-Icons -Scope CurrentUser`.

## 3. Windows PowerShell 5.1 (optional)

Nur der Prompt, ohne Farbeinstellungen (altes PSReadLine 2.0, kein `$PSStyle`):

```powershell
Set-Content (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'WindowsPowerShell\Microsoft.PowerShell_profile.ps1') `
  'oh-my-posh init pwsh --config "D:\usr\local\share\oh-my-posh\themes\mw88.omp.json" | Invoke-Expression'
```

## Test

Neuer Tab in Windows Terminal:

- Prompt erscheint, keine Meldung „Das Laden der persönlichen und Systemprofile dauerte …“.
- `ls` zeigt nach 1–2 s Icons.
- `cmd /c exit 3` → `✘ 3`; `Start-Sleep 3` → `3s`.
- `Get-Item C:\gibtsnicht` → Fehler in Orange; `Write-Warning "Test"` → Blau.
- Nach dem nächsten Befehl ist der vorige Prompt auf eine Zeile geschrumpft (Transient Prompt).

## Fehlersuche

- **Alte Version wird verwendet:** `oh-my-posh version; (Get-Command oh-my-posh).Source` – nur der
  Pfad unter `…\WindowsApps\` soll übrig sein.
- **Cursor sitzt falsch, Prompt verrutscht:** Läuft wirklich PowerShell 7? `$PSVersionTable.PSVersion`,
  `(Get-Module PSReadLine).Version` (≥ 2.3).
