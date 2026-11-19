# Fjordborn

A Viking survival saga: gather, craft, build a hall, and wake the giant sleeping under the Gloamwood.

**Download:** get the latest `Fjordborn-Setup-x.y.z.exe` from [Releases](../../releases/latest). Once installed, the game updates itself: new versions download in the background and install when you quit.

## Layout
- `game/fjordborn.html` — the whole game (one page, three.js r128).
- `launcher/` — the Windows desktop app (Electron), its installer script (NSIS) and `release.sh`, which builds a version and publishes it as a GitHub release with `latest.yml` for the updater.
- `tools/build_pages.py` — builds the phone, desktop and app editions of the page.
