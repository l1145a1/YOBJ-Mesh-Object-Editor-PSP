import bpy
import mathutils
import math

def rotate_normals(axis='X', angle_deg=180):
    """
    Memutar normals custom pada semua mesh yang dipilih.
    axis: 'X', 'Y', atau 'Z'
    angle_deg: sudut rotasi dalam derajat
    """
    # buat matriks rotasi
    angle_rad = math.radians(angle_deg)
    rot = mathutils.Matrix.Rotation(angle_rad, 3, axis.upper())

    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            mesh = obj.data
            mesh.use_auto_smooth = True
            mesh.calc_normals_split()

            new_normals = []
            for loop in mesh.loops:
                n = mathutils.Vector(loop.normal)
                n_rot = rot * n   # di Blender 2.79 gunakan * bukan @
                new_normals.append(n_rot)

            mesh.normals_split_custom_set(new_normals)
            mesh.use_auto_smooth = True

            print("Normals rotated {}° around {} axis for: {}".format(angle_deg, axis, obj.name))

# Contoh pemanggilan:
rotate_normals('X', 180)
