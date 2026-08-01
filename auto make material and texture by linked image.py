import bpy
import os

# Pastikan dalam Object Mode
if bpy.context.object.mode == 'OBJECT':
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        if obj.type == 'MESH':
            if obj.data.uv_textures.active:
                uv_layer = obj.data.uv_textures.active.data
                material_dict = {}

                for face in obj.data.polygons:
                    image = uv_layer[face.index].image
                    if image:
                        # nama material = nama file tanpa ekstensi
                        mat_name = os.path.splitext(image.name)[0]

                        if mat_name not in material_dict:
                            new_material = bpy.data.materials.new(name=mat_name)
                            obj.data.materials.append(new_material)

                            new_texture = bpy.data.textures.new(name="Texture_" + mat_name, type='IMAGE')
                            new_texture.image = image

                            tex_slot = new_material.texture_slots.add()
                            tex_slot.texture = new_texture
                            tex_slot.texture_coords = 'UV'

                            material_dict[mat_name] = new_material

                        mat_index = obj.data.materials.find(material_dict[mat_name].name)
                        if mat_index != -1:
                            obj.data.polygons[face.index].material_index = mat_index

                print("Materials and textures assigned for {0} based on image files.".format(obj.name))
            else:
                print("No active UV Map found for {0}.".format(obj.name))
        else:
            print("{0} is not a mesh object.".format(obj.name))
else:
    print("Switch to Object Mode to run this script.")
