// Sets Fjordborn's icon and version details on Fjordborn.exe (no Wine needed).
const fs = require('fs');
const path = require('path');
const ResEdit = require('resedit');
exports.default = async function (ctx) {
  if (ctx.electronPlatformName !== 'win32') return;
  // tells the built-in updater where new versions are published
  fs.writeFileSync(path.join(ctx.appOutDir, 'resources', 'app-update.yml'), 'owner: cdhrnbstl7\nrepo: fjordborn\nprovider: github\nupdaterCacheDirName: fjordborn-updater\n');
  const exe = path.join(ctx.appOutDir, 'Fjordborn.exe');
  const data = fs.readFileSync(exe);
  const pe = ResEdit.NtExecutable.from(data, { ignoreCert: true });
  const res = ResEdit.NtExecutableResource.from(pe);
  const ico = ResEdit.Data.IconFile.from(fs.readFileSync(path.join(__dirname, 'icon.ico')));
  const groups = ResEdit.Resource.IconGroupEntry.fromEntries(res.entries);
  const ids = groups.length ? groups.map(g => g.id) : [1];
  for (const id of ids) {
    ResEdit.Resource.IconGroupEntry.replaceIconsForResource(res.entries, id, groups[0] ? groups[0].lang : 1033, ico.icons.map(i => i.data));
  }
  const vi = ResEdit.Resource.VersionInfo.fromEntries(res.entries)[0];
  const lang = { lang: 1033, codepage: 1200 };
  vi.setStringValues(lang, {
    FileDescription: 'Fjordborn', ProductName: 'Fjordborn', CompanyName: 'Fjordborn',
    InternalName: 'Fjordborn', OriginalFilename: 'Fjordborn.exe', LegalCopyright: 'Fjordborn'
  });
  vi.removeStringValue(lang, 'Comments');
  const V = ctx.packager.appInfo.version.split('.').map(Number);
  vi.setFileVersion(V[0], V[1], V[2], 0, 1033);
  vi.setProductVersion(V[0], V[1], V[2], 0, 1033);
  vi.outputToResourceEntries(res.entries);
  res.outputResource(pe);
  fs.writeFileSync(exe, Buffer.from(pe.generate()));
  console.log('  • Fjordborn.exe icon and details set');
};
