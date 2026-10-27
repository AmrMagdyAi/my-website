#!/usr/bin/env python3
"""Dark header band for the guide pages: the eyebrow and title sit on the dark band (rose and teal glows, dot texture, rose|teal bar),
with the guide's own picture (a paper tile with an icon and a coloured badge, the same object as its share image) on the right.
Pages without a share-image object get the band without the picture. Body, short answer and everything below stay light.
Tools, the audit page, About and the sample report are not touched. Safe to rerun (a page that already has the band is skipped).
Usage: python3 scripts/guide_band.py [page.html ...]   (no arguments: every guide in GUIDES)
CSS: styles.css (.band-h). Picture data: scripts/guide_band_data.json (icon paths + badge colour per page, from the share-image list)."""
import json, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

D = json.load(open('scripts/guide_band_data.json'))
ICONS, PAGES = D['icons'], D['pages']

# the guides on the Guides page (blog.html); tools stay light
GUIDES = set(re.findall(r'<a href="([a-z0-9-]+)\.html" class="ac">', open('blog.html', encoding='utf-8').read()))


def svg(name):
    return f'<svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{ICONS[name]}</svg>'


def obj(slug):
    if slug not in PAGES:
        return ''
    main, badge, col = PAGES[slug]
    return f'<div class="obj {col}" aria-hidden="true"><div class="tile">{svg(main)}</div><div class="bdg">{svg(badge)}</div></div>'


HEAD = re.compile(r'(<main class="pg"><div class="pg-w">(?:\s*<style>.*?</style>)?\s*)(<span class="eyebrow">.*?</span>\s*<h1[^>]*>.*?</h1>)', re.S)


def band(slug, s):
    if 'class="band-h' in s:
        return s, 'skip'
    m = HEAD.search(s)
    if not m:
        return s, 'no-match'
    o = obj(slug)
    cls = 'band-h' + ('' if o else ' noobj')
    return s[:m.start(2)] + f'<div class="{cls}"><div>{m.group(2)}</div>{o}</div>' + s[m.end(2):], 'ok' if o else 'ok-noobj'


if __name__ == '__main__':
    pages = sys.argv[1:] or sorted(g + '.html' for g in GUIDES)
    res = {}
    for p in pages:
        s = open(p, encoding='utf-8').read()
        n, k = band(p[:-5], s)
        res.setdefault(k, []).append(p)
        if n != s:
            open(p, 'w', encoding='utf-8').write(n)
    for k, v in res.items():
        print(k, len(v), v if k in ('no-match',) else '')
