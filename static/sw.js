self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open('lyrics-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/static/style.css', // If you split out CSS
                '/static/icon-192.png',
                '/static/icon-512.png'
            ]);
        })
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});
