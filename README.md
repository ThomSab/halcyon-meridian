# Agentbox: Halcyon Meridian

Worldbuilding notes, a text adventure, 2D/SVG art, and low-poly 3D for the **Halcyon Meridian**, a 1,600 m nuclear-powered, wind-assisted city ship. The 3D parts are a walkable Spine with NPCs and the lore to discover, a walkable engine room, and an exterior overview of the whole ship.

## Contents

| Path | What it is |
|---|---|
| `lore/*.md` | Worldbuilding reference (60 files). Start with `lore/halcyon_meridian_general_description.md` and `lore/ship_structure_and_layout.md`. The Spine's lore terminals open these files. |
| `halcyon_meridian_game.py` | Text adventure (Python 3, stdlib only). Run with `python halcyon_meridian_game.py`. |
| `halcyon_meridian_exterior.svg`, `halcyon_meridian_spine_interior.svg` | 2D artwork of the ship exterior and the Spine. |
| `spine/` | Walkable Spine (Deck 9): lore terminals, NPCs, points of interest, a train, and a strip map. Blender build script, GLB, collision data, viewer. |
| `engine_room/` | Walkable low-poly engine room: Blender build script, GLB, collision data, viewer. |
| `ship/` | Exterior overview of the whole ship with an orbit camera: Blender build script, GLB, viewer. |
| `package.json`, `package-lock.json` | Node deps. Only `three` (0.187.0) is used, by the viewers. |

## Viewing

The viewers load files with `fetch` and ES modules, so they must be served over HTTP (opening the file directly won't work). From the repo root:

```powershell
python -m http.server 8000
```

- The Spine (walk): http://localhost:8000/spine/index.html
- Engine room (walk): http://localhost:8000/engine_room/index.html
- Ship overview (orbit): http://localhost:8000/ship/index.html

Run the server from the repo root so `node_modules/three` resolves. Dependencies: `npm install`.

## The Spine (walkable)

Layout: aft tower at X = 0 to 100 m, fore tower at X = 1500 to 1600 m, Spine floor between them (X = 100 to 1500 m, 40 m wide, Z = 0 is the Deck 9 floor). Market halls line both sides, leaving a 22 m clear centre aisle, with awnings, lit fronts, and planters with trees in the gaps. Lamp posts line the aisle. The Spine is 1,400 m here, against about 1.5 km in the lore.

Controls: WASD/arrows to walk, Shift to run, mouse to look, Esc to release. E to interact, J for the journal.

- **Lore terminals (60):** one glowing terminal per lore file, along the aisle. Press E to read the file. Each read marks the entry as found; the HUD and journal show progress. Found entries are saved in the browser (localStorage) for this site.
- **Points of interest (5):** named places with a short text taken from the lore. Set in `POIS` in `build_spine.py`.
- **NPCs (60):** walking the Spine, avoiding walls and the train. Each has a role and a line paraphrased from a lore file. Press E near one to talk. The layout is seeded (`?seed=N`).
- **Electric train:** shuttles along the centre track at 25 km/h (the lore's maximum), pausing 6 s at each end. It blocks the aisle; if it reaches you, you are pushed to the side of the track.
- **Strip map (top right):** the Spine as a bar, with terminals (cyan), points of interest (yellow), NPCs (grey), the train (blue), and your position (white).

Rebuild:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "spine\build_spine.py"
```

The build script reads the lore folder, so adding or removing lore files changes the number of terminals (the Spine must have room for them: about 22 m per terminal).

URL parameters (for testing and screenshots):
- `?x=800&y=0&yaw=0`: start position in metres and heading (0 = fore, 90 = port)
- `?shot=1`: hide the start overlay
- `?read=N`: open lore terminal N
- `?open=N`: open point of interest N
- `?journal=1`: open the journal
- `?train=600`: place the train at X = 600 m and hold it
- `?seed=N`: NPC layout seed

## Ship overview

`ship/build_ship.py` builds the whole ship as a blockout from the lore dimensions: 1,600 m long, 320 m beam, a hull with tapered bow and stern, residential terraces with a stepped upper level, towers at each end, a central superstructure with a bridge tower (about 150 m above the waterline), and 36 wingsails in two rows of 18 (110 m tall). The sea is a large plane. It's a blockout, not to scale for the details. The viewer uses an orbit camera.

Rebuild:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "ship\build_ship.py"
```

## Engine room

- `engine_room/build_engine_room.py`: Blender script that builds the room and exports `engine_room.glb` and `engine_room_colliders.json`. Units are meters. Blender is Z-up, and the glTF exporter converts to Y-up.
- `engine_room/index.html`: first-person viewer. Click to start, WASD/arrows to move, Shift to run, mouse to look, Esc to release.

Rebuild:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "engine_room\build_engine_room.py"
```

Layout (Blender coordinates: X along the ship from aft at 0, Y port/starboard with centre at 0, Z up with floor at 0): room is 120 x 40 x 14 m.
- Four reactor citadels (radius 6 m) on the centerline at X = 22, 47, 72, 97. They block the centre aisle, so walk the port or starboard aisle.
- Six pod thruster motors at the aft end (X about 9).
- Switchboards along both side walls, X = 30 to 66.
- Coolant pipes overhead, control room cabin at the fore end (X about 102 to 120, Y -20 to -10).
- Overhead catwalks at Z = 6 (no collision).

The viewer's start position is in the port aisle at Blender (20, -12).

## Status and open questions

Done:
- Blender 5.3 installed and verified headless.
- Lore moved into `lore/`. The Spine has a terminal for every lore file, a journal, and discovery saved in the browser.
- NPCs walk the Spine with lore-based lines.
- Whole-ship exterior overview.
- Headless screenshots and console checks for each viewer; no console errors.

Not done or not decided:
- **Game engine/platform is not decided.** Options are a browser game (Three.js or Babylon.js), Godot, or Unity. This determines the next steps.
- **Art style is not decided.** The models are untextured, flat-shaded blockouts.
- **Three.js MCP server not configured.** Candidate: `threejs-devtools-mcp` on npm (unverified). Add to `opencode.json` under `"mcp"` if wanted.
- **Interactions were not played by hand.** Walking, collisions, the train push-out, the E panels, and NPC conversations were checked with headless screenshots and a movement simulation. The lore panels were checked with `?read=N` and `?journal=1`, which use the same code path as E.
- NPCs do not avoid the player, and they do not talk to each other.
- The Spine is 1,400 m and not 1.5 km. Towers are plain boxes.
- The Spine GLB is about 1.3 MB because each sleeper, tree, and lamp is its own mesh; merging them would reduce this.
- The reactor citadels are solid cylinders.
- The overview's towers and superstructure are blockouts and do not match the Spine's exact footprints beyond the towers.

## Next steps (suggested)

1. Confirm the target engine/platform and art style.
2. Play the Spine and note collision, lighting, and NPC problems.
3. Add textures and detail if the style calls for it.
4. Model the residential terraces and the bridge, following `spine/build_spine.py`.
5. Give NPCs a little more life: stop-and-look behaviour, a route along the rail platforms, and reactions to the player.
