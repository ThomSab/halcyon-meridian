# Agentbox: Halcyon Meridian

Worldbuilding notes, a text adventure, 2D/SVG art, and low-poly 3D for the **Halcyon Meridian**, a 1,600 m nuclear-powered, wind-assisted city ship. The 3D parts are a walkable Spine with NPCs and the lore to discover, a walkable engine room, and an exterior overview of the whole ship.

## Contents

| Path | What it is |
|---|---|
| `lore/*.md` | Worldbuilding reference (60 files). Start with `lore/halcyon_meridian_general_description.md` and `lore/ship_structure_and_layout.md`. The Spine's NPCs say lines drawn from these files. |
| `halcyon_meridian_game.py` | Text adventure (Python 3, stdlib only). Run with `python halcyon_meridian_game.py`. |
| `halcyon_meridian_exterior.svg`, `halcyon_meridian_spine_interior.svg` | 2D artwork of the ship exterior and the Spine. |
| `spine/` | Walkable Spine (Deck 9): NPCs who talk and knock on doors, signs, a train, a journal, and a strip map. Blender build script, GLB, collision data, viewer, and `snippets.js` with the topic lines. |
| `engine_room/` | Walkable low-poly engine room: Blender build script, GLB, collision data, viewer. |
| `ship/` | Exterior overview of the whole ship with an orbit camera: Blender build script, GLB, viewer. |
| `world/` | The main game: every walkable zone in one page, connected by lifts and doors. Room build script, `rooms.glb`, `zones.json`, `index.html`. |
| `package.json`, `package-lock.json` | Node deps. Only `three` (0.187.0) is used, by the viewers. |

## Viewing

The viewers load files with `fetch` and ES modules, so they must be served over HTTP (opening the file directly won't work). From the repo root:

```powershell
python -m http.server 8000
```

- The ship (main game, all zones): http://localhost:8000/world/index.html
- The Spine only (earlier viewer): http://localhost:8000/spine/index.html
- Engine room (walk): http://localhost:8000/engine_room/index.html
- Ship overview (orbit): http://localhost:8000/ship/index.html

Run the server from the repo root so `node_modules/three` resolves. Dependencies: `npm install`.

## The ship (world viewer)

`world/index.html` is the main game: one page that holds every walkable zone.

- **Zones:** The Spine (the hub), the Engine Room, Bow Deck, Solarium Park, Bridge, Greenhouse, Classroom, Residential Cabin, and five rooms behind the market-hall doors (Harbour Hall, Commissary Canteen, Spine Theatre, Shift-Change Hall, Harbour Care Ward).
- **Getting around:** Use a lift on the Spine (E, at the lift shafts in the gaps between halls) to pick a level from the menu. Use a hall door (E) to go inside. Every room has an exit prompt that takes you back.
- **Transitions:** Zones are separate spaces joined by a short fade, not walked through continuously. The bow, the engine room, and the other decks are not physically connected to the Spine.
- **What carries over:** NPCs (Spine only), knocks on doors, signs, the train, the journal, and the lore discovery.

Rebuild the rooms (the Spine build also places the lifts):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "world\build_rooms.py"
```

`world/build_rooms.py` writes `rooms.glb` and `zones.json`. The rooms are placed on a grid far from the Spine, and the engine room is moved onto the same grid. Rooms are blockouts: boxes, rails, and simple props.

Debug parameters: `?zone=ID` (start in a zone), `?go=ID` (travel), `?back=1` (leave the current room), `?menu=1` (open the lift menu). Zone IDs: `engine_room`, `bow_deck`, `solarium`, `bridge`, `greenhouse`, `classroom`, `cabin`, `harbour_hall`, `commissary`, `theatre`, `shift_hall`, `care_ward`.

## The Spine (walkable)

Layout: aft tower at X = 0 to 100 m, fore tower at X = 1500 to 1600 m, Spine floor between them (X = 100 to 1500 m, 40 m wide, Z = 0 is the Deck 9 floor). Market halls line both sides, leaving a 22 m clear centre aisle, with awnings, lit fronts, and planters with trees in the gaps. Lamp posts line the aisle. The Spine is 1,400 m here, against about 1.5 km in the lore.

Controls: WASD/arrows to walk, Shift to run, mouse to look, Esc to release. E to talk or read a sign, J for the journal.

Nothing is handed over as a file to read. The lore comes out in the world:

- **NPCs (60):** walking the Spine, avoiding walls and the train. Press E near one to talk. Each NPC says a role line from a lore file, then short lines from two assigned topics, so each topic is said by at least two people. Repeat talks give the next line. The first time you hear a topic, a notice shows its title and the topic is added to the journal with the line you heard. Layout is seeded (`?seed=N`).
- **Knocks on doors:** every market hall has a door on each side. NPCs sometimes walk to a door and knock one of the six patterns from `lore/knock_codes_and_cabin_talk.md`. The light above the door flashes with each knock and you hear it. A subtitle shows the rhythm. Once you have heard the knock-codes topic, the subtitle also shows what the knock means.
- **Signs (5):** named places on hall fronts. E reads the sign, which counts as hearing its topic. Set in `POIS` in `build_spine.py`.
- **Journal (J):** the 60 topics, marked as heard (with the line you heard) or not yet found. The HUD shows how many you have heard. Progress is saved in the browser (localStorage) for this site.
- **Electric train:** shuttles along the centre track at 25 km/h (the lore's maximum), pausing 6 s at each end. It blocks the aisle; if it reaches you, you are pushed to the side of the track.
- **Strip map (top right):** the Spine as a bar, with signs (yellow), NPCs (grey), the train (blue), and your position (white).

Topic lines live in `spine/snippets.js`, one per lore file. They are short paraphrases of each file's opening points. Edit that file to change what people say.

Rebuild:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python "spine\build_spine.py"
```

URL parameters (for testing and screenshots):
- `?x=800&y=0&yaw=0`: start position in metres and heading (0 = fore, 90 = port)
- `?shot=1`: hide the start overlay
- `?talk=N`: stand next to NPC N and talk to them
- `?knock=1`: make NPC 0 knock on the first door right away
- `?open=N`: show sign N's text
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
- Lore moved into `lore/`. Lore is learned through NPC conversations and knocks on doors, not by reading files. A journal tracks what you have heard.
- NPCs walk the Spine, talk, and knock on doors.
- Whole-ship exterior overview.
- Headless screenshots and console checks for each viewer; no console errors.

Not done or not decided:
- **Game engine/platform is not decided.** Options are a browser game (Three.js or Babylon.js), Godot, or Unity. This determines the next steps.
- **Art style is not decided.** The models are untextured, flat-shaded blockouts.
- **Three.js MCP server not configured.** Candidate: `threejs-devtools-mcp` on npm (unverified). Add to `opencode.json` under `"mcp"` if wanted.
- **Interactions were not played by hand.** Walking, collisions, the train push-out, talking, and knocks were checked with headless screenshots, console logs, and a movement simulation. The E key itself was not pressed in a browser; the same functions run through `?talk=N` and `?knock=1`.
- The knock meaning and the flashing door light were checked from the code and one screenshot; the flashes are short, so they were not captured on screen.
- NPCs do not avoid the player, and they do not talk to each other.
- The lore snippets in `spine/snippets.js` are short paraphrases I wrote from each file's opening points. They have not been checked line by line against the full files.
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
