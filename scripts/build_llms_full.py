#!/usr/bin/env python3
"""Rebuild llms-full.txt: plain text of every indexable page, homepage first."""
import glob, os, re, datetime
from bs4 import BeautifulSoup
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
pages = [p for p in sorted(glob.glob('*.html')) if p not in ('404.html','theme-check.html') and 'http-equiv="refresh"' not in open(p).read()]
pages.remove('index.html'); pages.insert(0, 'index.html')
out = ['# Amr Magdy — full text of key pages (llms-full.txt)',
       '> Plain-text copy of the main content of amrmagdy.com for AI assistants and answer engines.',
       '> Short profile: https://amrmagdy.com/llms.txt',
       f'> Generated: {datetime.date.today().isoformat()}', '']
BLOCK = ['h1','h2','h3','h4','p','li','dt','dd','td','th','figcaption','blockquote','summary','div.formula','pre']
for p in pages:
    soup = BeautifulSoup(open(p).read(), 'html.parser')
    title = soup.title.get_text(strip=True) if soup.title else p
    root = soup.find('main') or soup.body
    for t in root.find_all(['script','style','nav','svg','noscript','form','button','video']): t.decompose()
    # leave out what the page hides until a script shows it, such as the parked $750 deposit lines (data-deposit-only)
    for t in root.find_all(lambda t: t.has_attr('hidden') or re.search(r'display\s*:\s*none', t.get('style') or '')):
        if not t.decomposed: t.decompose()
    lines = []
    for el in root.select('h1,h2,h3,h4,p,li,tr,dt,dd,figcaption,blockquote,summary,pre,div.formula'):
        if el.find_parent(['p','li','tr','dd','blockquote','pre']) or (el.name!='div' and el.find_parent('div', class_='formula')): continue
        if el.name == 'tr':
            txt = ' | '.join(re.sub(r'\s+', ' ', c.get_text(' ', strip=True)) for c in el.find_all(['td','th']))
        else:
            txt = re.sub(r'[ \t]+', ' ', el.get_text('\n' if el.name in ('div','pre') else ' ', strip=True)).strip()
        if txt and (not lines or lines[-1] != txt): lines.append(txt)
    url = 'https://amrmagdy.com/' if p == 'index.html' else f'https://amrmagdy.com/{p[:-5]}'
    out += ['', '---', f'## {title}', f'URL: {url}', ''] + lines
open('llms-full.txt', 'w').write('\n'.join(out) + '\n')
print(len(pages), 'pages', os.path.getsize('llms-full.txt'), 'bytes')
