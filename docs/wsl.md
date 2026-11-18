# WSL (Debian)

Same layout as on the Linux servers:

| What | Where |
|---|---|
| Program | `/usr/local/bin/oh-my-posh` |
| Theme | `/usr/local/share/oh-my-posh/themes/mw88.omp.json` |
| Integration | block in `/etc/bash.bashrc` |

WSL is detected automatically as **local** (light and blue dot).

## 0. Check the current state

```bash
type -a oh-my-posh; oh-my-posh version
grep -n posh ~/.bashrc ~/.profile ~/.bash_profile /etc/bash.bashrc /etc/profile.d/* 2>/dev/null
locale | grep -E '^(LANG|LC_CTYPE)='
uname -m
```

- There should be only **one** `oh-my-posh`. An installation via the install script usually lives
  in `~/.local/bin` and comes before `/usr/local/bin` in `PATH` – remove it.
- The locale must be UTF-8, otherwise bash computes the line length incorrectly
  (`sudo apt install locales && sudo dpkg-reconfigure locales`).

## 1. Install or update oh-my-posh

```bash
v=32.1.0
sudo curl -fsSL -o /usr/local/bin/oh-my-posh \
  "https://github.com/JanDeDobbeleer/oh-my-posh/releases/download/v$v/posh-linux-amd64"
sudo chmod 755 /usr/local/bin/oh-my-posh
rm -f ~/.local/bin/oh-my-posh; hash -r
oh-my-posh version
```

If `uname -m` reports `aarch64`, the file is called `posh-linux-arm64`.

## 2. Install or update the theme

A tagged release directly from GitHub, independent of the Windows installation. To update, just
change `tag`.

```bash
tag=v2.0.0
sudo install -d /usr/local/share/oh-my-posh/themes
sudo curl -fsSL -o /usr/local/share/oh-my-posh/themes/mw88.omp.json \
  "https://raw.githubusercontent.com/mw88-personal/oh-my-posh-theme/$tag/mw88.omp.json"
```

## 3. Integration (once)

```bash
sudo tee -a /etc/bash.bashrc >/dev/null <<'EOF'

# BEGIN oh-my-posh (see github.com/mw88-personal/oh-my-posh-theme)
if [ -x /usr/local/bin/oh-my-posh ] && [ "$TERM" != "linux" ]; then
    eval "$(oh-my-posh init bash --config /usr/local/share/oh-my-posh/themes/mw88.omp.json)"
fi
# END oh-my-posh
EOF
```

`$TERM != linux` turns the prompt off on a plain text console, which can't render Nerd Font glyphs.
Remove old `oh-my-posh init` lines from `~/.bashrc` or `~/.profile`.

## Test

New Debian tab: light and blue dot, may green `»`; `false` → `✘ 1`; `sleep 3` → `3s`;
in a repository with changes, the annotation hook `╭` sits above the branch.
No transient prompt (bash without ble.sh).

Git repositories under `/mnt/d/…` are noticeably slower from WSL – that's due to file access across
the Windows boundary, not the theme.
