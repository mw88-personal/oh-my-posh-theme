#!/usr/bin/env bash
# Regenerates the README preview images (docs/images/*.svg) from mw88.omp.json.
# Requires: oh-my-posh >= 32, git, python3. Run from anywhere, e.g. in WSL:
#   ./tools/render-preview.sh
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
theme="$repo/mw88.omp.json"
data="$repo/tools/preview-data"
out="$repo/docs/images"
mkdir -p "$out"

# Throw-away home and demo repository, so the images never show real paths or projects
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp"
demo="$tmp/projects/oh-my-posh-theme"
mkdir -p "$demo"
cd "$demo"
git init -q -b main
git config user.name demo
git config user.email demo@example.invalid
printf 'a\n' > a; printf 'b\n' > b; printf 'c\n' > c
git add . && git commit -qm init
printf 'x\n' >> a; printf 'y\n' >> b; rm c          # 2 modified, 1 deleted
printf 'n\n' > new1; printf 'n\n' > new2            # 2 untracked
printf 's\n' > staged; git add staged               # 1 staged

render() { # <name> <data file> <directory>
  ( cd "$3" && oh-my-posh config export image \
      --config "$theme" --data "$data/$2" \
      --terminal-width 100 --background-color '#1b1d23' \
      --font-family '"MesloLGM Nerd Font", "MesloLGM NF", "Cascadia Mono NF", "Hack Nerd Font", ui-monospace, monospace' \
      --output "$out/$1.svg" 2>/dev/null )
  python3 "$repo/tools/fix-svg.py" "$out/$1.svg"
}

export VIRTUAL_ENV="$demo/.venv"
render local local.json "$demo"
python3 "$repo/tools/session-svg.py" --theme "$theme" --data "$data/local.json" --out "$out/session.svg"
unset VIRTUAL_ENV
render remote remote.json /etc
render root root.json /etc

echo "Updated: $out/local.svg, remote.svg, root.svg, session.svg"
