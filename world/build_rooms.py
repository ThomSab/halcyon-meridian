"""
Builds the rooms of the Halcyon Meridian that are not the Spine, and writes the zone manifest
for the world viewer.

Run headless:
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python build_rooms.py

Outputs (in this folder):
  rooms.glb     every room built at its world position (Blender coordinates, Z-up)
  zones.json    one entry per zone: bounds, colliders, spawn point, exit, lift flag, GLB placement

Zones are placed on a grid far from the Spine, so they never overlap it. The engine room is
not rebuilt here: its GLB and colliders come from ../engine_room and are moved into place.

Units are meters. Floors are at Z = 0 in every zone.
"""
import bpy
import json
import os

WORLD_DIR = r"C:\Users\jaspe\Documents\agentbox\world"
ENGINE_DIR = r"C:\Users\jaspe\Documents\agentbox\engine_room"
os.makedirs(WORLD_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

GRID_ORIGIN = (2000.0, -1000.0)
COL_STEP = 340.0
ROW_STEP = 240.0
DOOR_GAP = 2.4

MAT_CACHE = {}


def mat(name, rgb, rough=0.7, emit=0.0, metal=0.0):
    if name in MAT_CACHE:
        return MAT_CACHE[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit > 0:
        b.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        b.inputs["Emission Strength"].default_value = emit
    MAT_CACHE[name] = m
    return m


FLOOR = mat("Floor", (0.30, 0.30, 0.32), rough=0.9)
WALL = mat("Wall", (0.62, 0.66, 0.68), rough=0.8)
CEIL = mat("Ceiling", (0.80, 0.82, 0.84), rough=0.9)
LIGHT = mat("CeilingLight", (1.0, 0.95, 0.85), rough=0.4, emit=3.0)
RAIL = mat("Rail", (0.22, 0.30, 0.36), rough=0.5, metal=0.4)
WOOD = mat("Wood", (0.42, 0.28, 0.16), rough=0.7)
STALL = mat("Stall", (0.70, 0.45, 0.25), rough=0.7)
COUNTER = mat("Counter", (0.80, 0.78, 0.70), rough=0.5)
SEAT = mat("Seat", (0.18, 0.30, 0.45), rough=0.7)
STAGE = mat("Stage", (0.25, 0.14, 0.12), rough=0.8)
BED = mat("Bed", (0.92, 0.94, 0.96), rough=0.9)
DESK = mat("Desk", (0.50, 0.36, 0.22), rough=0.7)
BOARD = mat("Board", (0.12, 0.30, 0.22), rough=0.8)
SCREEN = mat("Screen", (0.45, 0.90, 1.0), rough=0.3, emit=1.2)
WINDOW = mat("Window", (0.70, 0.88, 1.0), rough=0.2, emit=1.5)
PLANTER = mat("Planter", (0.35, 0.25, 0.18), rough=0.9)
FOLIAGE = mat("Foliage", (0.20, 0.50, 0.24), rough=0.8)
TRUNK = mat("Trunk", (0.35, 0.22, 0.12), rough=0.9)
BENCH = mat("Bench", (0.45, 0.32, 0.20), rough=0.7)
STEEL = mat("Steel", (0.45, 0.46, 0.48), rough=0.4, metal=0.7)
CONSOLE = mat("Console", (0.20, 0.24, 0.30), rough=0.4)
CABIN_WOOD = mat("CabinWood", (0.55, 0.40, 0.28), rough=0.7)
LIFT_STEEL = mat("LiftSteel", (0.35, 0.37, 0.40), rough=0.4, metal=0.6)
LIFT_LIGHT = mat("LiftLight", (0.50, 0.80, 0.90), rough=0.3, emit=0.6)


class Room:
    """A zone built at (ox, oy). Local coordinates run from (0, 0) to (w, d)."""

    def __init__(self, zid, name, ox, oy, w, d, h, roof=True, wall_h=1.1, door_gap=False):
        self.zid = zid
        self.name = name
        self.ox, self.oy = ox, oy
        self.w, self.d, self.h = w, d, h
        self.roof = roof
        self.wall_h = h if roof else wall_h
        self.door_gap = door_gap
        self.colliders = []
        self.spawn = (w / 2, 2.0)
        self.exit = None          # (x, y, label, target)
        self.lift = False
        self.hall = None
        self.side = None
        self.objects = []

    # -- primitives (local coordinates in, world coordinates out) -----------------
    def box(self, name, x0, x1, y0, y1, z0, z1, m, collide=False):
        X0, X1 = self.ox + x0, self.ox + x1
        Y0, Y1 = self.oy + y0, self.oy + y1
        cx, cy, cz = (X0 + X1) / 2, (Y0 + Y1) / 2, (z0 + z1) / 2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
        o = bpy.context.active_object
        o.name = f"{self.zid}_{name}"
        o.scale = (X1 - X0, Y1 - Y0, z1 - z0)
        o.data.materials.append(m)
        self.objects.append(o)
        if collide:
            self.colliders.append({"type": "box", "min": [X0, Y0], "max": [X1, Y1]})
        return o

    def trunk(self, name, x, y, radius, height, m):
        """A post with a collider (used for trees and posts)."""
        self.box(name, x - radius, x + radius, y - radius, y + radius, 0, height, m, collide=True)

    def elevator(self, ex):
        """A lift cabin against the south wall at local x = ex. Arrive in front of it."""
        self.box("ElevatorCabin", ex - 1.2, ex + 1.2, 0.0, 1.3, 0, 2.6, LIFT_STEEL, collide=True)
        self.box("ElevatorDoor", ex - 1.0, ex + 1.0, 1.3, 1.36, 0.15, 2.45, LIFT_LIGHT)
        self.box("ElevatorSign", ex - 0.8, ex + 0.8, 1.3, 1.36, 2.5, 2.8, LIFT_LIGHT)

    # -- shell -------------------------------------------------------------------
    def shell(self):
        W, D, H = self.w, self.d, self.h
        self.box("Floor", 0, W, 0, D, -0.5, 0, FLOOR)
        if self.roof:
            self.box("Ceiling", 0, W, 0, D, H, H + 0.3, CEIL)
            self.box("CeilingLight", W / 2 - 2.5, W / 2 + 2.5, D / 2 - 1.0, D / 2 + 1.0, H - 0.03, H - 0.01,
                     LIGHT)
        wh = self.wall_h
        self.box("WallWest", -0.5, 0, -0.5, D + 0.5, 0, wh, WALL, collide=True)
        self.box("WallEast", W, W + 0.5, -0.5, D + 0.5, 0, wh, WALL, collide=True)
        self.box("WallNorth", -0.5, W + 0.5, D, D + 0.5, 0, wh, WALL, collide=True)
        if self.door_gap:
            g0 = W / 2 - DOOR_GAP / 2
            g1 = W / 2 + DOOR_GAP / 2
            self.box("WallSouthA", -0.5, g0, -0.5, 0, 0, H, WALL, collide=True)
            self.box("WallSouthB", g1, W + 0.5, -0.5, 0, 0, H, WALL, collide=True)
            self.box("Lintel", g0, g1, -0.5, 0, 3.0, H, WALL)
        else:
            self.box("WallSouth", -0.5, W + 0.5, -0.5, 0, 0, wh, WALL, collide=True)
        if not self.roof:
            # Open decks get a rail along the edge rather than a solid wall (no south gap)
            pass

    def to_json(self):
        ox, oy = self.ox, self.oy
        out = {
            "id": self.zid,
            "name": self.name,
            "glb": "rooms.glb",
            "glbOffset": [0.0, 0.0],
            "bounds": {"min": [ox, oy], "max": [ox + self.w, oy + self.d]},
            "colliders": self.colliders,
            "spawn": [ox + self.spawn[0], oy + self.spawn[1]],
            "lift": self.lift,
        }
        if self.exit:
            ex, ey, label, target = self.exit
            out["exit"] = {"x": ox + ex, "y": oy + ey, "label": label, "target": target,
                           "face": [ox + ex, oy + 0.6]}   # the elevator cabin sits on the south wall
        if self.hall is not None:
            out["hall"] = self.hall
            out["side"] = self.side
        return out


def grid_origin(index):
    col = index % 4
    row = index // 4
    return GRID_ORIGIN[0] + col * COL_STEP, GRID_ORIGIN[1] - row * ROW_STEP


ZONES = []

# ---- 0: Engine room (existing model; placed on the grid, see below) --------------
ENGINE_INDEX = 0

# ---- 1: Bow deck (open deck with rails) ----------------------------------------------
r = Room("bow_deck", "Bow Deck", *grid_origin(1), 150, 60, 0, roof=False, wall_h=1.1)
r.shell()
for i, x in enumerate([30, 60, 90, 120]):
    r.box(f"Bench_{i}", x, x + 2.2, 4, 4.6, 0, 0.5, BENCH, collide=True)
r.trunk("Capstan_1", 40, 30, 1.2, 1.1, STEEL)
r.trunk("Capstan_2", 110, 30, 1.2, 1.1, STEEL)
r.box("MastStub", 74, 76, 28, 32, 0, 12, STEEL, collide=True)
r.elevator(12)
r.spawn = (12, 4.0)
r.exit = (12, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 2: Solarium park (open, trees and benches) --------------------------------------
r = Room("solarium", "Solarium Park", *grid_origin(2), 200, 120, 0, roof=False, wall_h=1.1)
r.shell()
for i in range(6):
    for j in range(3):
        tx = 25 + i * 30
        ty = 25 + j * 35
        r.trunk(f"Tree_{i}_{j}", tx, ty, 0.3, 3.0, TRUNK)
        r.box(f"Canopy_{i}_{j}", tx - 1.6, tx + 1.6, ty - 1.6, ty + 1.6, 2.8, 4.6, FOLIAGE)
for i, x in enumerate([60, 120, 150]):
    r.box(f"Bench_{i}", x, x + 2.2, 100, 100.6, 0, 0.5, BENCH, collide=True)
r.elevator(10)
r.spawn = (10, 4.0)
r.exit = (10, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 3: Bridge ----------------------------------------------------------------------
r = Room("bridge", "Bridge", *grid_origin(3), 40, 20, 6, roof=True)
r.shell()
r.box("Windows", 2, 38, 19.85, 19.97, 2.4, 5.0, WINDOW)
r.box("Console", 6, 34, 13, 15.5, 0, 1.2, CONSOLE, collide=True)
r.box("CaptainChair", 19, 21, 16.5, 17.5, 0, 1.0, SEAT, collide=True)
r.elevator(20)
r.spawn = (20, 4.0)
r.exit = (20, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 4: Greenhouse ----------------------------------------------------------------
r = Room("greenhouse", "Greenhouse", *grid_origin(4), 80, 30, 6, roof=True)
r.shell()
for i, y in enumerate([6, 12, 18, 24]):
    r.box(f"Planter_{i}", 8, 72, y - 0.9, y + 0.9, 0, 0.9, PLANTER, collide=True)
    r.box(f"Plants_{i}", 8, 72, y - 0.7, y + 0.7, 0.9, 1.6, FOLIAGE)
r.elevator(4)
r.spawn = (4, 4.0)
r.exit = (4, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 5: Classroom -------------------------------------------------------------------
r = Room("classroom", "Classroom", *grid_origin(5), 30, 20, 4, roof=True)
r.shell()
for i, x in enumerate([6, 12, 18, 24]):
    for j, y in enumerate([6, 10, 14]):
        r.box(f"Desk_{i}_{j}", x, x + 2.4, y, y + 1.0, 0, 0.8, DESK, collide=True)
r.box("TeacherDesk", 13.5, 16.5, 17, 18.2, 0, 0.9, DESK, collide=True)
r.box("Board", 6, 24, 19.85, 19.97, 1.2, 3.2, BOARD)
r.elevator(15)
r.spawn = (15, 4.0)
r.exit = (15, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 6: Residential cabin -------------------------------------------------------------
r = Room("cabin", "Residential Cabin", *grid_origin(6), 10, 8, 3, roof=True, door_gap=True)
r.shell()
r.box("Bed", 6.4, 8.6, 5.2, 6.2, 0, 0.5, BED, collide=True)
r.box("Table", 1.5, 2.7, 4.6, 5.4, 0, 0.8, CABIN_WOOD, collide=True)
r.box("Wardrobe", 8.6, 9.4, 0.8, 2.6, 0, 2.2, CABIN_WOOD, collide=True)
r.box("Window", 2, 4.5, 7.85, 7.97, 1.3, 2.4, WINDOW)
r.elevator(2.2)
r.spawn = (2.2, 4.0)
r.exit = (2.2, 3.0, "Use the elevator", "menu")
r.lift = True
ZONES.append(r)

# ---- 7-11: Market halls and the Harbour Care ward (reached through the hall doors) --------
HALLS = [
    ("harbour_hall", "Harbour Hall", 16, "port"),
    ("commissary", "Commissary Canteen", 20, "stbd"),
    ("theatre", "Spine Theatre", 11, "stbd"),
    ("shift_hall", "Shift-Change Hall", 4, "stbd"),
    ("care_ward", "Harbour Care Ward", 0, "port"),
]
for n, (zid, name, hall, side) in enumerate(HALLS):
    r = Room(zid, name, *grid_origin(7 + n), 40, 8, 5, roof=True, door_gap=True)
    r.shell()
    r.hall = hall
    r.side = side
    r.spawn = (20, 1.6)
    r.exit = (20, 1.0, f"Leave {name}", f"hall:{hall}")
    ZONES.append(r)

harbour = next(z for z in ZONES if z.zid == "harbour_hall")
for i in range(6):
    x = 4 + i * 6
    harbour.box(f"Stall_{i}", x, x + 4, 6.0, 7.4, 0, 2.2, STALL, collide=True)
    harbour.box(f"StallTop_{i}", x, x + 4, 6.0, 7.4, 2.2, 2.4, WOOD)

commissary = next(z for z in ZONES if z.zid == "commissary")
commissary.box("Counter", 2, 38, 6.4, 7.6, 0, 1.1, COUNTER, collide=True)
for i, x in enumerate([6, 14, 26, 34]):
    commissary.box(f"Table_{i}", x, x + 3, 2.6, 3.4, 0, 0.9, WOOD, collide=True)

theatre = next(z for z in ZONES if z.zid == "theatre")
for row, y in enumerate([2.6, 3.7, 4.8]):
    for k, x in enumerate(range(4, 38, 2)):
        theatre.box(f"Seat_{row}_{k}", x, x + 1.4, y, y + 0.7, 0, 0.9, SEAT, collide=True)
theatre.box("Stage", 0.5, 39.5, 6.2, 7.9, 0, 1.0, STAGE, collide=True)
theatre.spawn = (20, 1.2)
theatre.exit = (20, 0.9, "Leave Spine Theatre", "hall:11")

shift = next(z for z in ZONES if z.zid == "shift_hall")
shift.box("QueueDesk", 16, 24, 3.0, 4.0, 0, 1.1, COUNTER, collide=True)
for i in range(7):
    x = 4 + i * 5
    shift.box(f"Terminal_{i}", x, x + 1.4, 6.6, 7.2, 0, 1.2, CONSOLE, collide=True)
    shift.box(f"TerminalScreen_{i}", x + 0.2, x + 1.2, 6.55, 6.6, 0.8, 1.1, SCREEN)

ward = next(z for z in ZONES if z.zid == "care_ward")
for row, y in enumerate([2.5, 5.5]):
    for i in range(8):
        x = 3 + i * 4.5
        ward.box(f"Bed_{row}_{i}", x, x + 2.2, y, y + 1.0, 0, 0.6, BED, collide=True)

# ---- 0: Engine room, moved onto the grid -----------------------------------------------
EX, EY = grid_origin(ENGINE_INDEX)
with open(os.path.join(ENGINE_DIR, "engine_room_colliders.json"), "r", encoding="utf-8") as f:
    engine_data = json.load(f)


def shift_collider(c):
    if c["type"] == "box":
        return {"type": "box", "min": [c["min"][0] + EX, c["min"][1] + EY],
                "max": [c["max"][0] + EX, c["max"][1] + EY]}
    return {"type": "circle", "center": [c["center"][0] + EX, c["center"][1] + EY], "radius": c["radius"]}


# A lift cabin against the engine room's west wall (x = 0). Added to rooms.glb at world coordinates.
engine_lift = Room("engine_lift", "", 0.0, 0.0, 1, 1, 1)
engine_lift.box("EngineElevatorCabin", EX, EX + 1.3, EY - 1.2, EY + 1.2, 0, 2.6, LIFT_STEEL, collide=True)
engine_lift.box("EngineElevatorDoor", EX + 1.3, EX + 1.36, EY - 1.0, EY + 1.0, 0.15, 2.45, LIFT_LIGHT)

engine_entry = {
    "id": "engine_room",
    "name": "Engine Room",
    "glb": "../engine_room/engine_room.glb",
    "glbOffset": [EX, EY],
    "bounds": {"min": [EX + engine_data["bounds"]["min"][0], EY + engine_data["bounds"]["min"][1]],
               "max": [EX + engine_data["bounds"]["max"][0], EY + engine_data["bounds"]["max"][1]]},
    "colliders": [shift_collider(c) for c in engine_data["colliders"]] + engine_lift.colliders,
    "spawn": [EX + 4.0, EY],
    "exit": {"x": EX + 3.2, "y": EY, "label": "Use the elevator", "target": "menu",
             "face": [EX + 0.65, EY]},   # the cabin sits on the west wall
    "lift": True,
}

# ---- Export rooms.glb ------------------------------------------------------------------
glb_path = os.path.join(WORLD_DIR, "rooms.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")

zones = [engine_entry] + [z.to_json() for z in ZONES]
json_path = os.path.join(WORLD_DIR, "zones.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"zones": zones}, f, indent=2)

print("EXPORTED", glb_path, "zones:", len(zones), "rooms:", len(ZONES))
