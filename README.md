# Agentbox: Halcyon Meridian

Worldbuilding notes, a text adventure, 2D/SVG art, and a low-poly 3D engine room for the **Halcyon Meridian**, a 1,600 m nuclear-powered, wind-assisted city ship.

## Contents

| Path | What it is |
|---|---|
| `*.md` (root) | Worldbuilding reference: ship structure, propulsion, governance, daily life, etc. Start with `halcyon_meridian_general_description.md` and `ship_structure_and_layout.md`. |
| `halcyon_meridian_game.py` | Text adventure (Python 3, stdlib only). Run with `python halcyon_meridian_game.py`. |
| `halcyon_meridian_exterior.svg`, `halcyon_meridian_spine_interior.svg` | 2D artwork of the ship exterior and the Spine. |
| `engine_room/` | Low-poly engine room: Blender build script, exported GLB, collision data, and a walkable Three.js viewer. |
| `package.json`, `package-lock.json` | Node deps. Only `three` (0.187.0) is used, by the viewer. |

## Engine room

- `engine_room/build_engine_room.py`: Blender script that builds the room and exports `engine_room.glb` and `engine_room_colliders.json`. Units are meters. Blender is Z-up, and the glTF exporter converts to Y-up.
- `engine_room/index.html`: first-person viewer. Click to start, WASD/arrows to move, Shift to run, mouse to look, Esc to release.

### Rebuild the model

Blender 5.3 is installed at `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`.

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "engine_room\build_engine_room.py"
```

### View it

The viewer loads files with `fetch` and ES modules, so it must be served over HTTP (opening the file directly won't work):

```powershell
python -m http.server 8000
```

Then open http://localhost:8000/engine_room/index.html. Run the command from the repo root so `node_modules/three` resolves.

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
- Engine room model built, exported, and rendered in headless Edge (`engine_room` loads and displays).
- Viewer started from a local server on port 8000 (`python -m http.server 8000` from this folder). This is a background process and does not survive a restart.

Not done or not decided:
- **Game engine/platform is not decided.** Options are a browser game (Three.js or Babylon.js), Godot, or Unity. This determines the next steps.
- **Art style not decided.** The current model is untextured, flat-shaded, and lit with basic point lights.
- **Three.js MCP server not configured.** Candidate: `threejs-devtools-mcp` on npm (unverified). Add to `opencode.json` under `"mcp"` if wanted.
- **Mouse/keyboard controls not tested interactively.** Only a headless screenshot was checked.
- The interior of the reactor citadels is not modelled; they are solid cylinders.
- Ship text covers more areas (Spine, residential terraces, bridge) that are not modelled yet.

## Next steps (suggested)

1. Confirm the target engine/platform and art style.
2. Play the viewer and note any collision or lighting problems.
3. Add materials, textures, and more detail if the style calls for it.
4. Model additional areas (e.g., the Spine or a residential terrace), extending `build_engine_room.py` or adding new scripts.
