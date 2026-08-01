import bpy

# Pastikan dalam OBJECT mode
bpy.ops.object.mode_set(mode='OBJECT')

# Step 1: Hapus semua assignment weight 0 dari objek terpilih
for obj in bpy.context.selected_objects:
    if obj.type != 'MESH':
        continue

    mesh = obj.data
    if not obj.vertex_groups:
        continue

    for v in mesh.vertices:
        for g in list(v.groups):  # copy list supaya aman
            if g.weight == 0.0:
                vg = obj.vertex_groups[g.group]
                vg.remove([v.index])  # hapus vertex dari group ini

    print("Weight 0 dihapus dari:", obj.name)

# Step 2: Hapus vertex group yang kosong (tidak ada bobot > 0)
for obj in bpy.context.selected_objects:
    if obj.type != 'MESH':
        continue

    vgroups = obj.vertex_groups
    to_remove = []

    for vg in vgroups:
        has_weight = False
        for v in obj.data.vertices:
            try:
                w = vg.weight(v.index)
                if w > 1e-6:  # ada bobot non-zero
                    has_weight = True
                    break
            except RuntimeError:
                continue
        if not has_weight:
            to_remove.append(vg)

    for vg in to_remove:
        print("Removing group:", vg.name, "from object:", obj.name)
        obj.vertex_groups.remove(vg)

print("Done. Semua weight 0 dibersihkan dan group kosong dihapus.")
