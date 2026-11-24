#!/bin/bash
# Packs the private working source (the full game with its dev-only code, the build script and the test harness)
# into tools/source.enc, encrypted with the dev password. Run from the repo root:
#   FJ_DEV_PASS=... bash tools/source_pack.sh
set -e
[ -n "$FJ_DEV_PASS" ] || { echo "Set FJ_DEV_PASS"; exit 1; }
T=$(mktemp -d)
mkdir -p "$T/work" "$T/launcher" "$T/bin"
cp /home/claude/work/src.html /home/claude/work/build.py /home/claude/work/make_webapp.py /home/claude/work/app_head.txt "$T/work/" 2>/dev/null || true
cp /home/claude/launcher/*.js "$T/launcher/"
cp /home/claude/close.sh /home/claude/mont.py "$T/bin/" 2>/dev/null || true
tar -C "$T" -cf "$T/src.tar" work launcher bin
node tools/dev_encrypt.js "$T/src.tar" tools/source.enc
rm -rf "$T"
