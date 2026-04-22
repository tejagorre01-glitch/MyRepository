const CACHE_NAME = "expense-pwa-v1";
const FILES = [
  "/login",
  "/home",
  "/monthly",
  "/static/styles.css"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(FILES))
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(res => res || fetch(e.request))
  );
});
