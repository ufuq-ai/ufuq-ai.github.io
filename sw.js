/* أفق الذكاء: يعمل دون إنترنت (الموقع العام فقط).
   الصفحة: من الشبكة أولًا حتى تصل التحديثات فورًا، ومن النسخة المحفوظة إذا انقطع الإنترنت أو تأخر الرد أكثر من 4 ثوانٍ.
   الأيقونات والخطوط: من النسخة المحفوظة أولًا. ملفات التقويم cal/ لا تُحفظ لأنها تتغير مع كل تحديث.
   غيّر رقم CACHE فقط إذا غيّرت منطق هذا الملف؛ تحديثات المحتوى لا تحتاج ذلك. */
const CACHE = "ufuq-v1", FONTS = "ufuq-fonts-v1";
const CORE = ["./", "./manifest.webmanifest", "./favicon.svg", "./favicon-32.png", "./apple-touch-icon.png", "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== FONTS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

const shell = () => caches.open(CACHE).then(c => c.match("./"));
function page(req) {
  return new Promise(resolve => {
    let done = false;
    const finish = r => { if (!done && r) { done = true; resolve(r); } };
    const slow = setTimeout(() => shell().then(finish), 4000);
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put("./", copy)); }
      clearTimeout(slow); finish(res);
    }).catch(() => { clearTimeout(slow); shell().then(r => finish(r || Response.error())); });
  });
}

self.addEventListener("fetch", e => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin === location.origin) {
    if (u.pathname.startsWith("/cal/") || u.pathname.endsWith("/sw.js")) return;
    if (r.mode === "navigate") { if (u.pathname === "/" || u.pathname === "/index.html") e.respondWith(page(r)); return; }
    e.respondWith(caches.match(r, { ignoreSearch: true }).then(m => m || fetch(r).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); }
      return res;
    })));
    return;
  }
  if (u.hostname === "fonts.googleapis.com" || u.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.open(FONTS).then(c => c.match(r).then(m => {
      const net = fetch(r).then(res => { if (res.ok || res.type === "opaque") c.put(r, res.clone()); return res; })
        .catch(() => m || Response.error());
      return m || net;
    })));
  }
});
