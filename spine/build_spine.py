"""
Builds a rudimentary blockout of the Spine (Deck 9) of the Halcyon Meridian and exports it as GLB.

Run headless:
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python build_spine.py

Units are meters. Blender is Z-up; the glTF exporter converts to Y-up.
Blender axes: X = along the ship (aft at 0, fore at 1600), Y = port/starboard (centre 0), Z = up.
Deck 9 (Spine floor) is at Z = 0.

Layout (from lore/ship_structure_and_layout.md, simplified):
  - Spine: central boulevard, 40 m wide, about 1.4 km long between the two towers.
  - Residential towers: one forward and one aft, closing each end of the Spine.
  - Market halls: blocks lining both sides of the Spine.
  - Low rails along both edges of the Spine.

Also writes spine_colliders.json for the web viewer.
"""
import bpy
import json
import os

OUT_DIR = r"C:\Users\jaspe\Documents\agentbox\spine"
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

SHIP_LENGTH = 1600.0
SPINE_HALF_WIDTH = 20.0
TOWER_LENGTH = 100.0
TOWER_HALF_WIDTH = 30.0
TOWER_HEIGHT = 90.0
RAIL_HEIGHT = 1.2
SPINE_X0 = TOWER_LENGTH
SPINE_X1 = SHIP_LENGTH - TOWER_LENGTH


def make_mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m


MAT = {
    "deck":   make_mat("Deck",   (0.42, 0.40, 0.36), rough=0.9),
    "tower":  make_mat("Tower",  (0.75, 0.77, 0.80), rough=0.6),
    "hall":   make_mat("Hall",   (0.60, 0.50, 0.40), rough=0.7),
    "rail":   make_mat("Rail",   (0.20, 0.30, 0.35), rough=0.5, metal=0.4),
}

colliders = []


def box(name, x0, x1, y0, y1, z0, z1, mat, collide=False):
    """Axis-aligned box from min/max corners."""
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    sx, sy, sz = x1 - x0, y1 - y0, z1 - z0
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx, sy, sz)
    o.data.materials.append(mat)
    if collide:
        colliders.append({"type": "box", "min": [x0, y0], "max": [x1, y1]})
    return o


# --- Spine deck (walkable floor) ------------------------------------------------
box("Spine_Deck", SPINE_X0, SPINE_X1, -SPINE_HALF_WIDTH, SPINE_HALF_WIDTH, -0.5, 0.0, MAT["deck"])

# --- Forward and aft residential towers ----------------------------------------
box("Tower_Aft", 0, TOWER_LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, 0, TOWER_HEIGHT,
    MAT["tower"], collide=True)
box("Tower_Fore", SHIP_LENGTH - TOWER_LENGTH, SHIP_LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, 0,
    TOWER_HEIGHT, MAT["tower"], collide=True)

# --- Low rails along both edges of the Spine -----------------------------------
box("Rail_Port", SPINE_X0, SPINE_X1, -SPINE_HALF_WIDTH - 0.3, -SPINE_HALF_WIDTH, 0, RAIL_HEIGHT,
    MAT["rail"], collide=True)
box("Rail_Stbd", SPINE_X0, SPINE_X1, SPINE_HALF_WIDTH, SPINE_HALF_WIDTH + 0.3, 0, RAIL_HEIGHT,
    MAT["rail"], collide=True)

# --- Market halls lining both sides ---------------------------------------------
# Blocks sit between the rail and an inner aisle, with gaps for side streets.
HALL_LEN = 40.0
HALL_GAP = 20.0
HALL_INNER = 11.0     # inner face of the hall, measured from centre
HALL_OUTER = 19.0     # outer face, a little inside the rail
hall_index = 0
x = SPINE_X0 + 20.0
while x + HALL_LEN <= SPINE_X1 - 20.0:
    height = 7.0 if hall_index % 2 == 0 else 9.0
    box(f"Hall_Port_{hall_index}", x, x + HALL_LEN, -HALL_OUTER, -HALL_INNER, 0, height,
        MAT["hall"], collide=True)
    box(f"Hall_Stbd_{hall_index}", x, x + HALL_LEN, HALL_INNER, HALL_OUTER, 0, height,
        MAT["hall"], collide=True)
    hall_index += 1
    x += HALL_LEN + HALL_GAP

# --- Export ---------------------------------------------------------------------
glb_path = os.path.join(OUT_DIR, "spine.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")

json_path = os.path.join(OUT_DIR, "spine_colliders.json")
with open(json_path, "w") as f:
    json.dump({
        "bounds": {"min": [SPINE_X0, -SPINE_HALF_WIDTH], "max": [SPINE_X1, SPINE_HALF_WIDTH]},
        "spine": {"x0": SPINE_X0, "x1": SPINE_X1, "length": SPINE_X1 - SPINE_X0},
        "colliders": colliders,
    }, f, indent=2)

print("EXPORTED", glb_path, "halls:", hall_index, "colliders:", len(colliders))
