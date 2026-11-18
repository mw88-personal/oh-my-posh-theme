#!/usr/bin/env python3
"""Render a short terminal session (transient prompts, commands, output, current prompt) as SVG.

`oh-my-posh config export image` can only render the primary prompt. This script calls
`oh-my-posh print transient` / `print primary` instead, converts their ANSI output into SVG and
adds the typed commands and their output, so the README can show the transient prompt in action.

Run it from inside the demo repository (see render-preview.sh):
    session-svg.py --theme mw88.omp.json --data tools/preview-data/local.json --out docs/images/session.svg
"""
import argparse
import json
import os
import re
import subprocess
import tempfile
from html import escape

# The session to draw: (prompt kind, exit code of the previous command, duration of the previous
# command in ms, typed command, output lines)
SESSION = [
    ("transient", 0, 0, "git pull", ["fatal: Need to specify how to reconcile divergent branches."]),
    ("transient", 1, 0, "git pull --rebase", ["Successfully rebased and updated refs/heads/main."]),
    ("primary", 0, 3100, "", []),
]

FONT_FAMILY = ('"MesloLGM Nerd Font", "MesloLGM NF", "Cascadia Mono NF", "Hack Nerd Font", '
               'ui-monospace, monospace')
FONT_SIZE = 16
CELL = 0.6021 * FONT_SIZE      # horizontal advance of one cell (Hack Nerd Font ratio)
LINE = 22.35                   # vertical advance of one row
ASCENT, BOX_H = 14.95, 18.81   # segment background box relative to the baseline
PAD_X, HEADER, PAD_TOP, PAD_BOTTOM = 16, 26.67, 32.76, 20
BG, DEFAULT_FG = "#1b1d23", "#c8ccd4"
CMD_FG, PARAM_FG, STRING_FG = "#ffffff", "#7a6fac", "#f6a800"   # PSReadLine colours from the docs
CAP_L, CAP_R = "", ""

ANSI_RE = re.compile(r'\x1b\][^\x07]*\x07|\x1b\[([0-9;]*)([A-Za-z])|(\n)|(.)', re.S)


def parse_ansi(text):
    """Return rows of cells: {col: (char, fg, bg, bold)}."""
    rows, row, col = [], {}, 0
    fg, bg, bold = None, None, False
    for m in ANSI_RE.finditer(text):
        params, cmd, nl, ch = m.groups()
        if nl:
            rows.append(row); row, col = {}, 0
        elif ch is not None:
            row[col] = (ch, fg, bg, bold); col += 1
        elif cmd == "m":
            codes = [int(c) if c else 0 for c in (params or "0").split(";")]
            i = 0
            while i < len(codes):
                c = codes[i]
                if c == 0: fg, bg, bold = None, None, False
                elif c == 1: bold = True
                elif c == 22: bold = False
                elif c in (37, 39): fg = None
                elif c == 49: bg = None
                elif c in (38, 48) and i + 4 < len(codes) and codes[i + 1] == 2:
                    colour = "#%02x%02x%02x" % tuple(codes[i + 2:i + 5])
                    if c == 38: fg = colour
                    else: bg = colour
                    i += 4
                i += 1
        elif cmd == "C":
            col += int(params or 1)
    rows.append(row)
    return rows


def plain_row(text, fg=DEFAULT_FG, start=0, row=None):
    row = {} if row is None else row
    for i, ch in enumerate(text):
        row[start + i] = (ch, fg, None, False)
    return row


def command_row(row, command):
    """Append a typed command after the prompt, coloured roughly like PSReadLine."""
    col = max(row) + 1 if row else 0
    for n, word in enumerate(command.split(" ")):
        if n:
            row[col] = (" ", None, None, False); col += 1
        if n == 0: style = (CMD_FG, True)
        elif word.startswith("-"): style = (PARAM_FG, False)
        elif word.startswith('"'): style = (STRING_FG, False)
        else: style = (DEFAULT_FG, False)
        for ch in word:
            row[col] = (ch, style[0], None, style[1]); col += 1
    return row


def omp(kind, theme, data, code, duration, width):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        d = json.load(open(data))
        d.setdefault("env", {}).update({"Code": code, "ExecutionTime": duration})
        json.dump(d, f)
        tmp = f.name
    try:
        return subprocess.run(
            ["oh-my-posh", "print", kind, "--config", theme, "--shell", "pwsh",
             "--data", tmp, "--terminal-width", str(width)],
            capture_output=True, text=True, check=True).stdout
    finally:
        os.unlink(tmp)


def svg(rows, cols):
    width = 2 * PAD_X + cols * CELL
    height = HEADER + PAD_TOP + (len(rows) - 1) * LINE + PAD_BOTTOM
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.2f}" height="{height:.2f}" '
           f'viewBox="0 0 {width:.2f} {height:.2f}" font-family="{escape(FONT_FAMILY)}" font-size="{FONT_SIZE}px">',
           f'<rect x="0.5" y="0.5" width="{width - 1:.2f}" height="{height - 1:.2f}" rx="4" fill="{BG}" stroke="#ffffff" stroke-opacity="0.8"/>',
           f'<path fill="#313339" d="M 4.5,0.5 H {width - 4.5:.2f} A 4,4 0 0 1 {width - 0.5:.2f},4.5 V {HEADER:.2f} H 0.5 V 4.5 A 4,4 0 0 1 4.5,0.5 Z"/>',
           f'<line x1="0.5" y1="{HEADER:.2f}" x2="{width - 0.5:.2f}" y2="{HEADER:.2f}" stroke="#ffffff" stroke-opacity="0.8"/>']
    for i, sym in enumerate(("−", "▢", "×")):
        out.append(f'<text x="{width - 77.33 + i * 30.67:.2f}" y="18.47" font-size="14.67px" fill="#cfcfcf" text-anchor="middle">{sym}</text>')

    for r, row in enumerate(rows):
        base = HEADER + PAD_TOP + r * LINE
        top = base - ASCENT
        cols_sorted = sorted(row)
        # backgrounds
        for c in cols_sorted:
            _, _, bg, _ = row[c]
            if bg:
                out.append(f'<rect x="{PAD_X + c * CELL:.2f}" y="{top:.2f}" width="{CELL + 0.3:.2f}" height="{BOX_H}" fill="{bg}"/>')
        # glyph runs
        run, run_start, run_style = "", None, None

        def flush():
            if run and run.strip():
                fg, bold = run_style
                weight = ' font-weight="bold"' if bold else ""
                out.append(f'<text xml:space="preserve" x="{PAD_X + run_start * CELL:.2f}" y="{base:.2f}" '
                           f'textLength="{len(run) * CELL:.2f}" lengthAdjust="spacingAndGlyphs" '
                           f'fill="{fg or DEFAULT_FG}"{weight}>{escape(run)}</text>')

        prev = None
        for c in cols_sorted:
            ch, fg, _, bold = row[c]
            x = PAD_X + c * CELL
            if ch in (CAP_L, CAP_R):
                flush(); run, run_start, prev = "", None, None
                colour = fg or DEFAULT_FG
                r_ = BOX_H / 2
                if ch == CAP_L:
                    out.append(f'<path d="M {x + CELL:.2f},{top:.2f} A {r_:.2f},{r_:.2f} 0 0 0 {x + CELL:.2f},{top + BOX_H:.2f} Z" fill="{colour}"/>')
                else:
                    out.append(f'<path d="M {x:.2f},{top:.2f} A {r_:.2f},{r_:.2f} 0 0 1 {x:.2f},{top + BOX_H:.2f} Z" fill="{colour}"/>')
                continue
            ch = " " if ch == "⠀" else ch
            style = (fg, bold)
            if prev is not None and c == prev + 1 and style == run_style:
                run += ch
            else:
                flush(); run, run_start, run_style = ch, c, style
            prev = c
        flush()
    out.append("</svg>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=100)
    a = ap.parse_args()

    rows = []
    for kind, code, duration, command, output in SESSION:
        prompt_rows = parse_ansi(omp(kind, a.theme, a.data, code, duration, a.width))
        while prompt_rows and not prompt_rows[-1]:
            prompt_rows.pop()
        last = prompt_rows[-1]
        if command:
            command_row(last, command)
        else:
            plain_row("_", start=max(last) + 1, row=last)
        rows += prompt_rows
        rows += [plain_row(line) for line in output]

    open(a.out, "w", encoding="utf-8").write(svg(rows, a.width))


if __name__ == "__main__":
    main()
