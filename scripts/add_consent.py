#!/usr/bin/env python3
"""Give every tracked page the cookie choice: Google consent defaults (off for the EEA, the UK and Switzerland until the
visitor accepts, plus their saved choice) in the inline gtag snippet, assets/consent.js right after it, and a Privacy link
in the footer. Run it after adding pages. Pages already done are skipped. Usage: python3 scripts/add_consent.py"""
import glob, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
REGIONS = "'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'"
CONSENT = ("gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',region:[" + REGIONS + "]});"
           "try{(function(c){if(c==='granted'||c==='denied')gtag('consent','update',{analytics_storage:c});})(localStorage.getItem('ga_consent'));}catch(e){}")
GTAG = "function gtag(){dataLayer.push(arguments);}"
BASE = '<span>© <span data-year>2026</span> Amr Magdy · Salesforce CRM Consultant</span>'

changed = []
for p in sorted(glob.glob('*.html')):
    s = orig = open(p, encoding='utf-8').read()
    if 'G-66PK4JKWSF' not in s or 'http-equiv="refresh"' in s:
        continue
    root = '/' if p == '404.html' else ''  # the 404 page is served at any missing path, so it needs root paths
    if "gtag('consent','default'" not in s:
        if s.count(GTAG + "gtag('js',new Date());") != 1:
            sys.exit(f'{p}: expected one inline gtag snippet')
        s = s.replace(GTAG + "gtag('js',new Date());", GTAG + CONSENT + "gtag('js',new Date());")
    if 'assets/consent.js' not in s:
        m = re.search(r"<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\).*?</script>", s)
        s = s[:m.end()] + f'\n<script src="{root}assets/consent.js" defer></script>' + s[m.end():]
    if 'privacy.html">Privacy</a>' not in s and p != 'privacy.html':
        if BASE in s:      # Before & After footer
            s = s.replace(BASE, BASE[:-7] + ' · <a href="privacy.html">Privacy</a></span>')
        elif '<div class="fl">' in s:   # older footer: last link in the row
            s = re.sub(r'(<div class="fl">.*?)(</div>)', lambda m: m.group(1) + f'<a href="{root}privacy.html">Privacy</a>' + m.group(2), s, count=1)
        else:
            print(f'{p}: no known footer, add the Privacy link by hand')
    if s != orig:
        open(p, 'w', encoding='utf-8').write(s)
        changed.append(p)
print(f'updated {len(changed)} pages' + (': ' + ', '.join(changed) if changed else ', all already had it'))
