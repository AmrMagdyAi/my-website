#!/usr/bin/env python3
"""Insert (or refresh) the 'Ask Amr' conversation strip before the footer on every guide, tool and blog page (the pages on styles.css).
Run it after scripts/guide_look.py."""
import glob, html, os, re, urllib.parse
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
START, END = '<!-- ask-cta:start -->', '<!-- ask-cta:end -->'
ISTART, IEND = '<!-- ask-inline:start -->', '<!-- ask-inline:end -->'
# the audit terms and sample report: their buttons sit on the page, not in a dark box, and they have the audit's own calls to action;
# book.html is the LinkedIn Featured stop page, with its own look
SKIP = {'404.html', 'crm-revenue-audit-terms.html', 'sample-audit-report.html', 'book.html'}
# the main site's look (assets/site.css): teal for the main action, outlined for the rest, on the dark band
BTN = 'background:var(--teal);color:var(--on-accent);font-weight:600;text-decoration:none;padding:10px 20px;border-radius:999px;border:2px solid var(--teal)'
GHOST = 'background:transparent;color:var(--band-ink);font-weight:600;text-decoration:none;padding:10px 20px;border-radius:999px;border:2px solid var(--band-line)'

def block(page, h1):
    topic = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', ' ', h1)))).strip().rstrip('.')
    short = topic if len(topic) <= 70 else topic[:67].rsplit(' ', 1)[0] + '...'
    url = f'https://amrmagdy.com/{page}'
    subj = urllib.parse.quote(f'Question about: {short}')
    body = urllib.parse.quote(f'Hi Amr,\n\nI read {url} and have a question about our setup:\n\n')
    wa = urllib.parse.quote(f'Hi Amr, I read your page "{short}" and have a question: ')
    ev = "if(window.gtag)gtag('event','contact_click',{method:'%s',page_path:location.pathname})"
    return f'''{START}
<section class="ask-cta" aria-label="Ask a question" style="max-width:860px;margin:44px auto 0;padding:0 20px">
<div style="background:var(--band);color:var(--band-ink);border-radius:20px;padding:30px 28px 26px">
<p style="margin:0 0 8px;font-size:.76rem;letter-spacing:.1em;text-transform:uppercase;color:var(--band-ink2);font-weight:600">Found this useful?</p>
<h2 style="margin:0 0 8px;color:var(--band-ink);font-size:1.6rem;line-height:1.2">Ask me how this would work in your CRM.</h2>
<p style="margin:0 0 20px;color:var(--band-ink2);line-height:1.55">Send one question about your setup, whether you're on Podio, an investor CRM, spreadsheets or Salesforce. No pitch, just a straight answer.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px">
<a href="mailto:info@amrmagdy.com?subject={subj}&amp;body={body}" onclick="{ev % 'email'}" style="{BTN}">Email a question</a>
<a href="https://wa.me/201033275250?text={wa}" target="_blank" rel="noopener" onclick="{ev % 'whatsapp'}" style="{GHOST}">WhatsApp</a>
<a href="https://www.linkedin.com/in/amrmagdyai/" target="_blank" rel="noopener" onclick="{ev % 'linkedin'}" style="{GHOST}">Message on LinkedIn</a>
<a href="index.html#contact" onclick="{ev % 'call_request'}" style="{GHOST}">Request a free call</a>
</div></div></section>
{END}
'''

def inline(page, h1):
    topic = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', ' ', h1)))).strip().rstrip('.')
    short = topic if len(topic) <= 70 else topic[:67].rsplit(' ', 1)[0] + '...'
    url = f'https://amrmagdy.com/{page}'
    subj = urllib.parse.quote(f'Question about: {short}')
    body = urllib.parse.quote(f'Hi Amr,\n\nI read {url} and have a question about our setup:\n\n')
    wa = urllib.parse.quote(f'Hi Amr, I read your page "{short}" and have a question: ')
    ev = "if(window.gtag)gtag('event','contact_click',{method:'%s',page_path:location.pathname})"
    st = 'color:var(--band-ink);font-weight:700;text-decoration:underline'
    return (f'{ISTART}<p style="margin:16px 0 0;font-size:.95rem;color:var(--band-ink2)">Or just ask one question about your setup: '
            f'<a href="mailto:info@amrmagdy.com?subject={subj}&amp;body={body}" onclick="{ev % "email"}" style="{st}">email</a> · '
            f'<a href="https://wa.me/201033275250?text={wa}" target="_blank" rel="noopener" onclick="{ev % "whatsapp"}" style="{st}">WhatsApp</a> · '
            f'<a href="https://www.linkedin.com/in/amrmagdyai/" target="_blank" rel="noopener" onclick="{ev % "linkedin"}" style="{st}">LinkedIn</a></p>{IEND}')

n = 0
for p in sorted(glob.glob('*.html')):
    s = open(p).read()
    # only the guide, tool and blog pages (styles.css); the main site's pages have their own calls to action
    if p in SKIP or 'http-equiv="refresh"' in s or '<link rel="stylesheet" href="styles.css">' not in s: continue
    s = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', s, flags=re.S)
    s = re.sub(re.escape(ISTART) + r'.*?' + re.escape(IEND), '', s, flags=re.S)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h1 = m.group(1) if m else p
    if '<div class="cta">' in s:
        i = s.index('<div class="cta">'); j = s.index('</div>', i)
        s = s[:j] + inline(p, h1) + s[j:]
        open(p, 'w').write(s); n += 1
        continue
    anchor = s.find('<section aria-label="About the author"')
    if anchor < 0: anchor = s.rfind('<footer')
    s = s[:anchor] + block(p, h1) + s[anchor:]
    open(p, 'w').write(s); n += 1
print('pages', n)
