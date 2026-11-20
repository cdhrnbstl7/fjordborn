// Bridge between the launcher page and the app: status updates in, button presses out.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('FJL', {
  info: () => ipcRenderer.invoke('fjl:info'),
  onStatus: (fn) => ipcRenderer.on('fjl:status', (_e, s) => fn(s)),
  play: () => ipcRenderer.send('fjl:play'),
  install: () => ipcRenderer.send('fjl:install'),
  check: () => ipcRenderer.send('fjl:check'),
  quit: () => ipcRenderer.send('fjl:quit'),
  setOpt: (k, v) => ipcRenderer.send('fjl:opt', k, v),
  minimize: () => ipcRenderer.send('fjl:min')
});
