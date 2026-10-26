#!/usr/bin/env python3
"""Give the pages on styles.css (guides, tools, blog) the main site's look and chrome. Safe to rerun.
For each page that links styles.css:
- header: the main site's header (About, Services, Proof, Free tools, Revenue Audit, dark mode, Book a free call, phone menu)
- footer: the main site's footer
- phone bar: the main site's "$1,500 audit / Book a free call" bar, except where the page has its own bottom bar
- the page's own <style>: the old fonts and the hard-coded navy, blue, gold and red become the main site's tokens
- the dark call-to-action boxes' inline colors, the same
- the old dark-mode script becomes assets/chrome.js, and theme-color matches the main site
- the old font links (Google Fonts, assets/fonts/fonts.css) go, because styles.css declares the fonts
After it, run scripts/add_ask_cta.py (the "Ask me" strip) and scripts/build_llms_full.py.
Usage: python3 scripts/guide_look.py [page.html ...]   (no arguments: every page on styles.css)"""
import glob, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

BOOK = 'https://calendly.com/amr-magdy-crm/30min'
MENU = [('about.html', 'About'), ('./#services', 'Services'), ('./#cases', 'Proof'),
        ('resources.html', 'Free tools'), ('crm-revenue-audit.html', 'Revenue Audit')]
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
FOOT = [
    ('f1', 'Work with me', [('crm-revenue-audit.html', 'CRM Revenue Audit'), ('sample-audit-report.html', 'Sample audit report'),
                            ('move-to-salesforce.html', 'Move to Salesforce'), ('salesforce-admin-real-estate-investors.html', 'Admin or retainer?'),
                            ('salesforce-health-check.html', 'Free health check')]),
    ('f2', 'Free tools', [('deal-leak-score.html', 'Deal Leak Score'), ('wholesaling-cost-per-deal-calculator.html', 'Cost per deal calculator'),
                          ('wholesaling-mao-calculator.html', 'MAO calculator'), ('kept-deal-map.html', 'Kept-Deal Map'),
                          ('resources.html', 'All free tools')]),
    ('f3', 'Learn', [('real-estate-crm-guide.html', 'Real estate CRM guide'), ('salesforce-vs-investor-crms.html', 'Salesforce vs investor CRMs'),
                     ('podio-alternative-wholesalers.html', 'Moving off Podio'), ('videos.html', 'Videos'), ('blog.html', 'Blog')]),
]


def cur(page, href):
    return ' aria-current="page"' if href == page else ''


def header(page):
    links = '\n'.join(f'    <a href="{h}"{cur(page, h)}>{t}</a>' for h, t in MENU)
    return f'''<header class="top"><div class="wrap">
  <a class="brand" href="./"><b>Amr Magdy</b><span>Salesforce CRM Consultant</span></a>
  <nav class="nav" id="nav" aria-label="Main">
{links}
    <a class="btn nav-cta" href="{BOOK}" target="_blank" rel="noopener" data-book>Book a free 30-min call</a>
  </nav>
  <div class="top-act">
    <button class="icon-btn theme" id="theme-toggle" type="button" aria-label="Dark mode" aria-pressed="false">
      {MOON}
      {SUN}
    </button>
    <a class="btn sm ghost" href="{BOOK}" target="_blank" rel="noopener" data-book>Book a free call</a>
    <button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span class="bars" aria-hidden="true"></span><span class="txt">Menu</span></button>
  </div>
</div></header>'''


def footer(page):
    cols = ''
    for fid, title, links in FOOT:
        items = '\n'.join(f'      <li><a href="{h}"{cur(page, h)}>{t}</a></li>' for h, t in links)
        cols += f'    <nav aria-labelledby="{fid}"><h2 id="{fid}">{title}</h2><ul>\n{items}\n    </ul></nav>\n'
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div class="foot-brand"><b>Amr Magdy</b><p>Salesforce CRM Consultant for US real estate investors, wholesalers and home-buying companies.</p></div>
{cols}    <nav aria-labelledby="f4"><h2 id="f4">Contact</h2><ul>
      <li><a href="{BOOK}" target="_blank" rel="noopener" data-book>Book a free call</a></li>
      <li><a href="mailto:info@AmrMagdy.com">info@AmrMagdy.com</a></li>
      <li><a href="https://www.linkedin.com/in/amrmagdyai/" target="_blank" rel="noopener">LinkedIn</a></li>
      <li><a href="salesforce-consultant-canada-real-estate.html"{cur(page, 'salesforce-consultant-canada-real-estate.html')}>Canada</a> · <a href="salesforce-consultant-uk-estate-agents.html"{cur(page, 'salesforce-consultant-uk-estate-agents.html')}>UK</a></li>
      <li><a href="about.html">About me</a></li>
      <li><a href="Amr_Magdy_CV.pdf" download>CV (PDF)</a></li>
    </ul></nav>
  </div>
  <div class="base"><span>© <span data-year>2026</span> Amr Magdy · Salesforce CRM Consultant · <a href="privacy.html">Privacy</a></span><span>Remote from Cairo, for teams in the US, Canada, the UK and Europe</span></div>
</div></footer>'''


def phone_bar(page):
    if page == 'move-to-salesforce.html':  # the audit is for teams already on Salesforce, so this page offers the call only
        links = f'<a class="f" href="{BOOK}" target="_blank" rel="noopener" data-book>Book a free scoping call</a>'
    else:
        links = f'<a class="f" href="crm-revenue-audit.html">$1,500 audit</a><a class="g" href="{BOOK}" target="_blank" rel="noopener" data-book>Book a free call</a>'
    return f'<div class="mcta" id="mcta" data-stop=".cta,.article-cta,.ask-cta,.foot">{links}</div>'


# ── the page's own <style> ──
LEGACY_NAV_CSS = [  # the old header's own rules; the header is gone
    'nav .nb,.logo{white-space:nowrap}\n',
    '@media(max-width:520px){nav .nb{padding:7px 11px;font-size:.78rem}.logo{font-size:.98rem;gap:7px}.logo-mark{width:30px;height:30px}.nav-in{gap:7px}nav .nb.hide-sm{display:none}nav .nb.nb-call{margin-left:auto!important}}\n',
]
DARK_BOX = re.compile(r'^\s*(\.cta|\.mbar|\.price-card|\.cnt \.hi|\.req|\.res)(?![\w-])')  # inside boxes on var(--navy), now var(--band)
ON_BAND = {'#dbe4f0', '#c9d4e3', '#c9d5e4', '#dfe7f2', '#b9c6d8', '#9fb0c6'}  # the old light text on navy


def rule(sel, body):
    dark = 'var(--navy)' in body or DARK_BOX.match(sel)
    body = re.sub(r"""font-family:\s*'?Fraunces'?\s*,\s*Georgia\s*,\s*serif""", 'font-family:var(--f-head)', body)
    body = re.sub(r"""font-family:\s*'Plus Jakarta Sans'\s*,\s*(sans-serif|system-ui)""", 'font-family:var(--f-body)', body)
    last = re.split(r'[\s>+~]+', sel.split(',')[-1].strip())[-1]
    if 'var(--f-head)' in body or (re.match(r'h[1-4](\b|$)', last) and 'f-body' not in body and 'font:' not in body):
        body = re.sub(r'font-weight:\s*[5-9]00', 'font-weight:400', body)  # DM Serif Display has one weight

    def color(m):
        prop, val = m.group(1), m.group(2).lower()
        if val == '#fff':
            return f'{prop}:var(--band-ink)' if dark else f'{prop}:var(--on-accent)'
        if val in ON_BAND:
            return f'{prop}:var(--band-ink2)'
        if val == '#c0392b':
            return f'{prop}:var(--rose-ink)' if prop == 'color' else f'{prop}:var(--rose)'
        if val == '#0b6bce':
            return f'{prop}:var(--sf)'
        if val == '#d4a23e':
            return f'{prop}:var(--band-ink)' if prop == 'fill' else f'{prop}:var(--teal)'
        return m.group(0)
    body = re.sub(r'(color|background|background-color|border-color|fill)\s*:\s*(#[0-9a-fA-F]{3,6})\b(?![0-9a-fA-F])', color, body)
    body = re.sub(r'(border(?:-left|-top)?\s*:\s*[^;{}]*?)#c0392b', r'\1var(--rose)', body)
    body = re.sub(r'(border(?:-left|-top)?\s*:\s*[^;{}]*?)#d4a23e', r'\1var(--teal)', body)
    for old, new in [('rgba(11,107,206,.25)', 'var(--line2)'), ('rgba(11,107,206,.18)', 'var(--line)'),
                     ('rgba(11,107,206,.07)', 'var(--teal-soft)'), ('#1287e8', 'var(--teal)'),
                     ('#0b1628', 'var(--band)'), ('#8a5a00', 'var(--rose-ink)')]:
        body = body.replace(old, new)
    return sel + '{' + body + '}'


def restyle(css):
    for legacy in LEGACY_NAV_CSS:
        css = css.replace(legacy, '')
    # the calculators' bottom bar needs room under the footer, whichever footer markup the page has
    css = css.replace('footer{padding-bottom:70px}', 'footer,.foot{padding-bottom:70px}')
    return re.sub(r'([^{}]+)\{([^{}]*)\}', lambda m: rule(m.group(1), m.group(2)), css)


# ── inline style="" colors on the dark call-to-action boxes (the "Ask me" strip has its own script) ──
def attrs(s):
    def fix(m):
        a = m.group(0)
        a = a.replace('color:#c9d4e3', 'color:var(--band-ink2)').replace('color:#d4a23e', 'color:var(--band-ink)')
        return re.sub(r'(border(?:-left|-top)?:[^;"]*?)#d4a23e', r'\1var(--teal)', a)
    s = re.sub(r'style="[^"]*"', fix, s)
    # charts drawn in SVG name their font in an attribute
    return s.replace('font-family="Plus Jakarta Sans,', 'font-family="DM Sans,').replace('font-family="Fraunces,', 'font-family="DM Serif Display,')


OLD_THEME_JS = re.compile(r"<script>\s*\(function\(\)\{var r=document\.documentElement,b=document\.getElementById\('theme-toggle'\);.*?\}\)\(\);\s*</script>", re.S)
OLD_NAV = re.compile(r'<nav>\s*(?:<div class="wrap-wide">)?\s*<div class="nav-in">.*?</nav>', re.S)
# wholesaling-cost-per-deal-calculator.html lost its <nav> opening and logo: only the links, the dark-mode button and the closing tags are left
HEADLESS_NAV = re.compile(r'(?<=<body>\n)(?:[ \t]*<a [^>]*class="nb[^"]*"[^>]*>[^<]*</a>\n)+<button class="theme-toggle".*?</div></div></nav>', re.S)
OLD_FOOT = re.compile(r'<footer>.*?</footer>', re.S)
FONT_LINKS = re.compile(r'[ \t]*(?:<link rel="preload" as="style" href="assets/fonts/fonts(?:-italic-500)?\.css"[^>]*>|'
                        r'<noscript><link rel="stylesheet" href="assets/fonts/fonts(?:-italic-500)?\.css"></noscript>|'
                        r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"(?: crossorigin)?>|'
                        r'<link[^>]*href="https://fonts\.googleapis\.com/[^"]*"[^>]*>)\n?')


def page(p):
    s = orig = open(p, encoding='utf-8').read()
    s = FONT_LINKS.sub('', s)
    s = s.replace('<meta name="theme-color" content="#f7f4ee">', '<meta name="theme-color" content="#f7f4ef">')
    s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + restyle(m.group(2)) + m.group(3), s, flags=re.S)
    s = attrs(s)
    if '<header class="top">' not in s:
        s = OLD_NAV.sub(lambda m: header(p), s, count=1)
    if '<header class="top">' not in s:
        s = HEADLESS_NAV.sub(lambda m: header(p), s, count=1)
    if '<footer class="foot">' not in s:
        s = OLD_FOOT.sub(lambda m: footer(p), s, count=1)
    has_bar = 'class="mbar"' in s or 'id="res"' in s or p == '404.html'  # a calculator's own bottom bar, or the score's sticky result
    if 'id="mcta"' not in s and not has_bar:
        s = s.replace('</footer>', '</footer>\n\n' + phone_bar(p), 1)
    if 'assets/chrome.js' not in s:
        s, n = OLD_THEME_JS.subn('<script src="assets/chrome.js" defer></script>', s, count=1)
        if not n:
            s = s.replace('</body>', '<script src="assets/chrome.js" defer></script>\n</body>', 1)
    if s != orig:
        open(p, 'w', encoding='utf-8').write(s)
        return True
    return False


# book.html is the brand thread's stop page for LinkedIn Featured: its own inline look, no header or footer
SKIP = {'book.html'}
pages = sys.argv[1:] or [p for p in sorted(glob.glob('*.html')) if p not in SKIP and '<link rel="stylesheet" href="styles.css">' in open(p, encoding='utf-8').read()]
changed = [p for p in pages if page(p)]
print(f'updated {len(changed)} of {len(pages)} pages')
left = [p for p in pages if re.search(r"Fraunces|Plus Jakarta|#0b1f3a|#d4a23e|#0b6bce|#c0392b", open(p, encoding='utf-8').read())]
if left:
    print('old fonts or colors still in:', ', '.join(left))
