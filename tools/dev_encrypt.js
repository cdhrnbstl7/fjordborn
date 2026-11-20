// Encrypts the developer edition for the desktop launcher.
// Usage: FJ_DEV_PASS=... node tools/dev_encrypt.js <dev.html> <out dev.enc>
// The password is never stored in this repository; only the encrypted file is.
const crypto = require('crypto'), fs = require('fs'), zlib = require('zlib');
const pass = process.env.FJ_DEV_PASS; if (!pass) { console.error('Set FJ_DEV_PASS'); process.exit(1); }
const [src, out] = process.argv.slice(2);
const salt = crypto.randomBytes(16), iv = crypto.randomBytes(12), it = 250000;
const key = crypto.pbkdf2Sync(pass, salt, it, 32, 'sha256');
const c = crypto.createCipheriv('aes-256-gcm', key, iv);
const ct = Buffer.concat([c.update(zlib.gzipSync(fs.readFileSync(src), { level: 9 })), c.final(), c.getAuthTag()]);
fs.writeFileSync(out, JSON.stringify({ v: 1, it, salt: salt.toString('base64'), iv: iv.toString('base64'), ct: ct.toString('base64') }));
console.log('wrote', out, ct.length, 'bytes');
