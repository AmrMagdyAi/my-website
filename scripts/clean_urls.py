#!/usr/bin/env python3
"""Show page addresses without .html (amrmagdy.com/blog, not /blog.html).

GitHub Pages serves both /blog and /blog.html, so the files keep their names. This rewrites every internal
link, canonical, og:url, JSON-LD url, sitemap entry and share link to the clean address, and puts a tiny script
at the top of each page's <head> that cleans the address bar for visitors who arrive on an old .html link.
Safe to rerun (nothing left to change). Run it LAST, after guide_look.py, add_ask_cta.py and build_llms_full.py,
because those emit .html links. External links (developer.salesforce.com/....html) are left alone.
Usage: python3 scripts/clean_urls.py"""
import glob, re

SITE = r'(https?(?::|%3A)//amrmagdy\.com/)'
BAR = ("<script>if(/\\.html$/.test(location.pathname))try{history.replaceState(null,'',"
       "location.pathname.replace(/(^|\\/)index\\.html$/,'$1').replace(/\\.html$/,'')+location.search+location.hash)}catch(e){}</script>")
NO_BAR = {'404.html'}  # served at any missing path, so it must keep the address it was asked for

def clean(s):
    s = re.sub(SITE + r'index\.html', r'\1', s)
    s = re.sub(SITE + r'([a-z0-9][a-z0-9-]*)\.html(?![A-Za-z0-9_-])', r'\1\2', s)
    def attr(m):
        a, q, slash, name, frag = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or ''
        if name == 'index':
            return f'{a}={q}{"/" if slash else "./"}{frag}{q}'
        return f'{a}={q}{slash}{name}{frag}{q}'
    s = re.sub(r'\b(href|action)=(["\'])(/?)([a-z0-9][a-z0-9-]*)\.html(#[^"\']*)?\2', attr, s)
    return s

changed = 0
for p in sorted(glob.glob('*.html')) + ['sitemap.xml', 'llms.txt', 'llms-full.txt', 'booking.js', 'assets/consent.js']:
    s = open(p, encoding='utf-8').read()
    t = clean(s)
    if p.endswith('.html') and p not in NO_BAR and BAR not in t and '<head>' in t:
        t = t.replace('<head>', '<head>\n' + BAR, 1)
    if t != s:
        open(p, 'w', encoding='utf-8').write(t); changed += 1
print(changed, 'files changed')
