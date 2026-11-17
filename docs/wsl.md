# WSL (Debian)

Aufbau wie auf den Linux-Servern:

| Was | Wo |
|---|---|
| Programm | `/usr/local/bin/oh-my-posh` |
| Theme | `/usr/local/share/oh-my-posh/themes/mw88.omp.json` |
| Einbindung | Block in `/etc/bash.bashrc` |

WSL wird automatisch als **lokal** erkannt (blaue Host-Box).

## 0. Bestandsaufnahme

```bash
type -a oh-my-posh; oh-my-posh version
grep -n posh ~/.bashrc ~/.profile ~/.bash_profile /etc/bash.bashrc /etc/profile.d/* 2>/dev/null
locale | grep -E '^(LANG|LC_CTYPE)='
uname -m
```

- Es soll nur **ein** `oh-my-posh` geben. Eine Installation per Installationsskript liegt meist in
  `~/.local/bin` und steht im `PATH` vor `/usr/local/bin` – entfernen.
- Locale muss UTF-8 sein, sonst berechnet bash die Zeilenlänge falsch
  (`sudo apt install locales && sudo dpkg-reconfigure locales`).

## 1. oh-my-posh installieren bzw. aktualisieren

```bash
v=32.1.0
sudo curl -fsSL -o /usr/local/bin/oh-my-posh \
  "https://github.com/JanDeDobbeleer/oh-my-posh/releases/download/v$v/posh-linux-amd64"
sudo chmod 755 /usr/local/bin/oh-my-posh
rm -f ~/.local/bin/oh-my-posh; hash -r
oh-my-posh version
```

Bei `uname -m` = `aarch64` heißt die Datei `posh-linux-arm64`.

## 2. Theme übernehmen

Das Theme kommt aus der (getaggten) Windows-Installation – kein eigener GitHub-Zugang nötig:

```bash
sudo install -D -m 644 /mnt/d/usr/local/share/oh-my-posh/themes/mw88.omp.json \
  /usr/local/share/oh-my-posh/themes/mw88.omp.json
```

Update: erst unter Windows installieren ([windows-powershell.md](windows-powershell.md)), dann diese Zeile.

## 3. Einbindung (einmalig)

```bash
sudo tee -a /etc/bash.bashrc >/dev/null <<'EOF'

# BEGIN oh-my-posh (siehe github.com/mw88-personal/oh-my-posh-theme)
if [ -x /usr/local/bin/oh-my-posh ] && [ "$TERM" != "linux" ]; then
    eval "$(oh-my-posh init bash --config /usr/local/share/oh-my-posh/themes/mw88.omp.json)"
fi
# END oh-my-posh
EOF
```

`$TERM != linux` schaltet den Prompt in einer reinen Textkonsole ab, die keine Nerd-Font-Glyphen kann.
Alte `oh-my-posh init`-Zeilen in `~/.bashrc` oder `~/.profile` entfernen.

## Test

Neuer Debian-Tab: blaue Host-Box, maigrünes `»`; `false` → `✘ 1`; `sleep 3` → `3s`.
Kein Transient Prompt (bash ohne ble.sh).

Git-Repos unter `/mnt/d/…` sind aus WSL spürbar langsamer – das liegt am Dateizugriff über die
Windows-Grenze, nicht am Theme.
