# Fjordborn: project guide

Read this first. It is the shared memory for every chat and agent working on Fjordborn. This repository is **public**: never commit secrets, the dev password, or the plain dev source.

## What the game is
A Valheim-style Viking survival game. It has one large island with four biomes: the Strand (beaches), the Sunmeads (meadows), the Gloamwood (forest) and the Hoarfells (snowy mountains). It also has barrow tombs and the Drowned Colossus wreck. Players gather, build, craft, sail a longship, fight creatures and bosses, and explore dungeons.

## Engine and tech
- **No game engine.** The game is one hand-written HTML file running **three.js r128** (WebGL). Everything lives in that file: terrain, water, sky, creatures, UI, saves (localStorage) and audio.
- **Desktop:** an **Electron** launcher (`launcher/`) wraps the game and auto-updates from GitHub Releases.
- **Creatures:** sculpted offline in **Blender 4.0.2** from metaball specs (`tools/beasts/`), then packed as skinned meshes into the page.
- **Build:** Python (`build.py`) turns the one source file into phone, desktop and dev editions.

## Where things are
| Path | What it is |
|---|---|
| `game/fjordborn.html` | Desktop public build (copy of `out_desktop.html`) |
| `docs/` | Home-screen web app (GitHub Pages), made by `make_webapp.py` |
| `launcher/` | Electron app; `launcher/app/game/index.html` is the launcher's game page, `dev.enc` the encrypted dev edition |
| `tools/beasts/` | Creature pipeline: `specs.py` (sculpts), `build2.py` (Blender build), `pack.py` (packs `beasts.json`) |
| `tools/dev_encrypt.js` | Encrypts the dev edition into `launcher/app/game/dev.enc` |
| `tools/source.enc` | **Encrypted backup of the private working source** (see below) |
| `RELEASE_NOTES.md` | Newest release at the top; written for players |

The working source is **not** in plain form in this repo, because it contains the dev-only code:
- `/home/claude/work/src.html`: the single source file for everything.
- `/home/claude/work/build.py`: produces `out_phone.html`, `out_desktop.html`, `out_*_dev.html`, `app_dev.html`, and the launcher test page.
- `/home/claude/launcher/*.js`: test harnesses: `close.js` (creature close-ups), `vista.js` (landscape views), `mapshot.js` (world map), `perf.js` (phone frame times).
- `/home/claude/close.sh` and `/home/claude/mont.py`: capture wrapper and image montage.

**Restoring on a fresh machine:** clone the repo, get the dev password from the owner, then:
```
FJ_DEV_PASS=... node tools/source_unpack.js tools/source.enc /tmp/src.tar && tar -xf /tmp/src.tar -C /home/claude
```
After meaningful source changes, refresh the backup before committing: `FJ_DEV_PASS=... bash tools/source_pack.sh`.

## The dev edition (private)
- The owner wants a developer version that **nobody else can access**.
- Dev-only code sits between `/*DEV{*/` and `/*}DEV*/` in `src.html`. Public builds strip it.
- The dev build ships only encrypted (`dev.enc`, AES-GCM, key from `FJ_DEV_PASS`).
- The password lives only in `/home/claude/work/devpass.txt` (never committed) and with the owner.

## Every change ships everywhere, together
Six targets must always match:
1. Public phone artifact `862c8ee7-2065-4bd7-8178-a628851fee9e` (shared publicly; publish with `shared_live:"public"`, `artifact_title:"Fjordborn"`)
2. Desktop artifact `75238368-4ced-4d09-a3aa-5e7fe369159d`
3. Dev phone artifact `20abcd87-6090-480f-9aa6-7b74bbe24ba7` (private)
4. Dev desktop artifact `64d5da43-b4b9-439b-a80e-1f6b1899afa4` (private)
5. Home-screen web app (`docs/`)
6. Electron launcher via GitHub Releases

### Release checklist
1. Bump `GAME_VERSION` in `src.html`, then `cd /home/claude/work && python3 build.py`.
2. `cd /home/claude/repo && FJ_DEV_PASS="$(cat /home/claude/work/devpass.txt)" node tools/dev_encrypt.js /home/claude/work/app_dev.html launcher/app/game/dev.enc`
3. `cp /home/claude/work/out_desktop.html game/fjordborn.html`
4. `python3 /home/claude/work/make_webapp.py docs`, then `python3 tools/build_pages.py`
5. Bump `launcher/package.json` version, and prepend a player-facing entry to `RELEASE_NOTES.md`.
6. If creatures changed, copy `specs.py build2.py pack.py` to `tools/beasts/`. Refresh `tools/source.enc`.
7. Commit (end the message with the attribution lines), push, then `gh workflow run release.yml --ref main` and watch it finish.
8. Publish the four artifacts from `out_phone.html`, `out_desktop.html`, `out_phone_dev.html` and `out_desktop_dev.html`.

## Creature pipeline
- Sculpts live in `specs.py` as metaball parts: `ell`, `mcap`, `cap`, `horn`, `spike`, `sym`, and `neg` (carves).
  - Each sculpt has a `color(g,n)` function that paints vertex colours.
  - Each sculpt defines a rig: `biped_bones` or `quad_bones`.
- Spec keys: `tris` (detail), `voxel` (remesh size), `ao` and `aodist` (baked crevice shading).
  - `iface` is only for bipeds and floaters: a dict with `legs`.
  - `iface:{mat:...}` picks an in-game material: `metal`, `bone`, `skin`, `war` (war paint), `cinder` (glowing cracks), `ghost` or `cloth`.
- Build one creature: `cd /home/claude/beasts && blender -b -P build2.py -- <name>`. This takes 1 to 9 minutes and writes `out/<name>_{side,q,front}.png` previews.
- Pack: `python3 pack.py <every creature name>`, listing **all** of them, not just the new one. Then embed `beasts.json` into the `<script id="fjbeasts">` tag of `src.html`.
- In game: `BEASTMAP` maps creature to sculpt, and `PROPS.<name>(r,b)` adds eyes, weapons, rags and effects. Bone offsets are world positions minus `r.H[bone]`.
- Check in game with `/home/claude/close.sh '[["wolf",0,4,1,1,"dummy"],[type,yaw,camDist,camH,lookH,tag,preJS]...]'`, then `python3 /home/claude/mont.py out.png tags...`.
  - The first shot is a throwaway, since the shaders are still warming up.
  - `F.setTime(.86)` gives night and `.3` gives day.

## World
- `WS=1.5`: the island is built 1.5x its original 1.5 km. Island-shaping code works in pre-scale units (divide by `WS`). `coastR()` makes the ragged coast.
- `WLIM`: the sea limit, three times the old reach. `DZX=2700`: tombs are built past this x.
- `LANDK` scales how much scenery, ore and flowers are scattered.
- The save world version is `w:5`. Older saves go through `migrateWorld()`, which refunds buildings and resets the spawn point.

## How the owner likes to work
- **Quality over quantity.** One thing at a time, done well. Show pictures at each check-in before moving on.
- Use their reference images for the look, but never copy copyrighted characters; make original designs with the same feel.
- Keep replies plain and short. Say what changed, then show a picture.
- Player damage is tuned by `PDMG` (currently 1.1). The owner is collecting balance feedback.

## Roadmap (as of 1.24.0)
- **Done:**
  - Tomb undead: draugr, plate-armour Barrow Knight and ghoul.
  - Holy weapons: Hallowed Blade and Dawnbrand. Knights need holy steel; wraiths need the Dawnbrand.
  - Sunmeads night creatures: Ravager, Cinder Hound, Hollow Strawman and Crimson Revenant.
  - The 1.5x ragged island and the three-times-wider sea.
- **Next:**
  - Texture pass while the owner sleeps.
  - Creatures for the Drowned Colossus, then the Hoarfells (golem, serpent, spider, chained), then the bosses.
  - Holy weapon variants that get stronger per biome.
  - Attack animations from the owner's examples, much later.
  - New lands in the open sea.
- **Under consideration:** subagents. Start with one read-only reviewer that checks screenshots against the references.
