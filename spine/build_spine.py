"""
Builds a blockout of the Spine (Deck 9) of the Halcyon Meridian and exports it as GLB.

Run headless:
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python build_spine.py

Units are meters. Blender is Z-up; the glTF exporter converts to Y-up.
Blender axes: X = along the ship (aft at 0, fore at 1600), Y = port/starboard (centre 0), Z = up.
Deck 9 (Spine floor) is at Z = 0.

Layout (from lore/ship_structure_and_layout.md, simplified):
  - Spine: central boulevard, 40 m wide, about 1.4 km long between the two towers.
  - Residential towers: one forward and one aft, closing each end of the Spine.
  - Market halls: blocks lining both sides, with awnings and lit fronts.
  - Planters with trees in the gaps between halls.
  - Electric rail track down the centre, with lamp posts along the aisle.
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


def make_mat(name, rgb, rough=0.7, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit > 0:
        bsdf.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit
    return m


MAT = {
    "deck":      make_mat("Deck",      (0.42, 0.40, 0.36), rough=0.9),
    "tower":     make_mat("Tower",     (0.75, 0.77, 0.80), rough=0.6),
    "hall":      make_mat("Hall",      (0.60, 0.50, 0.40), rough=0.7),
    "rail":      make_mat("Rail",      (0.20, 0.30, 0.35), rough=0.5, metal=0.4),
    "steel":     make_mat("Steel",     (0.45, 0.46, 0.48), rough=0.4, metal=0.7),
    "wood":      make_mat("Sleeper",   (0.30, 0.22, 0.14), rough=0.9),
    "pole":      make_mat("Pole",      (0.25, 0.25, 0.27), rough=0.5, metal=0.5),
    "lamp":      make_mat("Lamp",      (1.0, 0.92, 0.75), rough=0.3, emit=6.0),
    "planter":   make_mat("Planter",   (0.35, 0.25, 0.18), rough=0.9),
    "foliage":   make_mat("Foliage",   (0.20, 0.45, 0.22), rough=0.8),
    "awn_red":   make_mat("AwningRed", (0.60, 0.20, 0.18), rough=0.8),
    "awn_cream": make_mat("AwningCream", (0.85, 0.80, 0.65), rough=0.8),
    "awn_teal":  make_mat("AwningTeal", (0.20, 0.50, 0.50), rough=0.8),
    "hall_lit":  make_mat("HallFront", (1.0, 0.70, 0.40), rough=0.5, emit=0.5),
    "tower_win": make_mat("TowerWindow", (0.70, 0.85, 1.0), rough=0.3, emit=1.5),
    "poi":       make_mat("PoiSign",   (1.0, 0.82, 0.25), rough=0.4, emit=0.8),
}

# Points of interest. "hall" is the index of the market hall (0 = aft end, hall spacing 60 m).
# Text is paraphrased from the lore files named in "source".
POIS = [
    {"name": "Harbour Care Complex", "hall": 0, "side": "port",
     "text": "Buildings at the aft end of the Spine with about 500 staff: nurses, carers, "
             "physiotherapists and social workers. Palliative patients can see the Spine's skylights.",
     "source": "lore/elder_care_and_end_of_life.md"},
    {"name": "Shift-Change Hall", "hall": 4, "side": "stbd",
     "text": "A large communal room next to the rail station. Rows of terminals and a queue desk, "
             "where batch clerks handle residents' messages. Busiest at shift changes.",
     "source": "lore/batch_clerks_message_runners.md"},
    {"name": "Spine Theatre", "hall": 11, "side": "stbd",
     "text": "On the Spine's central concourse. Seats about 1,200 people for plays, concerts and dance, "
             "with performers drawn from residents.",
     "source": "lore/arts_media_and_entertainment.md"},
    {"name": "Harbour Hall", "hall": 16, "side": "port",
     "text": "A market for port goods and imports, including clothing and fabric. About 60 tailors and "
             "seamstresses work here and in the terrace community rooms. The Landfall Festival market is held here.",
     "source": "lore/clothing_textiles_and_laundry.md"},
    {"name": "Commissary Canteen", "hall": 20, "side": "stbd",
     "text": "Part of the Commissary, which runs about 60 kitchens and canteens across the terraces "
             "and the Spine. Each adult receives a meal allowance on their ledger account.",
     "source": "lore/food_and_agriculture.md"},
]

AWNINGS = [MAT["awn_red"], MAT["awn_cream"], MAT["awn_teal"]]

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


def pole(name, x, y, z0, z1, radius, mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=radius, depth=z1 - z0,
                                        location=(x, y, (z0 + z1) / 2))
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    return o


def ball(name, x, y, z, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=radius, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    return o


# --- Spine deck (walkable floor) ------------------------------------------------
box("Spine_Deck", SPINE_X0, SPINE_X1, -SPINE_HALF_WIDTH, SPINE_HALF_WIDTH, -0.5, 0.0, MAT["deck"])

# --- Forward and aft residential towers ----------------------------------------
box("Tower_Aft", 0, TOWER_LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, 0, TOWER_HEIGHT,
    MAT["tower"], collide=True)
box("Tower_Fore", SHIP_LENGTH - TOWER_LENGTH, SHIP_LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, 0,
    TOWER_HEIGHT, MAT["tower"], collide=True)

# Lit window bands on the faces that look onto the Spine
for z in range(6, int(TOWER_HEIGHT) - 4, 9):
    box(f"Win_Aft_{z}", TOWER_LENGTH, TOWER_LENGTH + 0.25, -28, 28, z, z + 3, MAT["tower_win"])
    box(f"Win_Fore_{z}", SHIP_LENGTH - TOWER_LENGTH - 0.25, SHIP_LENGTH - TOWER_LENGTH, -28, 28, z, z + 3,
        MAT["tower_win"])

# --- Low rails along both edges of the Spine -----------------------------------
box("Rail_Port", SPINE_X0, SPINE_X1, -SPINE_HALF_WIDTH - 0.3, -SPINE_HALF_WIDTH, 0, RAIL_HEIGHT,
    MAT["rail"], collide=True)
box("Rail_Stbd", SPINE_X0, SPINE_X1, SPINE_HALF_WIDTH, SPINE_HALF_WIDTH + 0.3, 0, RAIL_HEIGHT,
    MAT["rail"], collide=True)

# --- Electric rail track down the centre ---------------------------------------
for side, y in (("Port", -0.72), ("Stbd", 0.72)):
    box(f"Track_{side}", SPINE_X0, SPINE_X1, y - 0.035, y + 0.035, 0, 0.15, MAT["steel"])
x = SPINE_X0
i = 0
while x + 0.3 <= SPINE_X1:
    box(f"Sleeper_{i}", x, x + 0.3, -1.0, 1.0, -0.02, 0.08, MAT["wood"])
    x += 4.0
    i += 1

# --- Market halls, awnings, lit fronts, planters ------------------------------
HALL_LEN = 40.0
HALL_GAP = 20.0
HALL_INNER = 11.0     # inner face of the hall, measured from centre
HALL_OUTER = 19.0     # outer face, a little inside the rail
hall_index = 0
x = SPINE_X0 + 20.0
while x + HALL_LEN <= SPINE_X1 - 20.0:
    height = 7.0 if hall_index % 2 == 0 else 9.0
    x0, x1 = x, x + HALL_LEN
    box(f"Hall_Port_{hall_index}", x0, x1, -HALL_OUTER, -HALL_INNER, 0, height, MAT["hall"], collide=True)
    box(f"Hall_Stbd_{hall_index}", x0, x1, HALL_INNER, HALL_OUTER, 0, height, MAT["hall"], collide=True)

    awning = AWNINGS[hall_index % len(AWNINGS)]
    box(f"Awning_Port_{hall_index}", x0, x1, -HALL_INNER, -9.0, 3.0, 3.4, awning)
    box(f"Awning_Stbd_{hall_index}", x0, x1, 9.0, HALL_INNER, 3.0, 3.4, awning)

    box(f"HallFront_Port_{hall_index}", x0 + 3, x1 - 3, -HALL_INNER - 0.08, -HALL_INNER + 0.02, 1.0,
        height - 1.5, MAT["hall_lit"])
    box(f"HallFront_Stbd_{hall_index}", x0 + 3, x1 - 3, HALL_INNER - 0.02, HALL_INNER + 0.08, 1.0,
        height - 1.5, MAT["hall_lit"])

    hall_index += 1
    x += HALL_LEN + HALL_GAP

# Point-of-interest signs on the hall fronts (yellow boards, facing the aisle)
poi_records = []
for poi in POIS:
    x0 = SPINE_X0 + 20.0 + poi["hall"] * (HALL_LEN + HALL_GAP)
    x1 = x0 + HALL_LEN
    cx = (x0 + x1) / 2
    if poi["side"] == "port":
        y = -7.0
        box(f"Sign_{poi['hall']}", x0 + 8, x1 - 8, -10.98, -10.86, 4.0, 5.0, MAT["poi"])
    else:
        y = 7.0
        box(f"Sign_{poi['hall']}", x0 + 8, x1 - 8, 10.86, 10.98, 4.0, 5.0, MAT["poi"])
    poi_records.append({"name": poi["name"], "text": poi["text"], "source": poi["source"],
                        "x": cx, "y": y})

# Planters with trees in the gaps between halls
# Lifts sit in two of the gaps between halls (gap k is centred at x = 170 + 60k).
# Gap 10 (x = 770, port) and gap 18 (x = 1250, starboard) become lift shafts instead of planters.
LIFT_GAPS = {10: ("Port", -15.0), 18: ("Stbd", 15.0)}
lifts = []
planter_index = 0
gap_x = SPINE_X0 + 20.0 + HALL_LEN
while gap_x + HALL_GAP <= SPINE_X1 - 20.0 + 0.1:
    cx = gap_x + HALL_GAP / 2
    if planter_index in LIFT_GAPS:
        side, y = LIFT_GAPS[planter_index]
        sign = -1.0 if y < 0 else 1.0
        box(f"Lift_{side}_{planter_index}", cx - 2.0, cx + 2.0, y - 4.0, y + 4.0, 0, 4.2, MAT["pole"], collide=True)
        # Lift doors face the aisle; a glowing panel shows the lift is in use
        box(f"LiftDoor_{side}_{planter_index}", cx - 1.6, cx + 1.6, -11.12 if sign < 0 else 10.9,
            -10.9 if sign < 0 else 11.12, 0.4, 3.6, MAT["poi"])
        lifts.append({"name": f"Lift {side}", "x": cx, "y": y, "stance": [cx, -9.0 if sign < 0 else 9.0]})
    else:
        for side, y in (("Port", -15.0), ("Stbd", 15.0)):
            box(f"Planter_{side}_{planter_index}", cx - 1.5, cx + 1.5, y - 1.0, y + 1.0, 0, 1.0,
                MAT["planter"], collide=True)
            ball(f"Tree_{side}_{planter_index}", cx, y, 2.3, 1.3, MAT["foliage"])
    planter_index += 1
    gap_x += HALL_LEN + HALL_GAP

# --- Lamp posts along the centre aisle -----------------------------------------
lamp_index = 0
x = SPINE_X0 + 20.0
while x <= SPINE_X1 - 20.0:
    for side, y in (("Port", -4.0), ("Stbd", 4.0)):
        pole(f"LampPole_{side}_{lamp_index}", x, y, 0, 4.5, 0.08, MAT["pole"])
        colliders.append({"type": "circle", "center": [x, y], "radius": 0.08})
        box(f"LampHead_{side}_{lamp_index}", x - 0.25, x + 0.25, y - 0.25, y + 0.25, 4.5, 4.9, MAT["lamp"])
    lamp_index += 1
    x += 40.0

# --- Cabin doors on the hall fronts, with a knock light above each -------------
# Each hall has one door per side. The light is a separate material so the viewer can flash it
# when an NPC knocks. The door stands just in front of the hall face (toward the aisle).
DOOR_MAT = make_mat("Door", (0.36, 0.24, 0.16), rough=0.7)
door_records = []
x = SPINE_X0 + 20.0
hall_k = 0
while x + HALL_LEN <= SPINE_X1 - 20.0:
    cx = x + HALL_LEN / 2
    # Port door sits at Y -10.96 .. -10.82, stbd at 10.82 .. 10.96 (just in front of the hall face).
    for side, face_y, y0, y1 in (("port", -10.9, -10.96, -10.82),
                                 ("stbd", 10.9, 10.82, 10.96)):
        box(f"Door_{side}_{hall_k}", cx - 1.0, cx + 1.0, y0, y1, 0.0, 2.2, DOOR_MAT)
        light_mat = make_mat(f"DoorLight_{side}_{hall_k}", (1.0, 0.85, 0.5), rough=0.5, emit=0.05)
        box(f"DoorLight_{side}_{hall_k}", cx - 0.3, cx + 0.3, y0, y1, 2.35, 2.6, light_mat)
        door_records.append({"name": f"Door_{side}_{hall_k}", "light": f"DoorLight_{side}_{hall_k}",
                             "side": side, "x": cx, "y": face_y})
    hall_k += 1
    x += HALL_LEN + HALL_GAP

# --- Electric train on the centre track ----------------------------------------
# Three cars parented to an empty named "Train". The viewer moves the empty along X.
# The train's rear (aft) end is at X = 0 in this model; cars are 22 m long, 1.5 m gap.
TRAIN_CAR_LEN = 22.0
TRAIN_GAP = 1.5
TRAIN_CARS = 3
TRAIN_LENGTH = TRAIN_CARS * TRAIN_CAR_LEN + (TRAIN_CARS - 1) * TRAIN_GAP   # 69 m

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
train_root = bpy.context.active_object
train_root.name = "Train"

for i in range(TRAIN_CARS):
    x0 = i * (TRAIN_CAR_LEN + TRAIN_GAP)
    body = box(f"TrainCar_{i}", x0, x0 + TRAIN_CAR_LEN, -1.5, 1.5, 0.15, 3.55, make_mat(f"TrainBody_{i}", (0.15, 0.35, 0.55), rough=0.4))
    windows = box(f"TrainWindows_{i}", x0 + 1.0, x0 + TRAIN_CAR_LEN - 1.0, -1.56, 1.56, 1.6, 2.6, MAT["tower_win"])
    roof = box(f"TrainRoof_{i}", x0, x0 + TRAIN_CAR_LEN, -1.5, 1.5, 3.55, 3.7, MAT["steel"])
    for part in (body, windows, roof):
        part.parent = train_root

# --- Aft elevator: where the player spawns, in the gap between the aft tower and hall 0 ---
box("Lift_Aft", 104.0, 116.0, -19.0, -11.0, 0, 4.2, MAT["pole"], collide=True)
box("LiftDoor_Aft", 106.4, 113.6, -11.12, -10.9, 0.4, 3.6, MAT["poi"])
lifts.append({"name": "Lift Aft", "x": 110.0, "y": -15.0, "stance": [110.0, -9.0]})
# --- Export ---------------------------------------------------------------------
glb_path = os.path.join(OUT_DIR, "spine.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")

json_path = os.path.join(OUT_DIR, "spine_colliders.json")
with open(json_path, "w") as f:
    json.dump({
        "bounds": {"min": [SPINE_X0, -SPINE_HALF_WIDTH], "max": [SPINE_X1, SPINE_HALF_WIDTH]},
        "spine": {"x0": SPINE_X0, "x1": SPINE_X1, "length": SPINE_X1 - SPINE_X0},
        "pois": poi_records,
        "doors": door_records,
        "lifts": lifts,
        "train": {"length": TRAIN_LENGTH, "half_width": 1.5, "speed": 6.94},
        "colliders": colliders,
    }, f, indent=2)

print("EXPORTED", glb_path, "halls:", hall_index, "doors:", len(door_records), "planters:", planter_index,
      "lamps:", lamp_index, "colliders:", len(colliders))
