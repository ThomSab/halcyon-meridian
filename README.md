# Agentbox: Halcyon Meridian

Worldbuilding notes, a text adventure, 2D/SVG art, and low-poly walkable 3D scenes (engine room and the Spine) for the **Halcyon Meridian**, a 1,600 m nuclear-powered, wind-assisted city ship.

## Contents

| Path | What it is |
|---|---|
| `lore/*.md` | Worldbuilding reference: ship structure, propulsion, governance, daily life, etc. Start with `lore/halcyon_meridian_general_description.md` and `lore/ship_structure_and_layout.md`. |
| `halcyon_meridian_game.py` | Text adventure (Python 3, stdlib only). Run with `python halcyon_meridian_game.py`. |
| `halcyon_meridian_exterior.svg`, `halcyon_meridian_spine_interior.svg` | 2D artwork of the ship exterior and the Spine. |
| `engine_room/` | Low-poly engine room: Blender build script, exported GLB, collision data, and a walkable Three.js viewer. |
| `spine/` | Walkable blockout of the Spine (Deck 9): towers at each end, market halls, rails. Blender build script, GLB, collision data, and a Three.js viewer. |
| `package.json`, `package-lock.json` | Node deps. Only `three` (0.187.0) is used, by the viewer. |

## Engine room

- `engine_room/build_engine_room.py`: Blender script that builds the room and exports `engine_room.glb` and `engine_room_colliders.json`. Units are meters. Blender is Z-up, and the glTF exporter converts to Y-up.
- `engine_room/index.html`: first-person viewer. Click to start, WASD/arrows to move, Shift to run, mouse to look, Esc to release.

### Rebuild the model

Blender 5.3 is installed at `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`.

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "engine_room\build_engine_room.py"
```

## The Spine (walkable ship)

- `spine/build_spine.py`: Blender script that builds the Spine blockout and exports `spine.glb` and `spine_colliders.json`.
- `spine/index.html`: first-person viewer. Walk from the aft tower to the fore tower along the centre aisle. The HUD shows your distance along the Spine.

Layout: aft tower at X = 0 to 100 m, fore tower at X = 1500 to 1600 m, Spine floor between them (X = 100 to 1500 m, 40 m wide, Z = 0 is the Deck 9 floor). Market halls line both sides, leaving a 22 m clear centre aisle. The Spine is 1,400 m here, against about 1.5 km in the lore; the towers are plain boxes; there is no hull or sky geometry beyond the Spine.

Rebuild:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "spine\build_spine.py"
```

## Viewing

The viewers load files with `fetch` and ES modules, so they must be served over HTTP (opening the file directly won't work). From the repo root:

```powershell
python -m http.server 8000
```

- Engine room: http://localhost:8000/engine_room/index.html
- The Spine: http://localhost:8000/spine/index.html

Run the server from the repo root so `node_modules/three` resolves. Click the page to start, WASD/arrows to move, Shift to run, mouse to look, Esc to release.

Dependencies: `npm install` (needed for `node_modules/three`).

## Layout of the engine room

Coordinates in Blender: X runs along the ship (aft at 0, fore at 120), Y is port/starboard (centre 0), Z is up (floor at 0). Room is 120 x 40 x 14 m.

- Four reactor citadels (radius 6 m) on the centerline at X = 22, 47, 72, 97. They block the centre aisle, so walk the port or starboard aisle.
- Six pod thruster motors at the aft end (X about 9).
- Switchboards along both side walls, X = 30 to 66.
- Coolant pipes overhead, control room cabin at the fore end (X about 102 to 120, Y -20 to -10).
- Overhead catwalks at Z = 6 (no collision).

The viewer's start position is in the port aisle at Blender (20, -12).

## Status and open questions

Done:
- Blender 5.3 installed and verified headless.
- Lore files moved into `lore/` (60 files, `README.md` stays at the root).
- Engine room model built, exported, and rendered in headless Edge.
- The Spine blockout built, exported, and rendered in headless Edge. No errors in the console; the viewer uses `THREE.Timer`, not the deprecated `THREE.Clock`.
- A local server runs on port 8000 from this folder. It's a background process and does not survive a restart.

Not done or not decided:
- **Game engine/platform is not decided.** Options are a browser game (Three.js or Babylon.js), Godot, or Unity. This determines the next steps.
- **Art style not decided.** The current model is untextured, flat-shaded, and lit with basic point lights.
- **Three.js MCP server not configured.** Candidate: `threejs-devtools-mcp` on npm (unverified). Add to `opencode.json` under `"mcp"` if wanted.
- **Mouse/keyboard controls not tested interactively.** Only a headless screenshot was checked.
- The interior of the reactor citadels is not modelled; they are solid cylinders.
- The Spine viewer's collision and movement were not played interactively; only a headless screenshot was checked.
- Only the engine room and the Spine are modelled. Residential terraces, the bridge, and the hull are not.

## Next steps (suggested)

1. Confirm the target engine/platform and art style.
2. Play both viewers and note any collision or lighting problems.
3. Add materials, textures, and more detail if the style calls for it.
4. Model additional areas (residential terraces, bridge), following the pattern in `spine/build_spine.py`.
