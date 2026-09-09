// FlipCam — Service Worker
// Caches the shell for offline first paint. Stays out of the way of camera & recording.

const CACHE = 'flipcam-v6';
const SHELL_URL = '/index.html';
const SHELL = [
  '/',
  '/index.html',
  '/manifest.json',
  '/images/icon-192.png',
  '/images/icon-512.png',
  '/images/apple-touch-icon.png',
  '/images/favicon.png',
];

// Per-file so one missing asset can't leave the app with no offline shell at all.
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(SHELL.map(u => c.add(new Request(u, { cache: 'reload' })))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

const offlineFallback = () => new Response('', { status: 504, statusText: 'Offline' });

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  // Never cache the build stamp — it must hit network so we detect new deploys
  if (url.pathname === '/build-stamp') return;
  if (url.origin !== location.origin) return;

  // The manifest start_url is "/?source=pwa", and caches.match() keys on the
  // query string too — so offline it missed the cached "/" and the camera app
  // showed the browser's error page until one online request cached that exact
  // URL. A camera needs no network at all; every navigation now resolves to the
  // cached shell, query string or not.
  if (e.request.mode === 'navigate') {
    e.respondWith(
      caches.match(SHELL_URL).then(cached => {
        const networked = fetch(e.request).then(res => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(SHELL_URL, copy)).catch(() => {});
          }
          return res;
        }).catch(() => cached || offlineFallback());
        return cached || networked;
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(cached => {
      const networked = fetch(e.request).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
        }
        return res;
      }).catch(() => cached || offlineFallback());
      return cached || networked;
    })
  );
});
