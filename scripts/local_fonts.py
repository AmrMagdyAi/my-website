#!/usr/bin/env python3
"""Serve Fraunces and Plus Jakarta Sans from this site instead of Google Fonts on the pages that use styles.css.
Points each Google Fonts stylesheet tag at the copy in assets/fonts/ that has the same faces, so pages look the same and
load the same way (it doesn't hold up the first paint, and the noscript copy covers no-JS visitors), and drops the
preconnects to Google. Run it after adding pages. Pages already done are skipped. Usage: python3 scripts/local_fonts.py"""
import glob, os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
PRECONNECT = re.compile(r'[ \t]*<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"( crossorigin)?>\n')
GOOGLE_CSS = re.compile(r'https://fonts\.googleapis\.com/css2\?[^"]*')
STANDARD = {('Fraunces', '0', w) for w in ('400', '500', '600')} | {('Fraunces', '1', '400')} | \
           {('Plus Jakarta Sans', '0', w) for w in ('400', '500', '600', '700')}
COPIES = [('assets/fonts/fonts.css', STANDARD), ('assets/fonts/fonts-italic-500.css', STANDARD | {('Fraunces', '1', '500')})]

def faces(url):
    """The (family, italic, weight) faces a css2 URL asks for, e.g. family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400"""
    out = set()
    for fam in re.findall(r'family=([^&]+)', url.replace('&amp;', '&')):
        name, _, spec = fam.partition(':')
        axes, _, tuples = spec.partition('@')
        for t in tuples.split(';'):
            v = dict(zip(axes.split(','), t.split(',')))
            out.add((name.replace('+', ' '), v.get('ital', '0'), v.get('wght', '400')))
    return out

def local(m):
    want = faces(m.group(0))
    return next((path for path, has in COPIES if want <= has), m.group(0))  # no copy has them all: leave it, reported below

changed = []
for p in sorted(glob.glob('*.html')):
    s = orig = open(p, encoding='utf-8').read()
    if '<link rel="stylesheet" href="styles.css">' not in s:
        continue
    s = GOOGLE_CSS.sub(local, PRECONNECT.sub('', s))
    if p == '404.html' and '<base href="/">' not in s:  # served at any missing path, so relative links resolve from the root
        s = s.replace('<head>\n', '<head>\n<base href="/">\n', 1)
    if 'fonts.googleapis.com' in s or 'fonts.gstatic.com' in s:
        print(f'{p}: Google Fonts reference left (a family or weight assets/fonts/ lacks), check it by hand')
    if s != orig:
        open(p, 'w', encoding='utf-8').write(s)
        changed.append(p)
print(f'updated {len(changed)} pages' + ('' if changed else ', all already done'))
