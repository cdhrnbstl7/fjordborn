// Restores the private working source from tools/source.enc.
// Usage: FJ_DEV_PASS=... node tools/source_unpack.js tools/source.enc out.tar   then: tar -xf out.tar -C /home/claude
const crypto = require('crypto'), fs = require('fs'), zlib = require('zlib');
const pass = process.env.FJ_DEV_PASS; if (!pass) { console.error('Set FJ_DEV_PASS'); process.exit(1); }
const [src, out] = process.argv.slice(2), d = JSON.parse(fs.readFileSync(src, 'utf8'));
const key = crypto.pbkdf2Sync(pass, Buffer.from(d.salt, 'base64'), d.it, 32, 'sha256'), ct = Buffer.from(d.ct, 'base64');
const dc = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(d.iv, 'base64'));dc.setAuthTag(ct.subarray(ct.length - 16));
fs.writeFileSync(out, zlib.gunzipSync(Buffer.concat([dc.update(ct.subarray(0, ct.length - 16)), dc.final()])));console.log('wrote', out);
