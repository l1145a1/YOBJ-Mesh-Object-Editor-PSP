import bpy

# Mengambil objek yang dipilih
obj = bpy.context.object

# Mendapatkan daftar vertex group dari objek
vg_list = obj.vertex_groups.keys()

# Loop melalui setiap vertex group dan memisahkan objek berdasarkan seleksinya
for vg_name in vg_list:
    # Mengambil vertex group berdasarkan namanya
    vg = obj.vertex_groups[vg_name]
    
    # Membuat satu objek baru untuk setiap vertex group
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=vg_name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Memberi nama baru pada objek yang terpisah
    new_obj = bpy.context.selected_objects[0]
    new_obj.name = vg_name
