#!/usr/bin/env python3
"""Regenerate the block-letter wordmarks for QEPilot Stack.

The upstream markup carried ASCII art spelling the old project name. That
art is drawn from box-drawing glyphs, so a plain text search-and-replace
could not touch it. This builds fresh art from a hand-written glyph set
and swaps both <pre> blocks in index.html.

Idempotent: run it again after changing NAME / FOOTER.
"""
import os, re, sys

NAME   = "QEPILOT STACK"
FOOTER = "QEPILOT"

# 6-row block alphabet (box-drawing "shadow" style).
GLYPHS = {
'A': [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
'C': [" ██████╗", "██╔════╝", "██║     ", "██║     ", "╚██████╗", " ╚═════╝"],
'E': ["███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "███████╗", "╚══════╝"],
'I': ["██╗", "██║", "██║", "██║", "██║", "╚═╝"],
'K': ["██╗  ██╗", "██║ ██╔╝", "█████╔╝ ", "██╔═██╗ ", "██║  ██╗", "╚═╝  ╚═╝"],
'L': ["██╗     ", "██║     ", "██║     ", "██║     ", "███████╗", "╚══════╝"],
'O': [" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
'P': ["██████╗ ", "██╔══██╗", "██████╔╝", "██╔═══╝ ", "██║     ", "╚═╝     "],
'Q': [" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║▄▄ ██║", "╚██████╔╝", " ╚══▀▀═╝ "],
'S': ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
'T': ["████████╗", "╚══██╔══╝", "   ██║   ", "   ██║   ", "   ██║   ", "   ╚═╝   "],
' ': ["    "] * 6,
}
ROWS = 6


def render(text: str) -> str:
    missing = sorted({c for c in text.upper() if c not in GLYPHS})
    if missing:
        sys.exit(f"No glyph for: {missing}. Add it to GLYPHS.")
    rows = []
    for r in range(ROWS):
        rows.append(''.join(GLYPHS[c][r] for c in text.upper()))
    return '\n'.join(rows)


def swap(html: str, cls: str, art: str) -> tuple[str, bool]:
    pattern = re.compile(rf'(<pre class="{cls}">).*?(</pre>)', re.S)
    if not pattern.search(html):
        return html, False
    return pattern.sub(lambda m: m.group(1) + art + m.group(2), html, count=1), True


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    html = open(path, encoding='utf-8').read()

    html, a = swap(html, 'ascii-art', render(NAME))
    html, b = swap(html, 'footer-ascii-art', render(FOOTER))

    open(path, 'w', encoding='utf-8').write(html)
    print(f"header wordmark: {'replaced' if a else 'NOT FOUND'}  ({NAME})")
    print(f"footer wordmark: {'replaced' if b else 'NOT FOUND'}  ({FOOTER})")
    print()
    print(render(NAME))


if __name__ == '__main__':
    main()
