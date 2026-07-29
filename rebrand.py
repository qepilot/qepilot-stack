#!/usr/bin/env python3
"""Rebrand this fork as QEPilot Stack.

Deliberately NOT touched:
  * LICENSE            — MIT requires the copyright notice be retained.
  * claude-code-templates (hyphenated) — the npm package name; renaming it
                         breaks `npx claude-code-templates`.
  * Live API endpoints — rewriting these to a domain that serves nothing
                         would break the app. They are handled separately
                         and routed through a single origin constant.

Idempotent: safe to run twice.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'.git', 'node_modules', '.venv', '__pycache__', 'dist', 'build', '.next'}
SKIP_FILES = {'LICENSE', 'LICENSE.txt', 'rebrand.py'}
BINARY_EXT = {'.png','.jpg','.jpeg','.gif','.ico','.woff','.woff2','.ttf','.eot',
              '.zip','.gz','.pdf','.mp4','.webp','.lock'}

# Endpoints that must keep resolving. Left alone by the bulk pass.
FUNCTIONAL = [
    'aitmpl.com/api/',
    'aitmpl.com/components.json',
    'aitmpl-newsletter',
]

REPLACEMENTS = [
    ('https://www.aitmpl.com', 'https://stack.qapilot.live'),
    ('https://app.aitmpl.com', 'https://app.qapilot.live'),
    ('https://docs.aitmpl.com', 'https://docs.qapilot.live'),
    ('https://aitmpl.com',     'https://stack.qapilot.live'),
    ('www.aitmpl.com',         'stack.qapilot.live'),
    ('app.aitmpl.com',         'app.qapilot.live'),
    ('docs.aitmpl.com',        'docs.qapilot.live'),
    ('aitmpl.com',             'stack.qapilot.live'),
    ('Claude Code Templates',  'QEPilot Stack'),
    ('AI Templates',           'QEPilot Stack'),
    ('aitmpl',                 'qepilot-stack'),
]


def protected(line: str) -> bool:
    return any(f in line for f in FUNCTIONAL)


def main():
    changed, edits = 0, 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES:
                continue
            if os.path.splitext(name)[1].lower() in BINARY_EXT:
                continue
            path = os.path.join(root, name)
            try:
                original = open(path, encoding='utf-8').read()
            except (OSError, UnicodeDecodeError):
                continue
            if 'aitmpl' not in original and 'Claude Code Templates' not in original \
               and 'AI Templates' not in original:
                continue

            out, hits = [], 0
            for line in original.split('\n'):
                if protected(line):
                    out.append(line)
                    continue
                new = line
                for old, repl in REPLACEMENTS:
                    if old in new:
                        new = new.replace(old, repl)
                if new != line:
                    hits += 1
                out.append(new)

            result = '\n'.join(out)
            if result != original:
                open(path, 'w', encoding='utf-8').write(result)
                changed += 1
                edits += hits
                print(f'  {os.path.relpath(path, ROOT)}  ({hits} lines)')

    print(f'\n{changed} files rewritten, {edits} lines changed')

    # Report what deliberately survives.
    survivors = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1].lower() in BINARY_EXT:
                continue
            path = os.path.join(root, name)
            try:
                txt = open(path, encoding='utf-8').read()
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(txt.split('\n'), 1):
                if 'aitmpl' in line:
                    survivors.append(f'{os.path.relpath(path, ROOT)}:{i}')
    print(f'\nremaining aitmpl references (intentional): {len(survivors)}')
    for s in survivors:
        print('   ', s)


if __name__ == '__main__':
    main()
