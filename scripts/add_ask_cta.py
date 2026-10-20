#!/usr/bin/env python3
"""Insert (or refresh) the 'Ask Amr' conversation strip before the footer on every content page."""
import glob, html, os, re, urllib.parse
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
START, END = '<!-- ask-cta:start -->', '<!-- ask-cta:end -->'
ISTART, IEND = '<!-- ask-inline:start -->', '<!-- ask-inline:end -->'
SKIP = {'index.html', '404.html'}

def block(page, h1):
    topic = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h1))).strip().rstrip('.')
    short = topic if len(topic) <= 70 else topic[:67].rsplit(' ', 1)[0] + '...'
    url = f'https://amrmagdy.com/{page}'
    subj = urllib.parse.quote(f'Question about: {short}')
    body = urllib.parse.quote(f'Hi Amr,\n\nI read {url} and have a question about our setup:\n\n')
    wa = urllib.parse.quote(f'Hi Amr, I read your page "{short}" and have a question: ')
    ev = "if(window.gtag)gtag('event','contact_click',{method:'%s',page_path:location.pathname})"
    return f'''{START}
<section class="ask-cta" aria-label="Ask a question" style="max-width:860px;margin:44px auto 0;padding:0 20px">
<div style="background:#0b1f3a;color:#fff;border-radius:16px;padding:26px 26px 24px;border-top:4px solid #d4a23e">
<p style="margin:0 0 6px;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:#d4a23e;font-weight:700">Found this useful?</p>
<h2 style="margin:0 0 8px;color:#fff;font-size:1.45rem;line-height:1.25">Ask me how this would work in your CRM.</h2>
<p style="margin:0 0 18px;color:#c9d4e3;line-height:1.55">Send one question about your setup, whether you're on Podio, an investor CRM, spreadsheets or Salesforce. No pitch, just a straight answer.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px">
<a href="mailto:info@amrmagdy.com?subject={subj}&amp;body={body}" onclick="{ev % 'email'}" style="background:#d4a23e;color:#0b1f3a;font-weight:700;text-decoration:none;padding:11px 18px;border-radius:999px">Email a question</a>
<a href="https://wa.me/201033275250?text={wa}" target="_blank" rel="noopener" onclick="{ev % 'whatsapp'}" style="background:#fff;color:#0b1f3a;font-weight:700;text-decoration:none;padding:11px 18px;border-radius:999px">WhatsApp</a>
<a href="https://www.linkedin.com/in/amrmagdyai/" target="_blank" rel="noopener" onclick="{ev % 'linkedin'}" style="background:transparent;color:#fff;font-weight:700;text-decoration:none;padding:10px 17px;border-radius:999px;border:1.5px solid #5d7393">Message on LinkedIn</a>
<a href="index.html#contact" onclick="{ev % 'call_request'}" style="background:transparent;color:#fff;font-weight:700;text-decoration:none;padding:10px 17px;border-radius:999px;border:1.5px solid #5d7393">Request a free call</a>
</div></div></section>
{END}
'''

def inline(page, h1):
    topic = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h1))).strip().rstrip('.')
    short = topic if len(topic) <= 70 else topic[:67].rsplit(' ', 1)[0] + '...'
    url = f'https://amrmagdy.com/{page}'
    subj = urllib.parse.quote(f'Question about: {short}')
    body = urllib.parse.quote(f'Hi Amr,\n\nI read {url} and have a question about our setup:\n\n')
    wa = urllib.parse.quote(f'Hi Amr, I read your page "{short}" and have a question: ')
    ev = "if(window.gtag)gtag('event','contact_click',{method:'%s',page_path:location.pathname})"
    st = 'color:#d4a23e;font-weight:700;text-decoration:underline'
    return (f'{ISTART}<p style="margin:16px 0 0;font-size:.95rem;color:#c9d4e3">Or just ask one question about your setup: '
            f'<a href="mailto:info@amrmagdy.com?subject={subj}&amp;body={body}" onclick="{ev % "email"}" style="{st}">email</a> · '
            f'<a href="https://wa.me/201033275250?text={wa}" target="_blank" rel="noopener" onclick="{ev % "whatsapp"}" style="{st}">WhatsApp</a> · '
            f'<a href="https://www.linkedin.com/in/amrmagdyai/" target="_blank" rel="noopener" onclick="{ev % "linkedin"}" style="{st}">LinkedIn</a></p>{IEND}')

n = 0
for p in sorted(glob.glob('*.html')):
    s = open(p).read()
    if p in SKIP or 'http-equiv="refresh"' in s: continue
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
