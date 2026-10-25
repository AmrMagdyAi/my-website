#!/usr/bin/env python3
"""Copy the visible FAQ (<details><summary>Q</summary><p>A</p></details>) into the page's FAQPage JSON-LD,
so the structured data always matches what visitors see. Usage: python3 scripts/sync_faq_schema.py index.html crm-revenue-audit.html"""
import html, json, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

def text(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()

def faqs(page):
    m = re.search(r'<section[^>]*id="faq".*?</section>', page, re.S)
    if not m:
        return []
    pairs = re.findall(r'<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', m.group(0), re.S)
    return [{"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}} for q, a in pairs]

def fill(node, entities):
    hits = 0
    if isinstance(node, dict):
        if node.get('@type') == 'FAQPage':
            node['mainEntity'] = entities
            hits += 1
        for v in node.values():
            hits += fill(v, entities)
    elif isinstance(node, list):
        for v in node:
            hits += fill(v, entities)
    return hits

for path in sys.argv[1:]:
    page = open(path, encoding='utf-8').read()
    entities = faqs(page)
    def swap(m):
        data = json.loads(m.group(2))
        if not fill(data, entities):
            return m.group(0)
        return m.group(1) + '\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n' + m.group(3)
    new = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', swap, page, flags=re.S)
    open(path, 'w', encoding='utf-8').write(new)
    print(f'{path}: {len(entities)} questions')
