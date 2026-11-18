#!/usr/bin/env python3
"""Post-process an SVG exported by `oh-my-posh config export image` for use in the README.

- Replaces the Nerd Font half-circle glyphs (U+E0B6/U+E0B4) with vector shapes, so the rounded
  box ends render correctly even where no Nerd Font is installed (e.g. on github.com).
- Replaces the invisible Braille blank (U+2800) with a normal space.
- Removes the "ohmyposh.dev" footer line.
"""
import re
import sys

CAP_L, CAP_R = "", ""
TEXT_RE = re.compile(r'<text([^>]*)>([^<]*)</text>')


def attr(attrs, name):
    m = re.search(rf'\b{name}="([^"]*)"', attrs)
    return m.group(1) if m else None


def main(path):
    svg = open(path, encoding="utf-8").read()
    rects = [(float(y), float(h)) for y, h in re.findall(r'<rect x="[^"]*" y="([^"]*)" width="[^"]*" height="([^"]*)"', svg)]

    def box_for(row_y):
        for y, h in rects:
            if row_y - 20 <= y <= row_y:
                return y, h
        return row_y - 14.95, 18.81  # Hack Nerd Font defaults at 16px

    def repl(m):
        attrs, content = m.group(1), m.group(2)
        if content.strip() == "ohmyposh.dev":
            return ""
        content = content.replace("⠀", " ")
        if CAP_L not in content and CAP_R not in content:
            return f"<text{attrs}>{content}</text>"
        x, y = float(attr(attrs, "x")), float(attr(attrs, "y"))
        cw = float(attr(attrs, "textLength")) / len(content)
        fill = attr(attrs, "fill") or "#ffffff"
        top, h = box_for(y)
        r = h / 2
        shapes = []
        for i, ch in enumerate(content):
            cx = x + i * cw
            if ch == CAP_L:   # flat side on the right, round side to the left
                shapes.append(f'<path d="M {cx + cw:.2f},{top:.2f} A {r:.2f},{r:.2f} 0 0 0 {cx + cw:.2f},{top + h:.2f} Z" fill="{fill}"/>')
            elif ch == CAP_R:  # flat side on the left, round side to the right
                shapes.append(f'<path d="M {cx:.2f},{top:.2f} A {r:.2f},{r:.2f} 0 0 1 {cx:.2f},{top + h:.2f} Z" fill="{fill}"/>')
        content = content.replace(CAP_L, " ").replace(CAP_R, " ")
        return "".join(shapes) + f"<text{attrs}>{content}</text>"

    svg = TEXT_RE.sub(repl, svg)
    open(path, "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
