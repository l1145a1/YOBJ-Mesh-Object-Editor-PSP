import bpy

# Membuat loop melalui objek yang dipilih
for obj in bpy.context.selected_objects:
    
    # Memilih objek sebagai objek yang aktif
    bpy.context.scene.objects.active = obj
    
    # Membuat vertex group baru dengan nama yang sama dengan nama objek
    vg = obj.vertex_groups.new(name=obj.name)
    
    # Menambahkan semua vertex ke vertex group baru
    for i in range(len(obj.data.vertices)):
        vg.add([i], 1.0, 'REPLACE')
    
    # Mencetak pesan konfirmasi untuk setiap objek yang diproses
    print("Vertex group created for object: " + obj.name + " with " + str(len(obj.data.vertices)) + " vertices.")

# Get a reference to the active object
active_object = bpy.context.active_object

# Get a list of all selected objects
selected_objects = bpy.context.selected_objects

# Remove the active object from the list of selected objects
selected_objects.remove(active_object)

# Join all selected objects to the active object
for obj in selected_objects:
    bpy.context.scene.objects.active = active_object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True
    active_object.select = True
    bpy.ops.object.join()

# Set the active object to the joined object
bpy.context.scene.objects.active = active_object
