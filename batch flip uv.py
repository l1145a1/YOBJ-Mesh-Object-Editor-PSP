import bpy
import bmesh

def mirror_y_uv_all_selected():
    # Simpan mode saat ini
    original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
    
    # Simpan objek aktif saat ini
    original_active = bpy.context.scene.objects.active
    
    # Loop melalui semua objek yang dipilih
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            # Set objek sebagai aktif
            bpy.context.scene.objects.active = obj
            
            # Masuk ke mode Edit
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Dapatkan data mesh dan UV layer
            mesh = bmesh.from_edit_mesh(obj.data)
            uv_layer = mesh.loops.layers.uv.verify()
            
            # Loop melalui semua face dan loop untuk mirror UV di sumbu Y
            for face in mesh.faces:
                for loop in face.loops:
                    uv = loop[uv_layer].uv
                    uv.y = 1.0 - uv.y  # Mirror UV di sumbu Y
            
            # Perbarui mesh
            bmesh.update_edit_mesh(obj.data)
            
            # Kembali ke mode Object
            bpy.ops.object.mode_set(mode='OBJECT')
    
    # Kembalikan objek aktif dan mode awal
    bpy.context.scene.objects.active = original_active
    if original_mode != 'EDIT':
        bpy.ops.object.mode_set(mode=original_mode)

# Jalankan fungsi
mirror_y_uv_all_selected()
