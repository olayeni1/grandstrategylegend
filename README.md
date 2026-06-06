# Grand Strategy — Legend Edition (Installable App / PWA)

A phone-friendly, **installable** version of `grandstrategylegend.html`. It is a
Progressive Web App (PWA): it runs in any modern browser, can be added to your
home screen, launches full-screen with its own icon, and **works offline** after
the first load. No app store required.

## Play / Install

Open the app in a browser:

```
https://olayeni1.github.io/Ola/grand-strategy/
```

**Install on Android / Chrome / Edge (desktop or phone):**
tap the **📲 Install App** button on the menu, or use the browser menu →
*“Install app” / “Add to Home screen.”*

**Install on iPhone / iPad (Safari):**
tap the **Share** button ⬆️, then **“Add to Home Screen.”**

Once installed it behaves like a native app: full-screen, offline-capable, and
your game auto-saves to the device.

## What was added on top of the original game

- **Web App Manifest** (`manifest.webmanifest`) + app icons → makes it installable.
- **Service worker** (`sw.js`) → caches the app shell so it loads & plays offline.
- **Mobile layout** → the side panel becomes a slide-up bottom sheet (“⚙️ Manage
  Empire”), with safe-area handling for notches.
- **Touch controls** → one-finger pan, two-finger pinch-to-zoom, tap a region for
  its info tooltip, tap the minimap to jump.

The game logic, world simulation, save format, and visuals are unchanged from the
original single-file version.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The game + PWA wiring + mobile/touch UI |
| `manifest.webmanifest` | App metadata, icons, install behavior |
| `sw.js` | Service worker (offline caching) |
| `icons/` | App icons (192, 512, maskable, Apple touch) |
| `gen_icons.py` | Script that generated the icons (no dependencies) |

## Local testing

Serve the folder over HTTP (service workers need http/https, not `file://`):

```bash
cd grand-strategy
python3 -m http.server 8080
# then open http://localhost:8080/
```
