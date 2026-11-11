"""
Builds a blockout of the whole Halcyon Meridian (exterior) and exports it as GLB.

Run headless:
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --factory-startup --python build_ship.py

Units are meters. Blender is Z-up; the glTF exporter converts to Y-up.
Blender axes: X = along the ship (aft at 0, fore at 1600), Y = port/starboard (centre 0), Z = up.
Waterline is Z = 0.

Dimensions from lore/ship_structure_and_layout.md and the exterior SVG:
  - Length 1,600 m, beam 320 m.
  - Superstructure rises to about 150 m above the waterline; wingsail masts to about 155 m.
  - 36 rigid wingsails in two rows of 18 (110 m tall, 14 m chord), flanking the centreline.
  - Residential towers at the aft and fore ends (same footprint as the Spine model).

This is a blockout: plain boxes and a prism hull. The hull sits in the sea plane (Z = 0).
"""
import bpy
import bmesh
import os

OUT_DIR = r"C:\Users\jaspe\Documents\agentbox\ship"
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)


def make_mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m


MAT = {
    "sea":      make_mat("Sea",       (0.13, 0.30, 0.40), rough=0.3),
    "hull":     make_mat("Hull",      (0.45, 0.20, 0.16), rough=0.6),
    "terrace":  make_mat("Terrace",   (0.78, 0.74, 0.66), rough=0.7),
    "tower":    make_mat("Tower",     (0.88, 0.90, 0.92), rough=0.5),
    "super":    make_mat("Super",     (0.70, 0.72, 0.75), rough=0.6),
    "sail":     make_mat("Wingsail",  (0.95, 0.96, 0.97), rough=0.4),
    "bridge":   make_mat("Bridge",    (0.25, 0.35, 0.45), rough=0.3),
}

LENGTH = 1600.0
BEAM_HALF = 160.0
HULL_BOTTOM = -45.0
DECK_Z = 30.0
TOWER_LENGTH = 100.0
TOWER_HALF_WIDTH = 30.0
TOWER_TOP = 120.0
SAIL_TOP = 140.0


def box(name, x0, x1, y0, y1, z0, z1, mat):
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    o = bpy.context.active_object
    o.name = name
    o.scale = (x1 - x0, y1 - y0, z1 - z0)
    o.data.materials.append(mat)
    return o


def prism(name, outline, z0, z1, mat):
    """Extrude a convex 2D outline (list of (x, y)) from z0 to z1."""
    bm = bmesh.new()
    bottom = [bm.verts.new((x, y, z0)) for x, y in outline]
    top = [bm.verts.new((x, y, z1)) for x, y in outline]
    n = len(outline)
    bm.faces.new(bottom)
    bm.faces.new(top)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([bottom[i], bottom[j], top[j], top[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


# --- Sea (top surface at the waterline) --------------------------------------
box("Sea", -15000, 17000, -15000, 15000, -3, 0, MAT["sea"])

# --- Hull: plan outline tapered at the bow and stern ---------------------------
HULL_OUTLINE = [
    (0, -150), (0, 150), (120, 165), (1450, 160),
    (1600, 70), (1600, -70), (1450, -160), (120, -165),
]
prism("Hull", HULL_OUTLINE, HULL_BOTTOM, DECK_Z, MAT["hull"])

# --- Residential terraces on both sides, with a stepped upper level -----------
for side, (y0, y1) in (("Port", (-150, -40)), ("Stbd", (40, 150))):
    box(f"Terraces_{side}", 150, 1450, y0, y1, DECK_Z, DECK_Z + 30, MAT["terrace"])
    upper = (-140, -60) if side == "Port" else (60, 140)
    box(f"TerracesUpper_{side}", 300, 1300, upper[0], upper[1], DECK_Z + 30, DECK_Z + 50, MAT["terrace"])

# --- Forward and aft residential towers ---------------------------------------
box("Tower_Aft", 0, TOWER_LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, DECK_Z, TOWER_TOP, MAT["tower"])
box("Tower_Fore", LENGTH - TOWER_LENGTH, LENGTH, -TOWER_HALF_WIDTH, TOWER_HALF_WIDTH, DECK_Z, TOWER_TOP,
    MAT["tower"])

# --- Central superstructure and bridge ---------------------------------------
box("Superstructure", 700, 900, -20, 20, DECK_Z, 120, MAT["super"])
box("BridgeTower", 780, 820, -12, 12, 120, 150, MAT["bridge"])

# --- 36 wingsails in two rows of 18 flanking the centreline --------------------
SAIL_CHORD = 14.0
SAIL_THICKNESS = 3.0
SAIL_ROW_Y = 32.0
for row, sign in (("Port", -1), ("Stbd", 1)):
    for i in range(18):
        x = 120 + i * (1360.0 / 17.0)
        box(f"Wingsail_{row}_{i}", x - SAIL_CHORD / 2, x + SAIL_CHORD / 2,
            sign * SAIL_ROW_Y - SAIL_THICKNESS / 2, sign * SAIL_ROW_Y + SAIL_THICKNESS / 2,
            DECK_Z, SAIL_TOP, MAT["sail"])

# --- Export ---------------------------------------------------------------------
glb_path = os.path.join(OUT_DIR, "ship.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")
print("EXPORTED", glb_path, "objects:", len(bpy.data.objects))
