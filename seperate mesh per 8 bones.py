import bpy
import bmesh

MAX_BONES = 8

obj = bpy.context.active_object

if not obj or obj.type != 'MESH':
    raise Exception("Pilih mesh terlebih dahulu")

me = obj.data

# =====================================================
# Ambil bone yang dipakai tiap face
# =====================================================

face_bones = []

for poly in me.polygons:

    bones = set()

    for vid in poly.vertices:

        v = me.vertices[vid]

        for g in v.groups:

            if g.weight > 0.0001:
                bones.add(g.group)

    face_bones.append(bones)

# =====================================================
# Packing face ke cluster max 8 bone
# =====================================================

clusters = []

for face_index, bones in enumerate(face_bones):

    placed = False

    for cluster in clusters:

        new_bones = cluster["bones"] | bones

        if len(new_bones) <= MAX_BONES:

            cluster["faces"].append(face_index)
            cluster["bones"] = new_bones
            placed = True
            break

    if not placed:

        clusters.append({
            "faces": [face_index],
            "bones": set(bones)
        })

print("Cluster:", len(clusters))

# =====================================================
# Duplicate object per cluster
# =====================================================

scene = bpy.context.scene

new_objects = []

for idx, cluster in enumerate(clusters):

    new_obj = obj.copy()
    new_obj.data = obj.data.copy()

    scene.objects.link(new_obj)

    new_obj.name = obj.name + "_part_%03d" % idx

    new_objects.append((new_obj, cluster))

# =====================================================
# Hapus face yang tidak termasuk cluster
# =====================================================

for new_obj, cluster in new_objects:

    me2 = new_obj.data

    bm = bmesh.new()
    bm.from_mesh(me2)

    bm.faces.ensure_lookup_table()

    keep_faces = set(cluster["faces"])

    delete_faces = []

    for i, f in enumerate(bm.faces):

        if i not in keep_faces:
            delete_faces.append(f)

    bmesh.ops.delete(
        bm,
        geom=delete_faces,
        context=5
    )

    bm.to_mesh(me2)
    bm.free()

# =====================================================
# Hapus vertex group yang tidak dipakai
# =====================================================

for new_obj, cluster in new_objects:

    used_groups = cluster["bones"]

    remove_groups = []

    for vg in new_obj.vertex_groups:

        if vg.index not in used_groups:
            remove_groups.append(vg)

    for vg in remove_groups:
        new_obj.vertex_groups.remove(vg)

print("Done")