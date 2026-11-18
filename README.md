# oh-my-posh-theme · mw88

Ein plattformübergreifendes [oh-my-posh](https://ohmyposh.dev)-Theme für PowerShell 7 und bash
(lokal in WSL und per SSH auf Linux-Servern) in Windows Terminal. Ziel: **Die wichtigen Dinge sofort
erkennen – wer bin ich, wo bin ich, in welchem Zustand – und alles andere nur als ruhige Information.**

Das Repo enthält ausschließlich das Theme (`mw88.omp.json`) und Anleitungen. Die Einbindung ins
jeweilige System ist bewusst Sache der Plattform und steht in [`docs/`](docs/).

---

## Vorschau

```
fatal: Need to specify how to reconcile divergent branches.
                                                                   2.3s ( ✘ 1 )   ← Statuszeile des vorigen Befehls
                                                                                  ← Leerzeile
                                              ╭ 1 staged · 2 modified · 1 untracked   ← Git-Annotation
●● Marc@laptop  ~/projects/oh-my-posh-theme  ( main ↑1 )  (oh-my-posh-theme) » git push
```

Entfernt und als root:

```
●● ansible@bw16-pve  /etc  » sudo -i
●● root@bw16-pve  /etc  # _
```

Ältere Befehle schrumpft der Transient Prompt (nur PowerShell) auf eine Zeile:

```
oh-my-posh-theme » git pull
fatal: Need to specify how to reconcile divergent branches.
  ✘ 1
oh-my-posh-theme » git pull --rebase
```

`( … )` steht für die farbigen Boxen mit runden Enden.

---

## Aufbau des Prompts

| Zeile | Inhalt | Wann sichtbar |
|---|---|---|
| Status | Dauer des vorigen Befehls (ab 2 s) und Exit-Code (`✘ n`, Bordeaux-Box), rechtsbündig | immer als Zeile vorhanden; ohne Fehler und unter 2 s leer |
| Leerzeile | Abstand zwischen Status und Prompt | immer |
| Git-Annotation | `╭ n staged · n modified · n deleted · n untracked · n conflict · n stashed`, der Haken steht genau über dem Branchnamen | nur in Git-Repos mit Änderungen oder Stashes |
| Prompt | Punkte · `user@host` · Pfad · Git-Branch · venv · Eingabezeichen – die Eingabe beginnt in derselben Zeile | immer; Branch und venv nur, wenn vorhanden |

Die Statuszeile gehört zum **vorigen** Befehl und steht direkt unter dessen Ausgabe. Die
Annotation beschreibt den **aktuellen** Zustand und steht deshalb direkt über dem Prompt.

### Die zwei Punkte

Der **erste Punkt** zeigt, *wer* du bist, der **zweite**, *wo* du bist.

| Situation | Erster Punkt | Zweiter Punkt | Hostname | Eingabe |
|---|---|---|---|---|
| Nutzer, lokal (Windows, WSL) | hell | blau | grau | `»` |
| Nutzer, entfernt | orange | orange | orange | `»` |
| root/Administrator, lokal | rot | blau | grau | `#` |
| root/Administrator, entfernt | rot | orange | orange | `#` |

Lokal oder entfernt erkennt das Theme selbst: Windows oder WSL gilt als lokal, alles andere als
entfernt – auch eine Server-Konsole ohne SSH.

### Git

| Element | Bedeutung |
|---|---|
| Box mit Branchname | aktueller Branch (bzw. Commit bei detached HEAD) |
| `↑n` / `↓n` in der Box | Commits voraus / zurück gegenüber dem Upstream; keine Pfeile = synchron |
| `staged` | vorgemerkt (`git add`) |
| `modified` | geändert, nicht vorgemerkt |
| `deleted` | gelöscht, nicht vorgemerkt |
| `untracked` | neu, nicht versioniert |
| `conflict` | Merge-Konflikt |
| `stashed` | Einträge im Stash |

Ein sauberes Repo zeigt nur die Branch-Box, ohne Annotationszeile.

### Farben (RWTH-Palette)

| Farbe | Hex | Verwendung |
|---|---|---|
| Blau, aufgehellt | `#4C87BC` | zweiter Punkt lokal |
| Orange | `#F6A800` | Punkte und Hostname entfernt, Hostname im Transient Prompt |
| RWTH-Rot | `#CC071E` | erster Punkt bei root/Administrator |
| Bordeaux | `#A11035` | Fehler-Box `✘`, Fehlercode im Transient Prompt |
| Maigrün | `#BDCD00` | Eingabezeichen `»` bzw. `#` |
| Violett | `#7A6FAC` | kleine Symbole: venv, `↑`/`↓`, `»` im Transient Prompt |
| Hell | `#e6e6e6` | Nutzername, aktueller Ordner, erster Punkt lokal |
| Grau | `#8b919a` | Nebensächliches: Hostname lokal, Elternpfad, Dauer, Annotation |
| Dunkelgrau | `#454b57` | Git-Box |

Gelb kommt bewusst nicht vor.

---

## Voraussetzungen

- **oh-my-posh** – getestet mit **32.1.0** (Windows, WSL). Konfigurationsformat `"version": 3`.
  Auf Servern mit älterer Version vor dem Ausrollen testen (siehe [`docs/linux.md`](docs/linux.md)).
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

Zustände zum Durchspielen: `cmd /c exit 3` bzw. `false` (Fehler), `Start-Sleep 3` bzw. `sleep 3`
(Dauer), ein venv aktivieren, Dateien im Repo ändern (Annotation), Testsitzung als Administrator
bzw. `sudo -i` (root), Pfade mit `~` (Home) und mit Laufwerksbuchstaben (Ausrichtung der Annotation).

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
- **Einzeiliger Prompt.** Die Eingabe beginnt in derselben Zeile wie Nutzer, Host, Pfad und Branch.
  Ein mehrzeiliger Prompt mit eigener Eingabezeile wurde ausprobiert (v1) und wieder verworfen.
- **Git-Zustand als Annotation.** Statt die Prompt-Zeile zu verlängern oder rechtsbündig neben die
  Eingabe zu setzen (dort würde ein langer Befehl darüberschreiben), steht der Zustand als Fußnote
  über dem Branch. Im Transient Prompt entfällt er automatisch.
- **Zwei kleine Punkte statt Host-Box.** Dezent, aber eindeutig: Der erste Punkt zeigt die Rolle
  (rot = root/Administrator), der zweite den Ort (blau = lokal, orange = entfernt). Ein geteilter
  Punkt aus zwei Halbkreisen wurde verworfen: Die großen Nerd-Font-Halbkreise waren zu wuchtig, die
  kleinen Halbkreiszeichen hinterlassen je nach Schrift eine Lücke.
- **Aufmerksamkeit lenken:** Farbe nur für Rolle, Ort, Fehler und Eingabe. Nutzername und aktueller
  Ordner sind fett und hell, alles andere grau. Die Annotation ist einfarbig – Farbe wäre Clutter.
- **Status gehört zum vorigen Befehl.** Eigene Zeile unter dessen Ausgabe, abgesetzt durch eine
  Leerzeile vom neuen Prompt; das Eingabezeichen wird nicht nach dem Status eingefärbt.
- **Keine Uhrzeit im Prompt.** Die Dauer deckt das Segment ab (ab 2 s); für „wann lief das?“ ist
  die Shell-History der bessere Ort (siehe Ideen).
- **Englische Git-Begriffe**, konsistent mit Git selbst.
- **Kopierfreundlich:** keine Trennlinie, keine Pfeil-Trennzeichen; Fortsetzungszeilen beginnen mit
  zwei Leerzeichen statt `>` und lassen sich direkt wieder einfügen.
- **Kontrast vor Farbtreue:** Blau und Bordeaux nicht als Schriftfarbe auf dunklem Grund
  (Kontrast ≈ 2 : 1); für den Punkt ein aufgehelltes Blau, für root RWTH-Rot statt Bordeaux.
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

- **Ausrichtung der Annotation** wird im Template aus Nutzername, Hostname und Pfad berechnet
  (Anzahl Zeichen). Der Pfad im Prompt wird deshalb von einem eigenen Template erzeugt, nicht vom
  `path`-Segment – beide müssen identisch bleiben. Zeichen, die im Terminal doppelt breit sind
  (Emoji, CJK) in Pfad oder Namen, verschieben den Haken.
- **Erster Punkt lokal:** Das Farb-Tag ist leer (`<>●</>`); der Punkt erbt die Vordergrundfarbe
  des Segments (`#e6e6e6`). Wer die Segmentfarbe ändert, ändert damit auch diesen Punkt.
- **Unsichtbare Zeichen:** oh-my-posh verwirft Zeilen, die nur aus Leerzeichen bestehen. Damit
  Statuszeile und Leerzeile auch ohne Inhalt erscheinen, enthalten sie je ein leeres
  Braille-Zeichen (U+2800). Wer diese Zeilen kopiert, kopiert es mit.
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
| `v1.0.0` | Mehrzeiliges Design: Statuszeile, Host-Box, Git-Zeile, eigene Eingabezeile, Transient und Secondary Prompt |
| `v2.0.0` | Einzeiliger Prompt: Rollen- und Ortspunkt, Git-Annotation über dem Branch, Leerzeile nach der Statuszeile |
