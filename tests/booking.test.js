// Run: node tests/booking.test.js. Checks booking.js turns call buttons into a same-tab link to /book (the inline calendar) and keeps campaign tags.
const fs = require('fs'), assert = require('assert');
const src = fs.readFileSync(__dirname + '/../booking.js', 'utf8');
function run(search, path, anchors, store) {
  global.window = {};
  global.location = { pathname: path, search };
  global.sessionStorage = { getItem: k => store[k] || null, setItem: (k, v) => { store[k] = v; } };
  global.document = { readyState: 'complete', addEventListener() {}, querySelectorAll: s => s.startsWith('a[href]') ? anchors : [] };
  eval(src);
}
function a(href, text, attrs = {}) {
  const o = { href, textContent: text, attrs, getAttribute(k) { return k === 'href' ? this.href : (this.attrs[k] || null); }, hasAttribute(k) { return k in this.attrs; }, removeAttribute(k) { delete this.attrs[k]; if (k === 'target') this._t = undefined; }, closest() { return null; }, addEventListener() {} };
  Object.defineProperty(o, 'target', { set(v) { o._t = v; }, get() { return o._t; } });
  return o;
}
// 1 the button text on the 44 calculator and guide pages matches
for (const t of ['Book a free 15-minute call', 'Book a free 15-min call', 'Book a free call']) {
  const x = a('./#contact', t); run('', '/dscr-calculator', [x], {});
  assert(x.href.startsWith('/book?'), t + ' not turned into the /book link: ' + x.href);
  assert(x.target !== '_blank', t + ' opens a new tab; /book must open in the same tab');
  assert(x.href.includes('utm_source=amrmagdy.com') && x.href.includes('utm_campaign=dscr_calculator'), 'default tags: ' + x.href);
}
// 2 a link that is not a call button is left alone
const y = a('./#contact', 'Send a message'); run('', '/x', [y], {});
assert.strictEqual(y.href, './#contact');
// 3 landing tags are kept and carried to a later page in the same tab
const store = {};
run('?utm_source=linkedin&utm_medium=social&utm_campaign=dec16', '/wholesaling-mao-calculator', [], store);
const z = a('./#contact', 'Book a free 15-minute call'); run('', '/climbmark', [z], store);
assert(z.href.includes('utm_source=linkedin') && z.href.includes('utm_campaign=dec16') && z.href.includes('utm_medium=social'), 'tags lost: ' + z.href);
assert(!z.href.includes('utm_source=amrmagdy.com'));
// 4 junk tags are dropped
const w = a('./#contact', 'Book a free call'); run('?utm_source=%3Cscript%3E', '/x', [w], {});
assert(w.href.includes('utm_source=amrmagdy.com'), 'junk tag kept: ' + w.href);
console.log('booking.test.js ok');
