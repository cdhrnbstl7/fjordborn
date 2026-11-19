#!/bin/bash
# release.sh 1.0.3 "notes"   -> builds the app + installer, writes latest.yml, and (with PUBLISH=1) publishes a GitHub release
set -e
V="$1"; NOTES="${2:-Fjordborn $1}"; cd /home/claude/launcher
python3 /home/claude/work/build.py >/dev/null
python3 - "$V" <<'PY'
import json,sys;d=json.load(open('package.json'));d['version']=sys.argv[1];d['build']['publish']=[{'provider':'github','owner':'cdhrnbstl7','repo':'fjordborn'}];json.dump(d,open('package.json','w'),indent=2)
PY
rm -rf dist; export WINEDEBUG=-all
npx electron-builder --win dir --x64 --publish never 2>&1 | grep -E "icon and details|⨯" || true
test -f dist/win-unpacked/resources/app-update.yml
N=$(dirname $(dirname $(find /root/.cache/electron-builder/nsis-3.0.4.1 -path "*linux/makensis")))
(cd build && NSISDIR=$N $N/linux/makensis -V2 -DVER=$V manual-installer.nsi.txt)
EXE=dist/Fjordborn-Setup-$V.exe; test -f $EXE
SHA=$(openssl dgst -sha512 -binary $EXE | base64 -w0); SIZE=$(stat -c %s $EXE); NOW=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
cat > dist/latest.yml <<YML
version: $V
files:
  - url: Fjordborn-Setup-$V.exe
    sha512: $SHA
    size: $SIZE
path: Fjordborn-Setup-$V.exe
sha512: $SHA
releaseDate: '$NOW'
YML
echo "built $EXE ($SIZE bytes)"
if [ "$PUBLISH" = "1" ]; then
  R=cdhrnbstl7/fjordborn
  ID=$(gh api repos/$R/releases -X POST -f tag_name=v$V -f name="Fjordborn $V" -f body="$NOTES" --jq .id)
  for f in $EXE dist/latest.yml; do
    gh api "https://uploads.github.com/repos/$R/releases/$ID/assets?name=$(basename $f)" -X POST -H "Content-Type: application/octet-stream" --input $f --jq .browser_download_url
  done
fi
