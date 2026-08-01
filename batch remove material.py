import bpy

# Loop melalui semua objek yang sedang dipilih
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # Hapus semua slot material
        obj.data.materials.clear()
