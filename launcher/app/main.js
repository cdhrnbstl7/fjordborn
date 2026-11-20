// Fjordborn desktop app: runs the game in its own window with the bundled engine.
const { app, BrowserWindow, protocol, net, shell, Menu, ipcMain, safeStorage } = require('electron');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
let autoUpdater = null;
try { ({ autoUpdater } = require('electron-updater')); } catch (e) { autoUpdater = null; }

// Use the dedicated graphics card and keep full speed when the window is in the background.
app.commandLine.appendSwitch('force_high_performance_gpu');
app.commandLine.appendSwitch('ignore-gpu-blocklist');
app.commandLine.appendSwitch('enable-gpu-rasterization');
app.commandLine.appendSwitch('enable-zero-copy');
app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('disable-renderer-backgrounding');
app.commandLine.appendSwitch('disable-backgrounding-occluded-windows');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');

// A fixed app:// address so saves in local storage always belong to the same place.
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } }
]);

const GAME_DIR = path.join(__dirname, 'game');
let devHtml = null;
let win = null;

if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (win) { if (win.isMinimized()) win.restore(); win.focus(); }
  });

  app.whenReady().then(() => {
    protocol.handle('app', (req) => {
      const u = new URL(req.url);
      let rel = decodeURIComponent(u.pathname);
      if (rel === '/' || rel === '') rel = '/index.html';
      // the developer edition is held only in memory after the launcher unlocks it with the password
      if (rel === '/dev.html') return devHtml ? new Response(devHtml, { headers: { 'content-type': 'text/html; charset=utf-8' } }) : new Response('Locked', { status: 403 });
      const file = path.normalize(path.join(GAME_DIR, rel));
      if (!file.startsWith(GAME_DIR)) return new Response('Not found', { status: 404 });
      return net.fetch(pathToFileURL(file).toString());
    });

    Menu.setApplicationMenu(null);
    // settings kept between launches (full screen or windowed)
    const optFile = path.join(app.getPath('userData'), 'launcher.json');
    let opts = { full: true };
    try { opts = Object.assign(opts, JSON.parse(fs.readFileSync(optFile, 'utf8'))); } catch (e) {}
    const saveOpts = () => { try { fs.writeFileSync(optFile, JSON.stringify(opts)); } catch (e) {} };

    // ---- the game window ----
    const openGame = (page) => {
      win = new BrowserWindow({
        width: 1600, height: 900, minWidth: 960, minHeight: 540,
        fullscreen: !process.env.FJORD_WINDOWED && opts.full,
        backgroundColor: '#000000',
        title: 'Fjordborn',
        icon: path.join(__dirname, 'icon.ico'),
        autoHideMenuBar: true,
        show: false,
        webPreferences: { contextIsolation: true, sandbox: true, nodeIntegration: false, backgroundThrottling: false, spellcheck: false }
      });
      win.once('ready-to-show', () => win.show());
      // F11 or Alt+Enter toggles full screen; Ctrl+Shift+I is left out on purpose.
      win.webContents.on('before-input-event', (e, input) => {
        if (input.type === 'keyDown' && (input.key === 'F11' || (input.alt && input.key === 'Enter'))) { win.setFullScreen(!win.isFullScreen()); e.preventDefault(); }
      });
      // Links (like "open on its own page") go to the normal web browser.
      win.webContents.setWindowOpenHandler(({ url }) => { if (/^https?:/.test(url)) shell.openExternal(url); return { action: 'deny' }; });
      win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('app://')) { e.preventDefault(); if (/^https?:/.test(url)) shell.openExternal(url); } });
      win.loadURL('app://fjordborn/' + (page || process.env.FJORD_PAGE || 'index.html'));
    };
    const note = (msg) => { try { if (win) win.webContents.executeJavaScript('window.FJ_NOTE&&FJ_NOTE(' + JSON.stringify(msg) + ')').catch(() => {}); } catch (e) {} };

    // ---- the launcher: news, version, updates, and the Play button (like Tarkov's) ----
    const useLauncher = !process.env.FJORD_PAGE && !process.env.FJORD_SKIP_LAUNCHER;
    let lw = null, status = { msg: 'Ready to play', block: false };
    const send = (s) => { status = s; if (lw && !lw.isDestroyed()) lw.webContents.send('fjl:status', s); };
    // developer edition: the password is remembered (encrypted by the operating system) only if asked
    const keyFile = path.join(app.getPath('userData'), 'dev.key');
    const savedPass = () => { try { if (safeStorage.isEncryptionAvailable() && fs.existsSync(keyFile)) return safeStorage.decryptString(fs.readFileSync(keyFile)); } catch (e) {} return ''; };
    ipcMain.handle('fjl:info', () => ({ version: app.getVersion(), full: !!opts.full, devPass: savedPass() }));
    ipcMain.on('fjl:devplay', (_e, html, pass, remember) => {
      if (typeof html !== 'string' || !html.includes('DEVELOPER EDITION')) return;
      devHtml = html;
      try { if (remember && pass && safeStorage.isEncryptionAvailable()) fs.writeFileSync(keyFile, safeStorage.encryptString(pass)); else if (!remember && fs.existsSync(keyFile)) fs.unlinkSync(keyFile); } catch (e) {}
      if (status.block) return; openGame('dev.html'); if (lw) { const l = lw; lw = null; l.close(); }
    });
    ipcMain.on('fjl:play', () => { if (status.block) return; openGame(); if (lw) { const l = lw; lw = null; l.close(); } });
    ipcMain.on('fjl:install', () => { if (autoUpdater) { send({ msg: 'Installing the update. Fjordborn will restart...', busy: true, block: true }); setImmediate(() => autoUpdater.quitAndInstall(true, true)); } });
    ipcMain.on('fjl:check', () => check(true));
    ipcMain.on('fjl:quit', () => app.quit());
    ipcMain.on('fjl:min', () => { if (lw) lw.minimize(); });
    ipcMain.on('fjl:opt', (_e, k, v) => { opts[k] = v; saveOpts(); });

    let checking = false, downloaded = false;
    const canUpdate = autoUpdater && app.isPackaged && !process.env.FJORD_NO_UPDATE;
    function check(manual) {
      if (!canUpdate) { send({ msg: manual ? 'Updates only work in the installed game.' : 'Ready to play', block: false }); return; }
      if (checking || downloaded) return; checking = true;
      if (lw) send({ msg: 'Checking for updates...', busy: true, block: true });
      // never keep the player waiting on a slow connection
      const t = setTimeout(() => { if (checking && !status.pct) send({ msg: 'The update server is slow to answer. You can play now.', block: false }); }, 12000);
      autoUpdater.checkForUpdates().catch(() => {}).finally(() => clearTimeout(t));
    }
    if (canUpdate) {
      autoUpdater.autoDownload = true;
      autoUpdater.autoInstallOnAppQuit = true;
      autoUpdater.on('update-available', (i) => { send({ msg: 'Downloading update ' + i.version + '...', busy: true, pct: 0, block: true }); note('Downloading Fjordborn ' + i.version + ' in the background...'); });
      autoUpdater.on('download-progress', (p) => send({ msg: 'Downloading update: ' + Math.round(p.percent) + '%  (' + (p.bytesPerSecond / 1048576).toFixed(1) + ' MB/s)', busy: true, pct: p.percent, block: true }));
      autoUpdater.on('update-not-available', () => { checking = false; send({ msg: 'Fjordborn is up to date', block: false }); });
      autoUpdater.on('update-downloaded', (i) => { checking = false; downloaded = true; send({ msg: 'Update ' + i.version + ' is ready. Press Update to install it.', state: 'downloaded', block: false }); note('Fjordborn ' + i.version + ' is ready. It installs when you quit the game.'); });
      autoUpdater.on('error', () => { checking = false; if (!downloaded) send({ msg: 'Could not reach the update server. You can still play.', block: false }); });
      setInterval(() => { if (!lw) check(false); }, 2 * 60 * 60 * 1000);
    }

    if (useLauncher) {
      lw = new BrowserWindow({
        width: 1120, height: 660, minWidth: 900, minHeight: 560, frame: false, resizable: true,
        backgroundColor: '#07080a', title: 'Fjordborn', icon: path.join(__dirname, 'icon.ico'), show: false,
        webPreferences: { contextIsolation: true, sandbox: true, nodeIntegration: false, preload: path.join(__dirname, 'preload.js'), spellcheck: false }
      });
      lw.once('ready-to-show', () => lw.show());
      lw.webContents.setWindowOpenHandler(({ url }) => { if (/^https?:/.test(url)) shell.openExternal(url); return { action: 'deny' }; });
      lw.webContents.on('did-finish-load', () => { send(status); check(false); });
      lw.on('closed', () => { if (lw) { lw = null; if (!win) app.quit(); } });
      lw.loadURL('app://fjordborn/launcher.html');
    } else {
      openGame();
      if (canUpdate) setTimeout(() => check(false), 8000);
    }
  });

  app.on('window-all-closed', () => app.quit());
}
