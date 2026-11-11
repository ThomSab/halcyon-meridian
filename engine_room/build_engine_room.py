"""
Builds a low-poly engine room for the Halcyon Meridian and exports it as GLB.

Run headless:
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python build_engine_room.py

Units are meters. Blender is Z-up; the glTF exporter converts to Y-up.
Blender axes: X = along the ship (aft at 0, fore at 120), Y = port/starboard (centre 0), Z = up (floor at 0).

Also writes engine_room_colliders.json (used by the web viewer for walking collision).
"""
import bpy
import math
import json
import os

OUT_DIR = r"C:\Users\jaspe\Documents\agentbox\engine_room"
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

# Room dimensions
LENGTH = 120.0   # X
WIDTH = 40.0     # Y (-20 .. 20)
HEIGHT = 14.0    # Z


def make_mat(name, rgb, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m


MAT = {
    "floor":    make_mat("Floor",    (0.12, 0.12, 0.13), rough=0.9),
    "wall":     make_mat("Wall",     (0.55, 0.60, 0.63), rough=0.8),
    "reactor":  make_mat("Reactor",  (0.70, 0.50, 0.25), rough=0.45, metal=0.6),
    "switch":   make_mat("Switchboard", (0.10, 0.20, 0.35), rough=0.5),
    "coolant":  make_mat("Coolant",  (0.70, 0.18, 0.10), rough=0.4, metal=0.3),
    "motor":    make_mat("PodMotor", (0.45, 0.47, 0.52), rough=0.5, metal=0.5),
    "catwalk":  make_mat("Catwalk",  (0.25, 0.25, 0.27), rough=0.7),
}

colliders = []


def box(name, center, size, mat, collide=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    o.data.materials.append(mat)
    if collide:
        cx, cy = center[0], center[1]
        sx, sy = size[0], size[1]
        colliders.append({"type": "box",
                          "min": [cx - sx / 2, cy - sy / 2],
                          "max": [cx + sx / 2, cy + sy / 2]})
    return o


def cylinder(name, center, radius, depth, mat, axis="z", verts=16, collide=False):
    rot = {
        "z": (0.0, 0.0, 0.0),
        "x": (0.0, math.radians(90), 0.0),
        "y": (math.radians(90), 0.0, 0.0),
    }[axis]
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=center, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    if collide and axis == "z":
        colliders.append({"type": "circle", "center": [center[0], center[1]], "radius": radius})
    return o


# --- Shell -------------------------------------------------------------------
box("Floor", (LENGTH / 2, 0, -0.25), (LENGTH, WIDTH, 0.5), MAT["floor"])
box("Ceiling", (LENGTH / 2, 0, HEIGHT + 0.25), (LENGTH, WIDTH, 0.5), MAT["wall"])
box("Wall_Port", (LENGTH / 2, -WIDTH / 2 - 0.25, HEIGHT / 2), (LENGTH, 0.5, HEIGHT), MAT["wall"])
box("Wall_Stbd", (LENGTH / 2, WIDTH / 2 + 0.25, HEIGHT / 2), (LENGTH, 0.5, HEIGHT), MAT["wall"])
box("Wall_Aft", (-0.25, 0, HEIGHT / 2), (0.5, WIDTH, HEIGHT), MAT["wall"])
box("Wall_Fore", (LENGTH + 0.25, 0, HEIGHT / 2), (0.5, WIDTH, HEIGHT), MAT["wall"])

# --- Four reactor citadels (shielded cylinders) -------------------------------
for i, x in enumerate([22, 47, 72, 97]):
    cylinder(f"Reactor_{i + 1}", (x, 0, 6.5), 6.0, 13.0, MAT["reactor"],
             verts=24, collide=True)

# --- Six pod thruster motors at the aft end -----------------------------------
for i, y in enumerate([-14, -8.5, -3, 3, 8.5, 14]):
    cylinder(f"PodMotor_{i + 1}", (9, y, 4), 2.4, 8.0, MAT["motor"], axis="x", verts=12)
    colliders.append({"type": "box", "min": [5, y - 2.4], "max": [13, y + 2.4]})

# --- Switchboards along both side walls ---------------------------------------
for x in range(30, 68, 4):
    box(f"Switchboard_Port_{x}", (x, -19, 1.1), (2.4, 0.9, 2.2), MAT["switch"], collide=True)
    box(f"Switchboard_Stbd_{x}", (x, 19, 1.1), (2.4, 0.9, 2.2), MAT["switch"], collide=True)

# --- Coolant and service pipes -------------------------------------------------
cylinder("Pipe_Port_Upper", (LENGTH / 2, -17, 12), 0.4, LENGTH, MAT["coolant"], axis="x", verts=8)
cylinder("Pipe_Stbd_Upper", (LENGTH / 2, 17, 12), 0.4, LENGTH, MAT["coolant"], axis="x", verts=8)
cylinder("Pipe_Port_Lower", (LENGTH / 2, -17, 10), 0.25, LENGTH, MAT["coolant"], axis="x", verts=8)
cylinder("Pipe_Stbd_Lower", (LENGTH / 2, 17, 10), 0.25, LENGTH, MAT["coolant"], axis="x", verts=8)

# --- Control room cabin at the fore end ---------------------------------------
box("ControlRoom_Front", (108, -15, 2), (0.4, 10, 4), MAT["wall"], collide=True)
box("ControlRoom_Side", (114, -10, 2), (12, 0.4, 4), MAT["wall"], collide=True)

# --- Overhead catwalks (no collision, sit above head height) ------------------
box("Catwalk_Port", (LENGTH / 2, -17, 6), (LENGTH, 2, 0.3), MAT["catwalk"])
box("Catwalk_Stbd", (LENGTH / 2, 17, 6), (LENGTH, 2, 0.3), MAT["catwalk"])

# --- Export --------------------------------------------------------------------
glb_path = os.path.join(OUT_DIR, "engine_room.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")

json_path = os.path.join(OUT_DIR, "engine_room_colliders.json")
with open(json_path, "w") as f:
    json.dump({
        "bounds": {"min": [0, -WIDTH / 2], "max": [LENGTH, WIDTH / 2]},
        "colliders": colliders,
    }, f, indent=2)

print("EXPORTED", glb_path, "objects:", len(bpy.data.objects), "colliders:", len(colliders))
