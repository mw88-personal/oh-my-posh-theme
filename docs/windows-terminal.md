# Windows Terminal

Einstellungen → „JSON-Datei öffnen“ (`settings.json`).

## Standardwerte für alle Profile

```json
"profiles": {
    "defaults": {
        "colorScheme": "One Half Dark",
        "font": { "face": "MesloLGM NF", "size": 12 },
        "opacity": 70,
        "useAcrylic": true,
        "startingDirectory": "D:\\home\\marc",
        "intenseTextStyle": "all",
        "adjustIndistinguishableColors": "never",
        "autoMarkPrompts": true,
        "showMarksOnScrollbar": true
    },
    "list": [ … ]
}
```

| Einstellung | Warum |
|---|---|
| `intenseTextStyle: "all"` | Fetter Text wird wirklich fett. Mit dem Standard `"bright"` wird er nur heller – bei Hex-Farben gar nicht. |
| `adjustIndistinguishableColors: "never"` | Windows Terminal soll die Theme-Farben nicht eigenmächtig ändern. |
| `autoMarkPrompts`, `showMarksOnScrollbar` | Markierung pro Befehl in der Scrollleiste (ab Windows Terminal 1.21; davor mit Präfix `experimental.`). |
| `startingDirectory` | Start im eigenen Home statt in `C:\Windows\System32`. |
| `opacity` | 70 lässt den Desktop durchscheinen; Farben wirken dann je nach Hintergrund anders. Für einheitliche Farben ≥ 90. |

Keine profilspezifischen `font`- oder `intenseTextStyle`-Einträge – sonst unterscheiden sich
Schriftgröße (Strg+0 setzt auf den Profilwert zurück) und Darstellung je Profil.

## Profile

```json
{
    "guid": "{574e775e-4f2a-5b96-ac1e-a2962a402336}",
    "name": "PowerShell",
    "source": "Windows.Terminal.PowershellCore",
    "commandline": "pwsh.exe -NoLogo"
},
{
    "name": "Debian",
    "source": "Windows.Terminal.Wsl",
    "startingDirectory": "~"
}
```

- `-NoLogo` blendet die Zeile „PowerShell 7.x.y“ beim Start aus.
- WSL-Profile brauchen `"startingDirectory": "~"`, sonst starten sie in `/mnt/d/home/marc`.
- `defaultProfile` auf die GUID von „PowerShell“ (PowerShell 7) setzen, nicht „Windows PowerShell“.

## Tastenbelegung

```json
"keybindings": [
    { "keys": "ctrl+up",   "command": { "action": "scrollToMark", "direction": "previous" } },
    { "keys": "ctrl+down", "command": { "action": "scrollToMark", "direction": "next" } }
]
```

**Strg+V nicht belegen.** Dann übernimmt PSReadLine in PowerShell das Einfügen und fügt mehrere
Zeilen als Block ein, der erst mit Enter ausgeführt wird. In bash/SSH-Sitzungen Strg+Umschalt+V
verwenden. Einfügen per Rechtsklick führt in PowerShell weiterhin jede Zeile einzeln aus.

## Schriftart

Das Theme braucht eine **Nerd Font** (runde Box-Enden U+E0B6/U+E0B4). Getestet mit **MesloLGM NF**.

Alternativen (monospace, serifenlos im Charakter):

| Schrift | Hinweis |
|---|---|
| Cascadia Mono NF | Microsofts Terminal-Schrift, offiziell mit Nerd-Font-Symbolen, ohne Ligaturen |
| JetBrains Mono (Nerd Font) | groß, sehr klare Unterscheidung von `0`/`O`, `1`/`l`/`I` |
| Fira Mono / Hack (Nerd Font) | ruhig, klassisch |

Nerd-Font-Varianten lassen sich mit `oh-my-posh font list` anzeigen und mit
`oh-my-posh font install <Name>` installieren. Die genaue Schriftbezeichnung für `"face"` danach
aus der Auswahlliste in den Windows-Terminal-Einstellungen übernehmen.

Prüfen: Die runden Enden schließen sauber an den Text an, `»` und `✘` haben passende Größe.
