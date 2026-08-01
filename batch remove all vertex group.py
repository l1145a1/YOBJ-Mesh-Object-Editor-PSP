import bpy

# Loop melalui semua objek yang sedang dipilih
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        obj.vertex_groups.clear()
        print("Semua vertex group telah dihapus dari", obj.name)

print("Proses selesai!")
