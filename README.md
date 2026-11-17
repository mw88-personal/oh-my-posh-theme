# oh-my-posh-theme · mw88

Ein plattformübergreifendes [oh-my-posh](https://ohmyposh.dev)-Theme für PowerShell 7, bash
(lokal in WSL und per SSH auf Linux-Servern) in Windows Terminal. Ziel: **Die wichtigen Dinge sofort
erkennen – wo bin ich, als wer, in welchem Zustand – und alles andere nur als ruhige Information.**

Das Repo enthält ausschließlich das Theme (`mw88.omp.json`) und Anleitungen. Die Einbindung ins
jeweilige System ist bewusst Sache der Plattform und steht in [`docs/`](docs/).

---

## Vorschau

```
                                                              2.3s ( ✘ 1 )     ← Statuszeile (nur bei Fehler/Dauer)
( Marc@laptop ) D:\home\marc\projects\oh-my-posh-theme (.venv) ( main ↑1 )     ← Wo bin ich?
  └ 1 staged · 2 modified · 1 untracked                                        ← nur in Git-Repos mit Änderungen
» _                                                                            ← Eingabe
```

Ältere Befehle schrumpft der Transient Prompt (nur PowerShell) auf eine Zeile:

```
oh-my-posh-theme » git pull
fatal: Need to specify how to reconcile divergent branches.
  ✘ 1
oh-my-posh-theme » git pull --rebase
```

`( … )` steht hier für die farbigen Boxen mit runden Enden.

---

## Aufbau des Prompts

| Zeile | Inhalt | Wann sichtbar |
|---|---|---|
| 1 · Status | Dauer des letzten Befehls (ab 2 s) und Exit-Code (`✘ n`, Bordeaux-Box), rechtsbündig | immer als Zeile vorhanden; ohne Fehler und unter 2 s leer und wirkt als Trenner |
| 2 · Ort | Box `user@host` · Pfad (übergeordnete Ordner grau, aktueller Ordner fett und hell) · aktives venv · Box mit Git-Branch und `↑`/`↓` | immer; venv und Branch nur, wenn vorhanden |
| 3 · Git-Zustand | `└ n staged · n modified · n deleted · n untracked · n conflict · n stashed` | nur in Git-Repos mit Änderungen oder Stashes |
| 4 · Eingabe | `»` fett in Maigrün, als root `#` | immer |

Die Statuszeile gehört zum **vorigen** Befehl: Sie steht direkt unter dessen Ausgabe.

### Git-Zeile

| Wort | Bedeutung |
|---|---|
| `staged` | vorgemerkt (`git add`) |
| `modified` | geändert, nicht vorgemerkt |
| `deleted` | gelöscht, nicht vorgemerkt |
| `untracked` | neu, nicht versioniert |
| `conflict` | Merge-Konflikt |
| `stashed` | Einträge im Stash |
| `↑n` / `↓n` | Commits voraus / zurück gegenüber dem Upstream; keine Pfeile = synchron |

### Farben (RWTH-Palette)

| Farbe | Hex | Verwendung |
|---|---|---|
| Blau | `#00549F` | Host-Box lokal (Windows, WSL) |
| Orange | `#F6A800` | Host-Box entfernt (alles andere), Hostname im Transient Prompt |
| Bordeaux | `#A11035` | Host-Box root, Fehler-Box `✘` |
| Maigrün | `#BDCD00` | Eingabezeichen `»` bzw. `#` |
| Violett | `#7A6FAC` | kleine Symbole: venv, `↑`/`↓`, `»` im Transient Prompt |
| Grau | `#8b919a` | Nebensächliches: Elternpfad, Dauer, Git-Zeile |
| Dunkelgrau | `#454b57` | Git-Box |

Gelb kommt bewusst nicht vor.

---

## Voraussetzungen

- **oh-my-posh** – getestet mit **32.1.0** (Windows, WSL) und **29.17.0** (Server).
  Konfigurationsformat `"version": 3`.
- **Nerd Font** im Terminal (für die runden Box-Enden ``/``) – siehe
  [`docs/windows-terminal.md`](docs/windows-terminal.md#schriftart).
- **Truecolor-Terminal** (Windows Terminal) und **UTF-8**-Locale (unter Linux z. B. `en_US.UTF-8`).

---

## Installation

| Plattform | Anleitung | Theme liegt unter | Einbindung |
|---|---|---|---|
| Windows, PowerShell 7 | [`docs/windows-powershell.md`](docs/windows-powershell.md) | `D:\usr\local\share\oh-my-posh\themes\` | `$PROFILE` |
| Windows Terminal | [`docs/windows-terminal.md`](docs/windows-terminal.md) | – | `settings.json` |
| WSL (Debian) | [`docs/wsl.md`](docs/wsl.md) | `/usr/local/share/oh-my-posh/themes/` | `/etc/bash.bashrc` |
| Linux-Server | [`docs/linux.md`](docs/linux.md) | `/usr/local/share/oh-my-posh/themes/` | `/etc/bash.bashrc` (per Ansible) |
| cmd | – | – | **bewusst nicht** (siehe Designentscheidungen) |

Installiert wird immer ein **getaggter Stand**, nie der Arbeitsordner.

---

## Entwicklung und Release

Entwickelt wird lokal in `D:\home\marc\projects\oh-my-posh-theme`.

**Vorschau ohne das eigene Profil anzufassen:**

```powershell
# einmal rendern
oh-my-posh print primary --config .\mw88.omp.json --shell pwsh
oh-my-posh print transient --config .\mw88.omp.json --shell pwsh --status 1

# Testsitzung (mit exit zurück)
pwsh -NoProfile -NoExit -Command "oh-my-posh init pwsh --config '$PWD\mw88.omp.json' | Invoke-Expression; Set-PSReadLineOption -PromptText ' '"
```

bash in WSL:

```bash
bash --norc
eval "$(oh-my-posh init bash --config /mnt/d/home/marc/projects/oh-my-posh-theme/mw88.omp.json)"
```

Zustände zum Durchspielen: `cmd /c exit 3` bzw. `false` (Fehler), `Start-Sleep 3` bzw. `sleep 3` (Dauer),
ein venv aktivieren, Dateien im Repo ändern, Testsitzung als Administrator bzw. `sudo -i` (root).

**Release:**

```powershell
git add mw88.omp.json
git commit -m "…"
git tag -a vX.Y.Z -m "…"
git push --follow-tags
```

Danach auf jedem Rechner den Installationsschritt mit dem neuen Tag ausführen (siehe `docs/`).
Reine Doku-Änderungen brauchen keinen neuen Tag.

---

## Designentscheidungen

- **Theme plattformübergreifend, Einbindung pro Plattform.** Gleiche Optik überall; wie das Theme
  geladen wird, regelt jede Plattform selbst (Profil, `bash.bashrc`, Ansible). Das Theme enthält
  nichts Rechnerspezifisches.
- **Lokal oder entfernt wird automatisch erkannt:** Windows oder WSL gilt als lokal (blau), alles
  andere als entfernt (orange) – auch eine Server-Konsole ohne SSH. Root ist immer Bordeaux.
- **Aufmerksamkeit lenken:** Boxen nur für Host, Git-Branch und Fehler. Der Pfad hat keine Box,
  nur der aktuelle Ordner ist fett und hell. Die Git-Zeile ist einfarbig grau – Farbe wäre Clutter.
- **Status gehört zum vorigen Befehl.** Deshalb steht er in einer eigenen Zeile unter der Ausgabe
  und färbt nicht das Eingabezeichen.
- **Keine Uhrzeit im Prompt.** Die Dauer deckt das Segment ab (ab 2 s); für „wann lief das?“ ist
  die Shell-History der bessere Ort (siehe Ideen).
- **Englische Git-Begriffe**, konsistent mit Git selbst.
- **Kopierfreundlich:** keine Trennlinie, keine Pfeil-Trennzeichen; Fortsetzungszeilen beginnen mit
  zwei Leerzeichen statt `>` und lassen sich direkt wieder einfügen.
- **Kontrast vor Farbtreue:** Blau und Bordeaux nur als Hintergrund, nie als Schriftfarbe auf
  dunklem Grund (Kontrast ≈ 2 : 1). Aufgehellte Varianten nur außerhalb des Themes (Warnungen in
  PowerShell).
- **Transient Prompt** mit aktuellem Ordner, Hostname nur bei entfernten Hosts, Fehlercode des
  vorigen Befehls als eigene, eingerückte Zeile. Das `»` ist violett, damit das maigrüne `»` der
  aktuellen Eingabe vorbehalten bleibt.
- **cmd bleibt unverändert.** Mit gleichem Theme wäre cmd nicht mehr von PowerShell zu
  unterscheiden; der Standard-Prompt `C:\…>` ist das deutlichste Erkennungszeichen.
- **Shell-Integration** (`shell_integration: true`) sendet OSC-133-Marken: Windows Terminal zeigt
  Markierungen in der Scrollleiste und springt mit Strg+↑/↓ zwischen Befehlen.
- **Fenstertitel** `user@host: Ordner` – der Host ist auch im Tab erkennbar.

---

## Bekannte Eigenheiten

- **Unsichtbares Zeichen in der Statuszeile:** oh-my-posh verwirft Zeilen, die nur aus Leerzeichen
  bestehen. Damit die Statuszeile auch ohne Fehler als Trennzeile erscheint, steht am rechten Rand
  ein leeres Braille-Zeichen (U+2800). Wer diese Zeile kopiert, kopiert es mit.
- **Runde Box-Enden** sind Nerd-Font-Zeichen (U+E0B6/U+E0B4) und landen beim Kopieren im Text.
- **Transient Prompt** nur in PowerShell (und cmd/zsh/fish/nu); bash nur mit ble.sh. Auf den
  Servern bleibt der volle Prompt – das hebt entfernte Sitzungen im Verlauf ab.
- **Im Transient Prompt** ist nur der Exit-Code des vorigen Befehls verfügbar, keine Dauer.
- **Farbmarken in Templates** müssen wörtlich im Template stehen; von Funktionen (`printf`, `join`)
  erzeugte `<#…>`-Marken interpretiert oh-my-posh nicht.
- **venv `.venv`** wird mit dem Namen des Projektordners angezeigt (oh-my-posh-Standard).
- **PowerShell:** Der Prompt endet auf Leerzeichen; deshalb `Set-PSReadLineOption -PromptText ' '`,
  sonst überschreibt PSReadLine bei Syntaxfehlern das Eingabezeichen.
- **Einfügen per Rechtsklick** führt in PowerShell jede Zeile einzeln aus (PSReadLine unterstützt
  kein Bracketed Paste). Strg+V fügt als Block ein, wenn Windows Terminal Strg+V nicht belegt.

---

## Ideen für später

- `HISTTIMEFORMAT="%F %T "` systemweit setzen, damit `history` Datum und Uhrzeit zeigt.
- Server auf oh-my-posh 32.x anheben (gleicher Stand wie Windows/WSL).
- **fzf** (Fuzzy-Suche in der History mit Strg+R), **zoxide** (`z projekt`), **atuin**
  (durchsuchbare, synchronisierte History, selbst hostbar).
- **ble.sh** für bash: Vorschläge, Syntaxhervorhebung und Transient Prompt auch unter Linux.
- PSReadLine-Vorschläge als Liste: `Set-PSReadLineOption -PredictionViewStyle ListView`.
- Vorschaubild fürs README mit `oh-my-posh config export image` und `--data`-Dateien für
  reproduzierbare Zustände.

---

## Versionen

| Tag | Inhalt |
|---|---|
| `v0.1.0` | Ausgangsstand: Theme, wie es vor der Überarbeitung auf den Servern lief |
| `v1.0.0` | Neues Design: Statuszeile, RWTH-Farben, Host-Erkennung lokal/entfernt, Git-Zeile, Transient und Secondary Prompt |
