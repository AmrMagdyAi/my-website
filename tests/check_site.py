"""Static checks for amrmagdy.com. Run: python3 tests/check_site.py (exits 1 on any failure)."""
import glob, json, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
errs = []
def fail(m): errs.append(m)
pages = sorted(glob.glob('*.html'))
def read(p): return open(p, encoding='utf-8').read()
def is_stub(h): return 'http-equiv="refresh"' in h or 'location.replace' in h and '<h1' not in h
indexable = [p for p in pages if p not in ('404.html', 'theme-check.html') and 'content="noindex' not in read(p) and not is_stub(read(p))]

# 1 sitemap lists every indexable page and no missing file
sm = read('sitemap.xml')
locs = re.findall(r'<loc>https://amrmagdy\.com/?([^<]*)</loc>', sm)
for p in indexable:
    slug = '' if p == 'index.html' else p[:-5]
    if slug not in locs: fail(f'sitemap missing {p}')
for l in locs:
    f = 'index.html' if l == '' else l + '.html'
    if not os.path.exists(f) and not os.path.exists(l): fail(f'sitemap url without file: {l}')

# 2 every JSON-LD block parses; every indexable page has title, description, canonical
for p in indexable:
    h = read(p)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(b)
        except Exception as e: fail(f'{p}: bad JSON-LD ({e})')
    for pat, name in ((r'<title>.+?</title>', 'title'), (r'<meta name="description" content="[^"]+"', 'description'), (r'<link rel="canonical" href="[^"]+"', 'canonical')):
        if not re.search(pat, h, re.S): fail(f'{p}: missing {name}')

# 3 writing rules: nothing the project forbids may ship in site text
banned = [r'certified architect', r'4x certified', r'Left Main', r'Central City', r'Grabow', r'Pezon', r'Sylndr', r'Conx Digital']
for p in pages + ['llms.txt']:
    h = read(p)
    h2 = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S) if p.endswith('.html') else h
    for b in banned:
        if re.search(b, h2, re.I): fail(f'{p}: banned text {b!r}')

# 4 accessibility wiring the homepage depends on
idx = read('index.html')
for i in ('sw-live', 'pick-live'):
    if f'id="{i}"' not in idx: fail(f'index.html: missing #{i}')
if 'aria-live="polite">\n      <div class="pane"' in idx: fail('index.html: picker panel announces whole pane')
for p in ('about.html', 'index.html'):
    if 'assets/consent.js' not in read(p): fail(f'{p}: consent.js not loaded')

# 5 privacy truth: no first-party cookie is written (privacy.html says only GA cookies)
for js in glob.glob('assets/*.js'):
    if re.search(r"document\.cookie\s*=\s*'theme='\s*\+", read(js)): fail(f'{js}: writes a theme cookie')

# 6 every target=_blank link has noopener
for p in pages:
    for m in re.findall(r'<a [^>]*target="_blank"[^>]*>', read(p)):
        if 'noopener' not in m: fail(f'{p}: _blank without noopener')

# 7 the booking script has its own test
import subprocess
r = subprocess.run(['node', 'tests/booking.test.js'], capture_output=True, text=True)
if r.returncode: fail('booking.test.js failed: ' + (r.stderr or r.stdout)[-300:])

if errs:
    print('\n'.join(errs[:60])); print(f'{len(errs)} problem(s)'); sys.exit(1)
print(f'ok: {len(pages)} pages, {len(indexable)} indexable')
