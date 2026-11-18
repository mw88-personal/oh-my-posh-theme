# Windows Terminal

Settings → "Open JSON file" (`settings.json`).

## Defaults for all profiles

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

| Setting | Why |
|---|---|
| `intenseTextStyle: "all"` | Bold text is really rendered bold. With the default `"bright"` it only gets brighter – and with hex colours not even that. |
| `adjustIndistinguishableColors: "never"` | Windows Terminal should not change the theme's colours on its own. |
| `autoMarkPrompts`, `showMarksOnScrollbar` | A mark per command on the scrollbar (Windows Terminal 1.21+; earlier with the prefix `experimental.`). |
| `startingDirectory` | Start in your own home instead of `C:\Windows\System32`. |
| `opacity` | 70 lets the desktop shine through; colours then look different depending on the background. For consistent colours use ≥ 90. |

No profile-specific `font` or `intenseTextStyle` entries – otherwise font size (Ctrl+0 resets to
the profile value) and rendering differ per profile.

## Profiles

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

- `-NoLogo` hides the "PowerShell 7.x.y" line at startup.
- WSL profiles need `"startingDirectory": "~"`, otherwise they start in `/mnt/d/home/marc`.
- Set `defaultProfile` to the GUID of "PowerShell" (PowerShell 7), not "Windows PowerShell".

## Key bindings

```json
"keybindings": [
    { "keys": "ctrl+up",   "command": { "action": "scrollToMark", "direction": "previous" } },
    { "keys": "ctrl+down", "command": { "action": "scrollToMark", "direction": "next" } }
]
```

**Don't bind Ctrl+V.** Then PSReadLine handles pasting in PowerShell and inserts multiple lines as
one block that only runs when you press Enter. In bash/SSH sessions use Ctrl+Shift+V. Pasting with
right-click still runs each line separately in PowerShell.

## Font

The theme needs a **Nerd Font** (rounded box ends U+E0B6/U+E0B4). Tested with **MesloLGM NF**.

Alternatives (monospace, sans-serif in character):

| Font | Note |
|---|---|
| Cascadia Mono NF | Microsoft's terminal font, officially with Nerd Font symbols, no ligatures |
| JetBrains Mono (Nerd Font) | large, very clear distinction of `0`/`O`, `1`/`l`/`I` |
| Fira Mono / Hack (Nerd Font) | calm, classic |

List the Nerd Font variants with `oh-my-posh font list` and install one with
`oh-my-posh font install <name>`. Then take the exact font name for `"face"` from the drop-down in
the Windows Terminal settings.

Check: the rounded ends join the text cleanly, and `»`, `✘` and `●` have a fitting size.
