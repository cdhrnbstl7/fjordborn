// Fjordborn desktop app: runs the game in its own window with the bundled engine.
const { app, BrowserWindow, protocol, net, shell, Menu, globalShortcut } = require('electron');
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
      const file = path.normalize(path.join(GAME_DIR, rel));
      if (!file.startsWith(GAME_DIR)) return new Response('Not found', { status: 404 });
      return net.fetch(pathToFileURL(file).toString());
    });

    Menu.setApplicationMenu(null);
    win = new BrowserWindow({
      width: 1600, height: 900, minWidth: 960, minHeight: 540,
      fullscreen: !process.env.FJORD_WINDOWED,
      backgroundColor: '#000000',
      title: 'Fjordborn',
      icon: path.join(__dirname, 'icon.ico'),
      autoHideMenuBar: true,
      show: false,
      webPreferences: {
        contextIsolation: true,
        sandbox: true,
        nodeIntegration: false,
        backgroundThrottling: false,
        spellcheck: false
      }
    });
    win.once('ready-to-show', () => win.show());

    // F11 toggles full screen; Ctrl+Shift+I is left out on purpose.
    win.webContents.on('before-input-event', (e, input) => {
      if (input.type === 'keyDown' && input.key === 'F11') {
        win.setFullScreen(!win.isFullScreen()); e.preventDefault();
      }
      if (input.type === 'keyDown' && input.alt && input.key === 'Enter') {
        win.setFullScreen(!win.isFullScreen()); e.preventDefault();
      }
    });

    // Links (like "open on its own page") go to the normal web browser.
    win.webContents.setWindowOpenHandler(({ url }) => {
      if (/^https?:/.test(url)) shell.openExternal(url);
      return { action: 'deny' };
    });
    win.webContents.on('will-navigate', (e, url) => {
      if (!url.startsWith('app://')) { e.preventDefault(); if (/^https?:/.test(url)) shell.openExternal(url); }
    });

    win.loadURL('app://fjordborn/' + (process.env.FJORD_PAGE || 'index.html'));

    // Updates: check GitHub for a newer version, download it in the background, install it when the game is quit.
    const note = (msg) => { try { win.webContents.executeJavaScript('window.FJ_NOTE&&FJ_NOTE(' + JSON.stringify(msg) + ')').catch(() => {}); } catch (e) {} };
    if (autoUpdater && app.isPackaged && !process.env.FJORD_NO_UPDATE) {
      autoUpdater.autoDownload = true;
      autoUpdater.autoInstallOnAppQuit = true;
      autoUpdater.on('update-available', (i) => note('Downloading Fjordborn ' + i.version + ' in the background...'));
      autoUpdater.on('update-downloaded', (i) => note('Fjordborn ' + i.version + ' is ready. It installs when you quit the game.'));
      autoUpdater.on('error', () => {});
      const check = () => autoUpdater.checkForUpdates().catch(() => {});
      setTimeout(check, 8000);
      setInterval(check, 2 * 60 * 60 * 1000);
    }
  });

  app.on('window-all-closed', () => app.quit());
}
