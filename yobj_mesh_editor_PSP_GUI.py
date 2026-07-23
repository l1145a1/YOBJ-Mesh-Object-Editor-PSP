import struct
import sys
import os
import re
import shutil
import copy
import math
import tkinter as tk
from tkinter import filedialog, Listbox
from tkinter import messagebox
from collections import Counter
import xml.etree.ElementTree as ET

base_file=''
target_file=''
header = b''
all_offset=[]
mesh_count=0
bone_count=0
texture_count=0
mesh_header_start_offset=0
bones_start_offset=0
texture_offset=0
model_name_offset=0
model_count=0
mesh_header=[]
mesh_bones_header_offset=[]
mesh_bones_count=[]
mesh_bones=[]
mesh_data_header_offset=[]
mesh_data_start_offset=[]
mesh_data_lenght=[]
mesh_data_count=[]
mesh_data=[]
mesh_flag=[]
mesh_flag_boolean=[]
mesh_flag_binary=[]
mesh_flag_decode=[]
mesh_bones_weight=[]
mesh_uv_u=[]
mesh_uv_v=[]
mesh_vertex_color=[]
mesh_normal_x=[]
mesh_normal_y=[]
mesh_normal_z=[]
mesh_vertex_x=[]
mesh_vertex_y=[]
mesh_vertex_z=[]
mesh_material_header_offset=[]
mesh_material_count=[]
mesh_material=[]
mesh_material_texture=[]
mesh_material_faces_count=[]
mesh_material_faces_header_offset=[]
mesh_material_faces_start_offset=[]
mesh_faces_header=[]
mesh_face_count=[]
mesh_face_offset=[]
mesh_face=[]
new_mesh_header_start_offset=0
new_bones_start_offset=0
new_mesh_header_offset=[]
new_mesh_bones_header_offset=[]
new_mesh_data_header_offset=[]
new_mesh_data_start_offset=[]
new_mesh_data_count=[]
new_mesh_material_header_offset=[]
new_mesh_material_offset=[]
new_mesh_material_count=[]
new_mesh_material=[]
new_mesh_material_faces_start_offset=[]
new_mesh_material_faces_header_offset=[]
new_mesh_faces_header_offset=[]
new_mesh_face_offset=[]
bone=[]
bone_name=[]
bone_local_position_x=[]
bone_local_position_y=[]
bone_local_position_z=[]
bone_local_position_w=[]
bone_rotation_x=[]
bone_rotation_y=[]
bone_rotation_z=[]
bone_parrent=[]
bone_global_position_x=[]
bone_global_position_y=[]
bone_global_position_z=[]
bone_unknown_float=[]
new_bone_offset=[]
texture=[]
new_texture_start_offset=0
new_texture_offset=[]
model_name=''
new_model_name_offset=0
#file_control
def backup_file(base_file, target_file):
    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    # tutup file handle dulu
    base_file.close()
    target_file.close()

    # rename file asli jadi .bak
    bak_path = f"{base_name}{base_ext}.bak"
    os.replace(base_path, bak_path)

    # rename file -new jadi file utama
    os.replace(target_path, base_path)

    # hapus file -new kalau masih ada
    if os.path.exists(target_path):
        os.remove(target_path)
def make_new_file(t):
    t.seek(0)
    t.write(b'YOBJ')
    print("Write Identifier 'YOBJ'")
    all_offset.append(8)
    pass
def padding(t):
    current_offset = t.tell()
    column = current_offset % 16
    if column != 8:
        # Kalau tidak di kolom 08, cari padding sampai kolom 08 berikutnya
        padding = (8 - column) % 16
        if padding == 0:
            padding = 16  # Kalau persis di kolom 08, skip
        t.write(b'\x00' * padding)
    pass
#read_procedure
def read_header(b):
    global mesh_count, bone_count, texture_count, mesh_header_start_offset, bones_start_offset, texture_offset, model_name_offset, model_count, header
    b.seek(4)
    print(f"Read Header at offset {b.tell()}, Lenght 64 Bytes")
    header=b.read(68)
    b.seek(24)
    mesh_count=struct.unpack('<I', b.read(4))[0]
    print(f"Read Mesh Count at offset {b.tell()-4}, Value {mesh_count}")
    bone_count=struct.unpack('<I', b.read(4))[0]
    print(f"Read Bone Count at offset {b.tell()-4}, Value {bone_count}")
    texture_count=struct.unpack('<I', b.read(4))[0]
    print(f"Read Texture Count at offset {b.tell()-4}, Value {texture_count}")
    mesh_header_start_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Mesh Header Offset at offset {b.tell()-4}, Value {mesh_header_start_offset}")
    bones_start_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Bone Offset at offset {b.tell()-4}, Value {bones_start_offset}")
    texture_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Texture Offset at offset {b.tell()-4}, Value {texture_offset}")
    model_name_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Model Name Offset at offset {b.tell()-4}, Value {model_name_offset}")
    model_count=struct.unpack('<I', b.read(4))[0]
    print(f"Read Model Count at offset {b.tell()-4}, Value {model_count}")
    pass
def read_mesh_header(b):
    global mesh_count, mesh_header_start_offset
    b.seek(mesh_header_start_offset+8)
    for i in range(mesh_count):
        offset=b.tell()
        print(f"Read Mesh Header, Object {i}, Offset {b.tell()}")
        mesh_header.append(b.read(64))
        b.seek(offset)
        b.read(4)
        mesh_material_count.append(struct.unpack('<I', b.read(4))[0])
        print(f"Material Count {mesh_material_count[i]}")
        mesh_bones_header_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Bones Header Offset {mesh_bones_header_offset[i]}")
        mesh_material_header_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Material Header Offset {mesh_material_header_offset[i]}")
        b.read(8)
        mesh_data_header_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Mesh Data Offset {mesh_data_header_offset[i]}")
        mesh_flag.append(struct.unpack('<I', b.read(4))[0])
        print(f"Mesh Flag {mesh_flag[i]}")
        b.read(8)
        mesh_data_count.append(struct.unpack('<I', b.read(4))[0])
        print(f"Mesh Data Count (Vertex & UV) {mesh_data_count[i]}")
        b.read(20)
        pass
    pass
def read_mesh_header_bones(b,i):
    b.seek(mesh_bones_header_offset[i]+8)
    print(f"Read Mesh Header Bones, Object {i}, Offset {b.tell()}")
    b.read(4) # Mesh Data Count (same as in mesh header)
    mesh_bones_count.append(struct.unpack('<I', b.read(4))[0])
    print(f"Mesh Bones Count {mesh_bones_count[i]}")
    b.read(4) # Mesh Data Offset (same as in mesh header)
    b.read(4) # Empty
    mesh_bones.append([])
    for j in range(mesh_bones_count[i]):
        mesh_bones[i].append(struct.unpack('<I', b.read(4))[0])
        print(f"Mesh Bones, Index {j}, Value {mesh_bones[i][j]}")
    pass
def read_mesh_data_header(b,i):
    b.seek(mesh_data_header_offset[i]+8)
    print(f"Read Mesh Data Offset, Object {i}, Offset {b.tell()}")
    mesh_data_start_offset.append(struct.unpack('<I', b.read(4))[0])
    pass
def read_flag(i):
    # Kalkulasi panjang Mesh Data
    print(f"Read Flag, Object {i}, Value {mesh_flag[i]}")
    mesh_flag_boolean.append(mesh_flag[i] & 1536 != 0)
    print(f"Convert Flag to Boolean: {mesh_flag_boolean[i]}")
    mesh_flag_binary.append(format(mesh_flag[i], '032b')[::-1])
    print(f"Convert Flag to Binary: {mesh_flag_binary[i]}")
    mesh_flag_decode.append(int(mesh_flag_binary[i][16:13:-1], 2))
    print(f"Decode Flag Binary to Integer: {mesh_flag_decode[i]}")
def read_mesh_data(b,i):
    b.seek(mesh_data_start_offset[i] + 8)
    print(f"Read Mesh Data, Object {i}, Offset {b.tell()}")
    if mesh_flag_boolean[i]:
        mesh_data_lenght.append((mesh_flag_decode[i] + 10) * 4)
    else:
        mesh_data_lenght.append(36)
    print(f"Mesh Data Length Per Index {mesh_data_lenght[i]}")

    mesh_data.append([])
    mesh_bones_weight.append([])
    mesh_uv_u.append([])
    mesh_uv_v.append([])
    mesh_vertex_color.append([])
    mesh_normal_x.append([])
    mesh_normal_y.append([])
    mesh_normal_z.append([])
    mesh_vertex_x.append([])
    mesh_vertex_y.append([])
    mesh_vertex_z.append([])

    for j in range(mesh_data_count[i]):
        offset = b.tell()
        mesh_data[i].append(b.read(mesh_data_lenght[i]))
        b.seek(offset)

        # hanya baca bones weight kalau panjang data > 36
        if mesh_data_lenght[i] > 36:
            mesh_bones_weight[i].append([])
            for k in range(mesh_bones_count[i]):
                mesh_bones_weight[i][j].append(struct.unpack('<f', b.read(4))[0])
        else:
            mesh_bones_weight[i].append([])  # tetap append list kosong

        # read UV
        mesh_uv_u[i].append(struct.unpack('<f', b.read(4))[0])
        mesh_uv_v[i].append(struct.unpack('<f', b.read(4))[0])

        # vertex color
        mesh_vertex_color[i].append(struct.unpack('BBBB', b.read(4)))

        # read normal
        mesh_normal_x[i].append(struct.unpack('<f', b.read(4))[0])
        mesh_normal_y[i].append(struct.unpack('<f', b.read(4))[0])
        mesh_normal_z[i].append(struct.unpack('<f', b.read(4))[0])

        # read vertex
        mesh_vertex_x[i].append(struct.unpack('<f', b.read(4))[0])
        mesh_vertex_y[i].append(struct.unpack('<f', b.read(4))[0])
        mesh_vertex_z[i].append(struct.unpack('<f', b.read(4))[0])

        print(f"Index {j}, Offset {offset}")
def read_mesh_material(b,i):
    b.seek(mesh_material_header_offset[i]+8)
    mesh_material.append([])
    mesh_material_texture.append([])
    mesh_material_faces_count.append([])
    mesh_material_faces_header_offset.append([])
    mesh_material_faces_start_offset.append([])
    for j in range(mesh_material_count[i]):
        offset=b.tell()
        mesh_material[i].append(b.read(144))
        b.seek(offset)
        b.read(22)
        mesh_material_texture[i].append(struct.unpack('<H', b.read(2))[0])
        b.read(108)
        mesh_material_faces_count[i].append(struct.unpack('<I', b.read(4))[0])
        mesh_material_faces_header_offset[i].append(struct.unpack('<I', b.read(4))[0])
        mesh_material_faces_start_offset[i].append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Mesh Material, Object {i}, Material {j}, offset {offset}")
        pass
    pass
def read_mesh_faces_header(b,i):
    mesh_faces_header.append([])
    mesh_face_count.append([])
    mesh_face_offset.append([])
    for j in range(mesh_material_count[i]):
        b.seek(mesh_material_faces_header_offset[i][j]+8)
        mesh_faces_header[i].append([])
        mesh_face_count[i].append([])
        mesh_face_offset[i].append([])
        for k in range(mesh_material_faces_count[i][j]):
            offset=b.tell()
            mesh_faces_header[i][j].append(b.read(16))
            print(f"Read Mesh Face Header, Object {i}, Material {j}, Face {k} Offset {offset}")
            b.seek(offset)
            b.read(8)
            mesh_face_count[i][j].append(struct.unpack('<I', b.read(4))[0])
            mesh_face_offset[i][j].append(struct.unpack('<I', b.read(4))[0])
            pass
        pass
    pass
def read_mesh_faces(b,i):
    mesh_face.append([])
    for j in range(mesh_material_count[i]):
        mesh_face[i].append([])
        for k in range(mesh_material_faces_count[i][j]):
            b.seek(mesh_face_offset[i][j][k] + 8)
            mesh_face[i][j].append([])  # siapkan list untuk face ke-k
            for l in range(mesh_face_count[i][j][k]):  # jumlah elemen dalam face
                mesh_face[i][j][k].append(struct.unpack('<H', b.read(2))[0])
                print(f"Read Face, Object {i}, Material {j}, Faces {k}, Index {l}, Value {mesh_face[i][j][k][l]}")
            pass
def read_bones(b):
    global bone_count, bones_start_offset
    b.seek(bones_start_offset+8)
    for i in range(bone_count):
        offset=b.tell()
        bone.append(b.read(80))
        b.seek(offset)
        bone_name.append(b.read(16).decode("ascii").rstrip("\x00"))
        bone_local_position_x.append(struct.unpack('<f', b.read(4))[0])
        bone_local_position_y.append(struct.unpack('<f', b.read(4))[0])
        bone_local_position_z.append(struct.unpack('<f', b.read(4))[0])
        bone_local_position_w.append(struct.unpack('<f', b.read(4))[0])
        bone_rotation_x.append(struct.unpack('<f', b.read(4))[0])
        bone_rotation_y.append(struct.unpack('<f', b.read(4))[0])
        bone_rotation_z.append(struct.unpack('<f', b.read(4))[0])
        b.read(4)
        bone_parrent.append(struct.unpack('<I', b.read(4))[0])
        b.read(12)
        bone_global_position_x.append(struct.unpack('<f', b.read(4))[0])
        bone_global_position_y.append(struct.unpack('<f', b.read(4))[0])
        bone_global_position_z.append(struct.unpack('<f', b.read(4))[0])
        bone_unknown_float.append(struct.unpack('<f', b.read(4))[0])
        print(f"Read Bone, Index {i}, {bone_name[i]}, Parrent {bone_parrent[i]}")
def read_texture(b):
    global texture_count, texture_offset
    b.seek(texture_offset+8)
    print(f"Read {texture_count} Texture at offset {b.tell()}")
    for i in range(texture_count):
        texture.append(b.read(16).decode("ascii").rstrip("\x00"))
def read_model_name(b):
    global model_name_offset, model_name
    b.seek(model_name_offset+8)
    print(f"Read Model Name at offset {b.tell()}")
    model_name=b.read(16).decode("ascii").rstrip("\x00")
    pass
#write_procedure
def cleanup_duplicate_textures():
    global texture, texture_count, mesh_material_texture

    new_texture = []
    remap = {}

    # buat daftar texture unik + tabel remap
    for old_idx, tex_name in enumerate(texture):

        if tex_name in new_texture:
            new_idx = new_texture.index(tex_name)
        else:
            new_idx = len(new_texture)
            new_texture.append(tex_name)

        remap[old_idx] = new_idx

    # perbaiki semua referensi material
    for mesh_id in range(len(mesh_material_texture)):
        for mat_id in range(len(mesh_material_texture[mesh_id])):

            old_tex = mesh_material_texture[mesh_id][mat_id]

            if old_tex in remap:
                mesh_material_texture[mesh_id][mat_id] = remap[old_tex]

    removed = len(texture) - len(new_texture)

    texture[:] = new_texture
    texture_count = len(texture)

    print("Removed", removed, "duplicate textures")
    print("New texture count:", texture_count)
def write_header(t):
    t.seek(0,os.SEEK_END)
    print(f"Write Header at offset {t.tell()}")
    t.write(header)
    pass
def write_mesh_header(t):
    global mesh_count, mesh_header_start_offset, new_mesh_header_start_offset, new_mesh_header_offset, mesh_header
    t.seek(0,os.SEEK_END)
    new_mesh_header_start_offset=t.tell()
    for i in range(mesh_count):
        print(f"Write Mesh Header, Object {i}, Offset {t.tell()}")
        new_mesh_header_offset.append(t.tell())
        t.write(mesh_header[i])
        t.seek(new_mesh_header_offset[i])
        t.read(4)
        t.write(struct.pack('<I',mesh_material_count[i]))
        t.read(20)
        t.write(struct.pack('<I',mesh_flag[i]))
        t.read(8)
        t.write(struct.pack('<I',mesh_data_count[i]))
        t.read(20)
        pass
    t.seek(24)
    t.write(struct.pack('<I',mesh_count))
    t.seek(36)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_header_start_offset-8))
    print(f"Write New Mesh Header Offset at offset 36, Value {new_mesh_header_offset[0]-8}")
    pass
def write_mesh_header_bones(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_bones_header_offset.append(t.tell())
    t.write(struct.pack('<I',mesh_data_count[i]))
    t.write(struct.pack('<I',mesh_bones_count[i]))
    t.write(struct.pack('<I',mesh_data_header_offset[i]))
    t.write(b'\x00' * 4)
    for j in range(mesh_bones_count[i]):
        t.write(struct.pack('<I',mesh_bones[i][j]))
    t.seek(new_mesh_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_bones_header_offset[i]-8))
    print(f"Write New Mesh Bones Header, Object {i}, Offset {new_mesh_bones_header_offset[i]}")
    pass
def write_mesh_data_header(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_data_header_offset.append(t.tell())
    t.write(struct.pack('<I',mesh_data_start_offset[i]-8))
    t.seek(new_mesh_header_offset[i])
    t.read(24)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_header_offset[i]-8))
def write_mesh_data(t,i):
    t.seek(0,os.SEEK_END)
    padding(t)
    new_mesh_data_start_offset.append(t.tell())
    for j in range(mesh_data_count[i]):
        offset = t.tell()
        t.write(mesh_data[i][j])
        t.seek(offset)

        # hanya tulis bones weight kalau panjang data > 36
        if mesh_data_lenght[i] > 36:
            for k in range(mesh_bones_count[i]):
                print(f"mesh_bone_weight")
                t.write(struct.pack('<f', mesh_bones_weight[i][j][k]))

        # UV
        print(f"uv")
        t.write(struct.pack('<f', mesh_uv_u[i][j]))
        t.write(struct.pack('<f', mesh_uv_v[i][j]))

        # vertex color
        print(f"vertex_color")
        t.write(struct.pack('BBBB', *mesh_vertex_color[i][j]))

        # normal
        print(f"normals")
        t.write(struct.pack('<f', mesh_normal_x[i][j]))
        t.write(struct.pack('<f', mesh_normal_y[i][j]))
        t.write(struct.pack('<f', mesh_normal_z[i][j]))

        # vertex
        print(f"vertex")
        t.write(struct.pack('<f', mesh_vertex_x[i][j]))
        t.write(struct.pack('<f', mesh_vertex_y[i][j]))
        t.write(struct.pack('<f', mesh_vertex_z[i][j]))

        print(f"Write New Mesh Data, Object {i}, Offset {offset}, Length {mesh_data_lenght[i]}")

    # update offset di header
    t.seek(new_mesh_bones_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I', new_mesh_data_start_offset[i]-8))

    t.seek(new_mesh_data_header_offset[i])
    all_offset.append(t.tell())
    t.write(struct.pack('<I', new_mesh_data_start_offset[i]-8))
    pass
def write_mesh_material(t,i):
    t.seek(0,os.SEEK_END)
    padding(t)
    new_mesh_material_header_offset.append(t.tell())
    new_mesh_material_offset.append([])
    for j in range(mesh_material_count[i]):
        offset=t.tell()
        new_mesh_material_offset[i].append(offset)
        t.write(mesh_material[i][j])
        t.seek(offset)
        t.read(22)
        t.write(struct.pack('<H',mesh_material_texture[i][j]))
        t.read(108)
        t.write(struct.pack('<I',mesh_material_faces_count[i][j]))
        t.write(struct.pack('<I',mesh_material_faces_header_offset[i][j]))
        t.write(struct.pack('<I',mesh_material_faces_start_offset[i][j]))
        pass
    t.seek(new_mesh_header_offset[i])
    t.read(12)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_material_header_offset[i]-8))
    print(f"Write New Mesh Material, Object {i}, Offset {new_mesh_material_header_offset[i]}, Lenght {len(mesh_material[i])}")
    pass
def write_mesh_faces_header(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_material_faces_header_offset.append([])
    new_mesh_faces_header_offset.append([])
    for j in range(mesh_material_count[i]):
        t.seek(0,os.SEEK_END)
        new_mesh_material_faces_header_offset[i].append(t.tell())
        new_mesh_faces_header_offset[i].append([])
        for k in range(mesh_material_faces_count[i][j]):
            t.seek(0,os.SEEK_END)
            offset=t.tell()
            new_mesh_faces_header_offset[i][j].append(offset)
            t.write(mesh_faces_header[i][j][k])
            t.seek(offset)
            t.read(8)
            t.write(struct.pack('<I',mesh_face_count[i][j][k]))
            t.write(struct.pack('<I',mesh_face_offset[i][j][k]))
            print(f"Write Mesh Faces Header, Object {i}, Material {j}, Index {k}, Offset {offset}")
        t.seek(new_mesh_material_offset[i][j])
        t.read(136)
        all_offset.append(t.tell())
        t.write(struct.pack('<I',new_mesh_material_faces_header_offset[i][j]-8))
def write_mesh_faces(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_face_offset.append([])
    new_mesh_material_faces_start_offset.append([])
    for j in range(mesh_material_count[i]):
        t.seek(0,os.SEEK_END)
        new_mesh_face_offset[i].append([])
        new_mesh_material_faces_start_offset[i].append(t.tell())
        for k in range(mesh_material_faces_count[i][j]):
            t.seek(0,os.SEEK_END)
            new_mesh_face_offset[i][j].append(t.tell())
            for l in range(mesh_face_count[i][j][k]):
                t.write(struct.pack('<H', mesh_face[i][j][k][l]))
                print(f"Write Mesh Faces, Object {i}, Material {j}, Faces {k}, Index {l} Offset {t.tell()}")
            padding(t)    
            t.seek(new_mesh_faces_header_offset[i][j][k])
            t.read(12)
            all_offset.append(t.tell())
            t.write(struct.pack('<I',new_mesh_face_offset[i][j][k]-8))
        t.seek(new_mesh_material_offset[i][j])
        t.read(140)
        all_offset.append(t.tell())
        t.write(struct.pack('<I',new_mesh_material_faces_start_offset[i][j]-8))
def write_bones(t):
    global bone_count, new_bones_start_offset
    t.seek(0,os.SEEK_END)
    new_bones_start_offset=t.tell()
    for i in range(bone_count):
        t.seek(0,os.SEEK_END)
        offset=t.tell()
        new_bone_offset.append(offset)
        t.write(bone[i])
        t.seek(offset)
        t.write(bone_name[i].encode("ascii").ljust(16, b"\x00"))
        t.write(struct.pack('<f',bone_local_position_x[i]))
        t.write(struct.pack('<f',bone_local_position_y[i]))
        t.write(struct.pack('<f',bone_local_position_z[i]))
        t.write(struct.pack('<f',bone_local_position_w[i]))
        t.write(struct.pack('<f',bone_rotation_x[i]))
        t.write(struct.pack('<f',bone_rotation_y[i]))
        t.write(struct.pack('<f',bone_rotation_z[i]))
        t.read(4)
        t.write(struct.pack('<I',bone_parrent[i]))
        parent_name = ""
        try:
            parent_idx = bone_parrent[i]
            if 0 <= parent_idx < len(bone_name):
                parent_name = bone_name[parent_idx]
        except Exception:
            parent_name = ""
        t.read(12)
        t.write(struct.pack('<f',bone_global_position_x[i]))
        t.write(struct.pack('<f',bone_global_position_y[i]))
        t.write(struct.pack('<f',bone_global_position_z[i]))
        t.write(struct.pack('<f',bone_unknown_float[i]))
        print(f"Write Bones, Index {i}, {bone_name[i]}, Parent {bone_parrent[i]}({parent_name})")
        pass
    t.seek(28)
    t.write(struct.pack('<I',bone_count))
    t.seek(40)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_bones_start_offset-8))
    pass
def write_texture(t):
    global texture_count, new_texture_start_offset
    t.seek(0, os.SEEK_END)
    new_texture_start_offset = t.tell()
    for i in range(texture_count):
        t.seek(0, os.SEEK_END)
        new_texture_offset.append(t.tell())
        t.write(texture[i].encode("ascii").ljust(16, b"\x00"))
        print(f"Write Texture, Index {i}, {texture[i]}")
    # update header
    t.seek(32)
    t.write(struct.pack('<I', texture_count))
    t.seek(44)
    all_offset.append(t.tell())
    t.write(struct.pack('<I', new_texture_start_offset - 8))
def write_model_name(t):
    global model_name_offset, new_model_name_offset, model_name
    t.seek(0,os.SEEK_END)
    new_model_name_offset=t.tell()
    print(f"Write Model Name at offset {t.tell()}")
    t.write(model_name.encode('ascii').ljust(16, b"\x00"))
    print(f"Write Model Count at offset {t.tell()}")
    t.write(struct.pack('<I', model_count))
    t.write(b'\x00' * 4)
    print(f"Write Mesh Count at offset {t.tell()}")
    t.write(struct.pack('<I', mesh_count))
    t.write(b'\x00' * 4)
    t.seek(48)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_model_name_offset-8))
    pass
#pof0_generator
def out(t, cursor, diff):   #pofo encrpyt logic
    count = 0
    sp = cursor - diff
    if sp <= 0xFC:
        sp = (sp >> 2) | 0x40
        t.write(struct.pack('B', sp))
        count += 1
    elif sp <= 0xFFFC:
        sp = (sp >> 2) | 0x8000
        sp = struct.pack('>H', sp)
        t.write(sp)
        count += 2
    else:
        sp = (sp >> 2) | 0xC0000000
        sp = struct.pack('>I', sp)
        t.write(sp)
        count += 4
    print(f"Generate POF0, Cursor {cursor}, Diff/Temp {diff}, SP {sp}, Count {count}")
    return count
def generate_pof0(t):
    t.seek(0,os.SEEK_END)
    new_pof0_offset=t.tell()
    t.seek(4)
    t.write(struct.pack('<I',new_pof0_offset-8)) # POF0 Offset
    t.seek(12)
    t.write(struct.pack('<I',new_pof0_offset-8)) # YOBJ Lenght
    t.seek(0,os.SEEK_END)
    t.write(b'POF0')
    new_pof0_lenght_offset=t.tell()
    t.write(b'\x00' * 4)
    new_pof0_start_offset=t.tell()
    all_offset.sort()
    for i in range(len(all_offset)-1):
        cursor = all_offset[i+1]
        temp = all_offset[i]
        out(t, cursor, temp)
    new_pof0_end_offset=t.tell()
    new_pof0_lenght=new_pof0_end_offset-new_pof0_start_offset
    print(f"POF0 Lenght {new_pof0_lenght}")
    t.seek(new_pof0_lenght_offset)
    t.write(struct.pack('<I',new_pof0_lenght))
#mesh_editor
def print_mesh():
    print(f"Mesh List: ")
    for i in range(mesh_count):
        print(f"Object {i}, Mesh Data {mesh_data_count[i]}, Material {mesh_material_count[i]}")
        pass
    pass
def duplicate_mesh(b, i):
    global mesh_count
    mesh_count += 1
    
    # duplicate mesh_header
    mesh_header.append(copy.deepcopy(mesh_header[i]))
    mesh_material_count.append(copy.deepcopy(mesh_material_count[i]))
    mesh_data_header_offset.append(copy.deepcopy(mesh_data_header_offset[i]))
    mesh_flag.append(copy.deepcopy(mesh_flag[i]))
    mesh_data_count.append(copy.deepcopy(mesh_data_count[i]))

    # re-read untuk isi detail
    read_mesh_header_bones(b, mesh_count-1)
    read_mesh_data_header(b, mesh_count-1)
    read_flag(mesh_count-1)
    read_mesh_data(b, mesh_count-1)
    read_mesh_material(b, mesh_count-1)
    read_mesh_faces_header(b, mesh_count-1)
    read_mesh_faces(b, mesh_count-1)
    print(f"Mesh {i}, Duplicated.")
def remove_mesh(i):
    global mesh_count
    mesh_count -= 1

    # mesh
    del mesh_header[i]
    del mesh_bones_header_offset[i]
    del mesh_bones_count[i]
    del mesh_bones[i]
    del mesh_data_header_offset[i]
    del mesh_data_start_offset[i]
    del mesh_data_lenght[i]
    del mesh_data_count[i]
    del mesh_data[i]
    del mesh_flag[i]
    del mesh_flag_boolean[i]
    del mesh_flag_binary[i]
    del mesh_flag_decode[i]
    del mesh_bones_weight[i]
    del mesh_uv_u[i]
    del mesh_uv_v[i]
    del mesh_vertex_color[i]
    del mesh_normal_x[i]
    del mesh_normal_y[i]
    del mesh_normal_z[i]
    del mesh_vertex_x[i]
    del mesh_vertex_y[i]
    del mesh_vertex_z[i]
    del mesh_material_count[i]
    del mesh_material[i]
    del mesh_material_texture[i]
    del mesh_material_faces_count[i]
    del mesh_material_faces_header_offset[i]
    del mesh_material_faces_start_offset[i]
    del mesh_faces_header[i]
    del mesh_face_count[i]
    del mesh_face_offset[i]
    del mesh_face[i]

    print(f"Mesh {i}, Removed.")
def rotate_3d_x(x, y, z, degree):
    q = degree * (math.pi / 180)
    new_y = y * math.cos(q) - z * math.sin(q)
    new_z = y * math.sin(q) + z * math.cos(q)
    new_x = x
    return (new_x, new_y, new_z)
def export_obj(i, filepath, mtlpath):
    import os, math

    with open(filepath, "w", encoding="utf-8") as obj_file:
        obj_file.write(f"# Exported Object {i}\n")
        obj_file.write(f"mtllib {os.path.basename(mtlpath)}\n")

        # vertex dengan rotasi 180 derajat di sumbu X
        for j in range(mesh_data_count[i]):
            x, y, z = mesh_vertex_x[i][j], mesh_vertex_y[i][j], mesh_vertex_z[i][j]
            coord_x, coord_y, coord_z = rotate_3d_x(x, y, z, 180)
            obj_file.write(f"v {round(coord_x,6)} {round(-coord_z,6)} {round(coord_y,6)}\n")

        # uv
        for j in range(mesh_data_count[i]):
            obj_file.write(f"vt {mesh_uv_u[i][j]} {mesh_uv_v[i][j]}\n")

        # normals (tanpa rotasi, atau bisa rotasi juga kalau mau konsisten)
        for j in range(mesh_data_count[i]):
            nx, ny, nz = mesh_normal_x[i][j], mesh_normal_y[i][j], mesh_normal_z[i][j]
            obj_file.write(f"vn {round(nx,6)} {round(ny,6)} {round(nz,6)}\n")

        # faces dengan pola ganjil-genap + usemtl
        for j in range(mesh_material_count[i]):
            tex_id = mesh_material_texture[i][j]
            tex_name = str(texture[tex_id]).strip("\x00")
            obj_file.write(f"usemtl {tex_name}\n")

            for k in range(mesh_material_faces_count[i][j]):
                face_indices = mesh_face[i][j][k]
                if len(face_indices) < 3:
                    continue
                # baris pertama
                obj_file.write(
                    f"f {face_indices[0]+1}/{face_indices[0]+1}/{face_indices[0]+1} "
                    f"{face_indices[1]+1}/{face_indices[1]+1}/{face_indices[1]+1} "
                    f"{face_indices[2]+1}/{face_indices[2]+1}/{face_indices[2]+1}\n"
                )
                # baris berikutnya zig-zag
                for n in range(1, len(face_indices)-2):
                    if n % 2 == 1:
                        v1, v2, v3 = face_indices[n], face_indices[n+2], face_indices[n+1]
                    else:
                        v1, v2, v3 = face_indices[n], face_indices[n+1], face_indices[n+2]
                    obj_file.write(
                        f"f {v1+1}/{v1+1}/{v1+1} {v2+1}/{v2+1}/{v2+1} {v3+1}/{v3+1}/{v3+1}\n"
                    )
def export_mtl(i, mtlpath):
    with open(mtlpath, "w", encoding="utf-8") as mtl_file:
        mtl_file.write(f"# Exported Material for Object {i}\n")

        for j in range(mesh_material_count[i]):
            tex_id = mesh_material_texture[i][j]
            tex_name_raw = texture[tex_id]

            if isinstance(tex_name_raw, bytes):
                tex_name = tex_name_raw.decode("utf-8", errors="ignore")
            else:
                tex_name = str(tex_name_raw)

            # bersihkan karakter null, whitespace, dan kontrol
            tex_name = tex_name.strip().strip("\x00")
            tex_name = "".join(ch for ch in tex_name if ch.isprintable())

            mtl_file.write(f"newmtl {tex_name}\n")
            mtl_file.write("Ka 1.000 1.000 1.000\n")
            mtl_file.write("Kd 1.000 1.000 1.000\n")
            mtl_file.write("Ks 0.000 0.000 0.000\n")
            mtl_file.write("d 1.0\n")
            mtl_file.write("illum 2\n")
            mtl_file.write(f"map_Kd {tex_name}.png\n")
def import_obj(i, filepath):
    from collections import Counter

    vertices = []
    normals = []
    vertex_normals = [[] for _ in range(mesh_data_count[i])]

    with open(filepath, "r", encoding="utf-8") as obj_file:
        for line in obj_file:
            if line.startswith("v "):
                vx, vy, vz = map(float, line.strip().split()[1:4])
                coord_x, coord_y, coord_z = vx, vz, -vy
                orig_x, orig_y, orig_z = rotate_3d_x(coord_x, coord_y, coord_z, 180)
                vertices.append((orig_x, orig_y, orig_z))

            elif line.startswith("vn "):
                nx, ny, nz = map(float, line.strip().split()[1:4])
                normals.append((nx, ny, nz))

            elif line.startswith("f "):
                parts = line.strip().split()[1:]
                for p in parts:
                    vals = p.split("/")
                    if len(vals) >= 3:  # v/vt/vn
                        v_idx = int(vals[0]) - 1
                        vn_idx = int(vals[2]) - 1
                        if 0 <= v_idx < mesh_data_count[i] and 0 <= vn_idx < len(normals):
                            vertex_normals[v_idx].append(normals[vn_idx])

    # verifikasi jumlah vertex
    if len(vertices) != mesh_data_count[i]:
        return False

    # assign vertex
    for j, (x, y, z) in enumerate(vertices):
        mesh_vertex_x[i][j] = x
        mesh_vertex_y[i][j] = y
        mesh_vertex_z[i][j] = z

    # assign normals: pilih yang paling sering muncul
    for j in range(mesh_data_count[i]):
        if vertex_normals[j]:
            nx, ny, nz = Counter(vertex_normals[j]).most_common(1)[0][0]
            mesh_normal_x[i][j], mesh_normal_y[i][j], mesh_normal_z[i][j] = nx, ny, nz

    return True
def parse_obj(filepath):
    vertices = []
    uvs = []
    faces_raw = []
    materials = []
    current_material = 0

    with open(filepath, "r", encoding="utf-8") as obj_file:
        for line in obj_file:
            if line.startswith("v "):  # vertex
                vx, vy, vz = map(float, line.strip().split()[1:4])
                vertices.append((vx, vy, vz))

            elif line.startswith("vt "):  # uv
                u, v = map(float, line.strip().split()[1:3])
                uvs.append((u, v))

            elif line.startswith("usemtl "):  # material
                mat_name = line.strip().split()[1]
                materials.append(mat_name)
                current_material = len(materials) - 1

            elif line.startswith("f "):  # face
                parts = line.strip().split()[1:]
                indices = []
                uv_indices = []
                for p in parts:
                    vals = p.split("/")
                    v_idx = int(vals[0]) - 1  # OBJ → 0-based
                    indices.append(v_idx)
                    if len(vals) > 1 and vals[1]:
                        uv_idx = int(vals[1]) - 1
                        uv_indices.append((v_idx, uv_idx))
                faces_raw.append((current_material, indices, uv_indices))

    return vertices, uvs, faces_raw, materials
def normalize_obj(vertices, uvs, faces_raw, materials):
    # --- Normalisasi dengan kombinasi unik (v_idx, vt_idx) ---
    vertices_norm = []
    uvs_norm = []
    faces_norm = [[] for _ in materials]

    index_map = {}
    next_index = 0
    vertex_order = []  # simpan urutan traversal

    for mat_id, indices, uv_indices in faces_raw:
        tri = []
        for v_idx, vt_idx in uv_indices:
            key = (v_idx, vt_idx)
            if key not in index_map:
                index_map[key] = next_index
                next_index += 1
                # simpan vertex sesuai urutan face traversal
                vertices_norm.append(vertices[v_idx])
                if vt_idx is not None and 0 <= vt_idx < len(uvs):
                    uvs_norm.append(uvs[vt_idx])
                else:
                    uvs_norm.append((0.0, 0.0))
                vertex_order.append(v_idx)  # catat urutan asli
            tri.append(index_map[key])
        faces_norm[mat_id].append(tri)

    return vertices_norm, uvs_norm, faces_norm, vertex_order
def import_custom_obj(filepath, source_index=0):
    global mesh_count, texture_count

    # --- Parse & normalize OBJ ---
    vertices, uvs, faces_raw, materials = parse_obj(filepath)
    vertices_norm, uvs_norm, faces_norm, vertex_order = normalize_obj(vertices, uvs, faces_raw, materials)

    # --- Tambah mesh baru ---
    mesh_count += 1
    i = mesh_count - 1

    # Copy struktur default dari mesh yang dipilih
    mesh_header.append(copy.deepcopy(mesh_header[source_index]))
    mesh_bones_header_offset.append(copy.deepcopy(mesh_bones_header_offset[source_index]))
    mesh_bones_count.append(copy.deepcopy(mesh_bones_count[source_index]))
    mesh_bones.append(copy.deepcopy(mesh_bones[source_index]))
    mesh_data_header_offset.append(copy.deepcopy(mesh_data_header_offset[source_index]))
    mesh_data_start_offset.append(copy.deepcopy(mesh_data_start_offset[source_index]))
    mesh_data_lenght.append(copy.deepcopy(mesh_data_lenght[source_index]))
    mesh_flag.append(copy.deepcopy(mesh_flag[source_index]))
    mesh_flag_boolean.append(copy.deepcopy(mesh_flag_boolean[source_index]))
    mesh_flag_binary.append(copy.deepcopy(mesh_flag_binary[source_index]))
    mesh_flag_decode.append(copy.deepcopy(mesh_flag_decode[source_index]))
    mesh_material_header_offset.append(copy.deepcopy(mesh_material_header_offset[source_index]))
    mesh_material.append([])
    mesh_material_faces_header_offset.append([])
    mesh_material_faces_start_offset.append([])
    mesh_faces_header.append([])
    mesh_face_count.append([])
    mesh_face_offset.append([])
    mesh_face.append([])

    # Replace bagian dinamis
    mesh_data_count.append(len(vertices_norm))

    # Inisialisasi field baru sesuai read/write
    mesh_data.append([])
    mesh_bones_weight.append([])
    mesh_uv_u.append([])
    mesh_uv_v.append([])
    mesh_vertex_color.append([])
    mesh_normal_x.append([])
    mesh_normal_y.append([])
    mesh_normal_z.append([])
    mesh_vertex_x.append([])
    mesh_vertex_y.append([])
    mesh_vertex_z.append([])

    # Isi vertex, normal, UV, color, bones weight
    for j, (vx, vy, vz) in enumerate(vertices_norm):
        coord_x = vx
        coord_y = vz
        coord_z = -vy
        orig_x, orig_y, orig_z = rotate_3d_x(coord_x, coord_y, coord_z, 180)

        mesh_vertex_x[i].append(orig_x)
        mesh_vertex_y[i].append(orig_y)
        mesh_vertex_z[i].append(orig_z)

        # normal dummy
        mesh_normal_x[i].append(0.0)
        mesh_normal_y[i].append(0.0)
        mesh_normal_z[i].append(1.0)

        # UV
        u, v = uvs_norm[j]
        mesh_uv_u[i].append(u)
        mesh_uv_v[i].append(v)

        # vertex color default putih
        mesh_vertex_color[i].append((255, 255, 255, 255))

        # bones weight copy dari source (atau kosong)
        if mesh_bones_weight[source_index]:
            mesh_bones_weight[i].append(copy.deepcopy(mesh_bones_weight[source_index][0]))
        else:
            mesh_bones_weight[i].append([])

    # Mesh data blok dummy (copy dari mesh yang dipilih)
    src_blocks = mesh_data[source_index]
    src_len = len(src_blocks)
    for j, v_idx in enumerate(vertex_order):
        block_template = src_blocks[j % src_len]
        mesh_data[i].append(copy.deepcopy(block_template))

    # Materials
    mesh_material_count.append(len(materials))
    mesh_material_texture.append([])
    mesh_material_faces_count.append([])

    for j, mat_name in enumerate(materials):
        mesh_material[i].append(copy.deepcopy(mesh_material[source_index][0]))
        texture_count += 1
        mesh_material_texture[i].append(texture_count - 1)

        mesh_material_faces_count[i].append(len(faces_norm[j]))
        mesh_material_faces_header_offset[i].append(0)
        mesh_material_faces_start_offset[i].append(0)

        mesh_faces_header[i].append([])
        mesh_face_count[i].append([])
        mesh_face_offset[i].append([])
        mesh_face[i].append([])

        for tri in faces_norm[j]:
            triangle = [int(v) for v in tri]
            mesh_faces_header[i][j].append(copy.deepcopy(mesh_faces_header[source_index][0][0]))
            mesh_face_count[i][j].append(len(triangle))
            mesh_face_offset[i][j].append(0)
            mesh_face[i][j].append(triangle)

        tex_name = mat_name.encode("ascii").decode("ascii").rstrip("\x00")[:16]
        texture.append(tex_name)

    return True
def export_object_data(i, filename):
    offset_list = []
    try:
        with open(filename, "wb") as f:
            f.seek(0)
            # jumlah slot sesuai bagian mesh yang mau diekspor
            for j in range(39):  # header, bones, data, flag, uv, vertex, material/faces, texture, plus variabel baru
                offset_list.append(f.tell())
                f.write(b'\x00' * 4)  # offset
                f.write(b'\x00' * 4)  # length
    except IOError:
        print(f"Cannot open {filename}")
        return 1

    try:
        with open(filename, "r+b") as f:
            # 0 mesh_header
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(mesh_header[i])
            length = f.tell() - offset
            f.seek(offset_list[0]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 1 mesh_bones_header_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_bones_header_offset[i]))
            length = f.tell() - offset
            f.seek(offset_list[1]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 2 mesh_bones_count
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_bones_count[i]))
            length = f.tell() - offset
            f.seek(offset_list[2]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 3 mesh_bones
            f.seek(0, os.SEEK_END); offset = f.tell()
            for bone_id in mesh_bones[i]:
                f.write(struct.pack("<I", bone_id))
            length = f.tell() - offset
            f.seek(offset_list[3]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 4 mesh_data_header_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_data_header_offset[i]))
            length = f.tell() - offset
            f.seek(offset_list[4]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 5 mesh_data_start_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_data_start_offset[i]))
            length = f.tell() - offset
            f.seek(offset_list[5]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 6 mesh_data_lenght
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_data_lenght[i]))
            length = f.tell() - offset
            f.seek(offset_list[6]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 7 mesh_data_count
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_data_count[i]))
            length = f.tell() - offset
            f.seek(offset_list[7]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 8 mesh_data
            f.seek(0, os.SEEK_END); offset = f.tell()
            for block in mesh_data[i]:
                f.write(block)
            length = f.tell() - offset
            f.seek(offset_list[8]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 9 mesh_flag
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_flag[i]))
            length = f.tell() - offset
            f.seek(offset_list[9]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 10 mesh_flag_boolean
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<?", mesh_flag_boolean[i]))
            length = f.tell() - offset
            f.seek(offset_list[10]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 11 mesh_flag_binary
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(mesh_flag_binary[i].encode("ascii"))
            length = f.tell() - offset
            f.seek(offset_list[11]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 12 mesh_flag_decode
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_flag_decode[i]))
            length = f.tell() - offset
            f.seek(offset_list[12]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 13 mesh_bones_weight
            f.seek(0, os.SEEK_END); offset = f.tell()
            for weights in mesh_bones_weight[i]:
                for w in weights:
                    f.write(struct.pack("<f", w))
            length = f.tell() - offset
            f.seek(offset_list[13]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 14 mesh_uv_u
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_uv_u[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[14]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 15 mesh_uv_v
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_uv_v[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[15]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 16 mesh_vertex_color
            f.seek(0, os.SEEK_END); offset = f.tell()
            for col in mesh_vertex_color[i]:
                f.write(struct.pack("BBBB", *col))
            length = f.tell() - offset
            f.seek(offset_list[16]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 17 mesh_normal_x
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_normal_x[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[17]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 18 mesh_normal_y
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_normal_y[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[18]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 19 mesh_normal_z
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_normal_z[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[19]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 20 mesh_vertex_x
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_vertex_x[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[20]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 21 mesh_vertex_y
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_vertex_y[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[21]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 22 mesh_vertex_z
            f.seek(0, os.SEEK_END); offset = f.tell()
            for val in mesh_vertex_z[i]:
                f.write(struct.pack("<f", val))
            length = f.tell() - offset
            f.seek(offset_list[22]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 23 mesh_material_count
            f.seek(0, os.SEEK_END); offset = f.tell()
            f.write(struct.pack("<I", mesh_material_count[i]))
            length = f.tell() - offset
            f.seek(offset_list[23]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

                        # 24 mesh_material
            f.seek(0, os.SEEK_END); offset = f.tell()
            for mat in mesh_material[i]:
                f.write(mat)
            length = f.tell() - offset
            f.seek(offset_list[24]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 25 mesh_material_texture
            f.seek(0, os.SEEK_END); offset = f.tell()
            for tex in mesh_material_texture[i]:
                f.write(struct.pack("<H", tex))
            length = f.tell() - offset
            f.seek(offset_list[25]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 26 mesh_material_faces_count
            f.seek(0, os.SEEK_END); offset = f.tell()
            for cnt in mesh_material_faces_count[i]:
                f.write(struct.pack("<I", cnt))
            length = f.tell() - offset
            f.seek(offset_list[26]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 27 mesh_material_faces_header_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            for j in mesh_material_faces_header_offset[i]:
                f.write(struct.pack("<I", j))
            length = f.tell() - offset
            f.seek(offset_list[27]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 28 mesh_material_faces_start_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            for j in mesh_material_faces_start_offset[i]:
                f.write(struct.pack("<I", j))
            length = f.tell() - offset
            f.seek(offset_list[28]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 29 mesh_faces_header
            f.seek(0, os.SEEK_END); offset = f.tell()
            for mat in mesh_faces_header[i]:
                for face in mat:
                    f.write(face)
            length = f.tell() - offset
            f.seek(offset_list[29]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 30 mesh_face_count
            f.seek(0, os.SEEK_END); offset = f.tell()
            for mat in mesh_face_count[i]:
                for cnt in mat:
                    f.write(struct.pack("<I", cnt))
            length = f.tell() - offset
            f.seek(offset_list[30]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 31 mesh_face_offset
            f.seek(0, os.SEEK_END); offset = f.tell()
            for mat in mesh_face_offset[i]:
                for off in mat:
                    f.write(struct.pack("<I", off))
            length = f.tell() - offset
            f.seek(offset_list[31]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 32 mesh_face
            f.seek(0, os.SEEK_END); offset = f.tell()
            for mat in mesh_face[i]:
                for face in mat:
                    for idx in face:
                        f.write(struct.pack("<H", idx))
            length = f.tell() - offset
            f.seek(offset_list[32]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

            # 33 texture
            f.seek(0, os.SEEK_END); offset = f.tell()
            for texname in texture:
                f.write(texname.encode("ascii").ljust(16, b"\x00"))
            length = f.tell() - offset
            f.seek(offset_list[33]); f.write(struct.pack("<I", offset)); f.write(struct.pack("<I", length))

    except IOError:
        print(f"Cannot open {filename}")
        return 1
def import_object_data(filename):
    global mesh_count, texture_count
    mesh_count += 1
    i = mesh_count - 1
    offset_list = []
    length_list = []
    try:
        with open(filename, "rb") as f:
            # baca semua offset/length
            for j in range(34):  # jumlah slot sesuai export terbaru
                offset = struct.unpack("<I", f.read(4))[0]
                length = struct.unpack("<I", f.read(4))[0]
                offset_list.append(offset)
                length_list.append(length)

            # 0 mesh_header
            f.seek(offset_list[0])
            mesh_header.append(f.read(length_list[0]))

            # 1 mesh_bones_header_offset
            f.seek(offset_list[1])
            mesh_bones_header_offset.append(struct.unpack("<I", f.read(4))[0])

            # 2 mesh_bones_count
            f.seek(offset_list[2])
            mesh_bones_count.append(struct.unpack("<I", f.read(4))[0])

            # 3 mesh_bones
            f.seek(offset_list[3])
            mesh_bones.append([])
            for _ in range(length_list[3] // 4):
                mesh_bones[i].append(struct.unpack("<I", f.read(4))[0])

            # 4 mesh_data_header_offset
            f.seek(offset_list[4])
            mesh_data_header_offset.append(struct.unpack("<I", f.read(4))[0])

            # 5 mesh_data_start_offset
            f.seek(offset_list[5])
            mesh_data_start_offset.append(struct.unpack("<I", f.read(4))[0])

            # 6 mesh_data_lenght
            f.seek(offset_list[6])
            mesh_data_lenght.append(struct.unpack("<I", f.read(4))[0])

            # 7 mesh_data_count
            f.seek(offset_list[7])
            mesh_data_count.append(struct.unpack("<I", f.read(4))[0])

            # 8 mesh_data
            f.seek(offset_list[8])
            mesh_data.append([])
            for _ in range(mesh_data_count[i]):
                block_len = length_list[8] // mesh_data_count[i]
                mesh_data[i].append(f.read(block_len))

            # 9 mesh_flag
            f.seek(offset_list[9])
            mesh_flag.append(struct.unpack("<I", f.read(4))[0])

            # 10 mesh_flag_boolean
            f.seek(offset_list[10])
            mesh_flag_boolean.append(struct.unpack("<?", f.read(1))[0])

            # 11 mesh_flag_binary
            f.seek(offset_list[11])
            mesh_flag_binary.append(f.read(length_list[11]).decode("ascii"))

            # 12 mesh_flag_decode
            f.seek(offset_list[12])
            mesh_flag_decode.append(struct.unpack("<I", f.read(4))[0])

            # 13 mesh_bones_weight
            f.seek(offset_list[13])
            mesh_bones_weight.append([])
            for _ in range(mesh_data_count[i]):
                weights = []
                for _ in range(mesh_bones_count[i]):
                    weights.append(struct.unpack("<f", f.read(4))[0])
                mesh_bones_weight[i].append(weights)

            # 14 mesh_uv_u
            f.seek(offset_list[14])
            mesh_uv_u.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[14] // 4)])

            # 15 mesh_uv_v
            f.seek(offset_list[15])
            mesh_uv_v.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[15] // 4)])

            # 16 mesh_vertex_color
            f.seek(offset_list[16])
            mesh_vertex_color.append([struct.unpack("BBBB", f.read(4)) for _ in range(length_list[16] // 4)])

            # 17 mesh_normal_x
            f.seek(offset_list[17])
            mesh_normal_x.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[17] // 4)])

            # 18 mesh_normal_y
            f.seek(offset_list[18])
            mesh_normal_y.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[18] // 4)])

            # 19 mesh_normal_z
            f.seek(offset_list[19])
            mesh_normal_z.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[19] // 4)])

            # 20 mesh_vertex_x
            f.seek(offset_list[20])
            mesh_vertex_x.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[20] // 4)])

            # 21 mesh_vertex_y
            f.seek(offset_list[21])
            mesh_vertex_y.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[21] // 4)])

            # 22 mesh_vertex_z
            f.seek(offset_list[22])
            mesh_vertex_z.append([struct.unpack("<f", f.read(4))[0] for _ in range(length_list[22] // 4)])

            # 23 mesh_material_count
            f.seek(offset_list[23])
            mesh_material_count.append(struct.unpack("<I", f.read(4))[0])

            # 24 mesh_material
            f.seek(offset_list[24])
            mesh_material.append([])
            for _ in range(mesh_material_count[i]):
                mat_len = length_list[24] // mesh_material_count[i]
                mesh_material[i].append(f.read(mat_len))

            # 25 mesh_material_texture (pakai logika increment texture_count)
            f.seek(offset_list[25])
            mesh_material_texture.append([])
            for _ in range(length_list[25] // 2):
                texture_count += 1
                mesh_material_texture[i].append(texture_count - 1)

            # 26 mesh_material_faces_count
            f.seek(offset_list[26])
            mesh_material_faces_count.append([struct.unpack("<I", f.read(4))[0] for _ in range(length_list[26] // 4)])

            # 27 mesh_material_faces_header_offset
            f.seek(offset_list[27])
            mesh_material_faces_header_offset.append([struct.unpack("<I", f.read(4))[0] for _ in range(length_list[27] // 4)])

            # 28 mesh_material_faces_start_offset
            f.seek(offset_list[28])
            mesh_material_faces_start_offset.append([struct.unpack("<I", f.read(4))[0] for _ in range(length_list[28] // 4)])

            # 29 mesh_faces_header
            f.seek(offset_list[29])
            mesh_faces_header.append([])
            for j in range(mesh_material_count[i]):
                mesh_faces_header[i].append([])
                for k in range(mesh_material_faces_count[i][j]):
                    mesh_faces_header[i][j].append(f.read(16))

            # 30 mesh_face_count
            f.seek(offset_list[30])
            mesh_face_count.append([])
            for j in range(mesh_material_count[i]):
                mesh_face_count[i].append([])
                for k in range(mesh_material_faces_count[i][j]):
                    mesh_face_count[i][j].append(struct.unpack("<I", f.read(4))[0])

            # 31 mesh_face_offset
            f.seek(offset_list[31])
            mesh_face_offset.append([])
            for j in range(mesh_material_count[i]):
                mesh_face_offset[i].append([])
                for k in range(mesh_material_faces_count[i][j]):
                    mesh_face_offset[i][j].append(struct.unpack("<I", f.read(4))[0])

            # 32 mesh_face
            f.seek(offset_list[32])
            mesh_face.append([])
            for j in range(mesh_material_count[i]):
                mesh_face[i].append([])
                for k in range(mesh_material_faces_count[i][j]):
                    mesh_face[i][j].append([])
                    for l in range(mesh_face_count[i][j][k]):
                        mesh_face[i][j][k].append(struct.unpack("<H", f.read(2))[0])

            # 33 texture
            f.seek(offset_list[33])
            for _ in range(length_list[33] // 16):
                texture.append(f.read(16).decode("ascii").rstrip("\x00"))

    except IOError:
        print(f"Cannot open {filename}")
        return 1
def export_dae(i, filename):
    collada = ET.Element("COLLADA", {
        "xmlns": "http://www.collada.org/2005/11/COLLADASchema",
        "version": "1.4.1"
    })
    def make_matrix(px, py, pz, rx, ry, rz):
        cx, cy, cz = math.cos(rx), math.cos(ry), math.cos(rz)
        sx, sy, sz = math.sin(rx), math.sin(ry), math.sin(rz)
        m00 = cy*cz
        m01 = -cy*sz
        m02 = sy
        m10 = sx*sy*cz+cx*sz
        m11 = -sx*sy*sz+cx*cz
        m12 = -sx*cy
        m20 = -cx*sy*cz+sx*sz
        m21 = cx*sy*sz+sx*cz
        m22 = cx*cy
        return f"{m00} {m01} {m02} {px}  {m10} {m11} {m12} {py}  {m20} {m21} {m22} {pz}  0 0 0 1"
    # --- Geometry untuk mesh i ---
    lib_geom = ET.SubElement(collada, "library_geometries")
    geom = ET.SubElement(lib_geom, "geometry", id=f"Mesh{i}", name=f"Mesh{i}")
    mesh = ET.SubElement(geom, "mesh")

    # positions
    pos_source = ET.SubElement(mesh, "source", id=f"Mesh{i}-positions")
    pos_array = ET.SubElement(pos_source, "float_array",
                              id=f"Mesh{i}-positions-array",
                              count=str(mesh_data_count[i]*3))
    verts = []
    for j in range(mesh_data_count[i]):
        verts.extend([mesh_vertex_x[i][j], mesh_vertex_y[i][j], mesh_vertex_z[i][j]])
    pos_array.text = " ".join(str(round(v,6)) for v in verts)

    tech = ET.SubElement(pos_source, "technique_common")
    acc = ET.SubElement(tech, "accessor",
                        source=f"#Mesh{i}-positions-array",
                        count=str(mesh_data_count[i]), stride="3")
    ET.SubElement(acc, "param", name="X", type="float")
    ET.SubElement(acc, "param", name="Y", type="float")
    ET.SubElement(acc, "param", name="Z", type="float")

    # vertices
    vertices = ET.SubElement(mesh, "vertices", id=f"Mesh{i}-vertices")
    ET.SubElement(vertices, "input", semantic="POSITION", source=f"#Mesh{i}-positions")

    # faces (triangulasi)
    tris_list = []
    for j in range(mesh_material_count[i]):
        for k in range(mesh_material_faces_count[i][j]):
            face_indices = mesh_face[i][j][k]
            if len(face_indices) >= 3:
                tris_list.append([face_indices[0], face_indices[1], face_indices[2]])
                for n in range(1, len(face_indices)-2):
                    if n % 2 == 1:
                        v1, v2, v3 = face_indices[n], face_indices[n+2], face_indices[n+1]
                    else:
                        v1, v2, v3 = face_indices[n], face_indices[n+1], face_indices[n+2]
                    tris_list.append([v1, v2, v3])
    tris = ET.SubElement(mesh, "triangles", count=str(len(tris_list)))
    ET.SubElement(tris, "input", semantic="VERTEX", source=f"#Mesh{i}-vertices", offset="0")
    p = ET.SubElement(tris, "p")
    p.text = " ".join(str(idx) for tri in tris_list for idx in tri)

    # --- Controller untuk mesh i ---
    lib_ctrl = ET.SubElement(collada, "library_controllers")
    ctrl = ET.SubElement(lib_ctrl, "controller", id=f"Mesh{i}-skin")
    skin = ET.SubElement(ctrl, "skin", source=f"#Mesh{i}")
    ET.SubElement(skin, "bind_shape_matrix").text = "1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1"

    # joints
    src_joints = ET.SubElement(skin, "source", id=f"Mesh{i}-joints")
    name_array = ET.SubElement(src_joints, "Name_array",
                               id=f"Mesh{i}-joints-array",
                               count=str(mesh_bones_count[i]))
    valid_bones = [bone_name[b] if 0 <= b < len(bone_name) else f"Bone{b}" for b in mesh_bones[i]]
    name_array.text = " ".join(valid_bones)

    tech = ET.SubElement(src_joints, "technique_common")
    acc = ET.SubElement(tech, "accessor",
                        source=f"#Mesh{i}-joints-array",
                        count=str(len(valid_bones)), stride="1")
    ET.SubElement(acc, "param", name="JOINT", type="Name")

    # inverse bind matrix (identity)
    src_bind = ET.SubElement(skin, "source", id=f"Mesh{i}-bindposes")
    float_array = ET.SubElement(src_bind, "float_array",
                                id=f"Mesh{i}-bindposes-array",
                                count=str(len(valid_bones)*16))
    float_array.text = " ".join(["1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1"] * len(valid_bones))
    tech = ET.SubElement(src_bind, "technique_common")
    acc = ET.SubElement(tech, "accessor",
                        source=f"#Mesh{i}-bindposes-array",
                        count=str(len(valid_bones)), stride="16")
    ET.SubElement(acc, "param", name="TRANSFORM", type="float4x4")

    # weights
    weights_flat = []
    vcount_list = []
    vw_pairs = []
    weight_counter = 0

    for j in range(mesh_data_count[i]):
        weights = mesh_bones_weight[i][j]
        valid_pairs = []
        for k, w in enumerate(weights):
            if w > 0:
                valid_pairs.append((k, w))
            else:
                # tambahkan dummy kecil supaya group tetap ada
                valid_pairs.append((k, 1e-6))

        total = sum(w for _, w in valid_pairs)
        if total >= 0:
            valid_pairs = [(k, w/total) for k, w in valid_pairs]

        vcount_list.append(len(valid_pairs))
        for k, w in valid_pairs:
            vw_pairs.extend([k, weight_counter])
            weights_flat.append(w)
            weight_counter += 1


    src_weights = ET.SubElement(skin, "source", id=f"Mesh{i}-weights")
    float_array = ET.SubElement(src_weights, "float_array",
                                id=f"Mesh{i}-weights-array",
                                count=str(len(weights_flat)))
    float_array.text = " ".join(str(round(w,6)) for w in weights_flat)
    tech = ET.SubElement(src_weights, "technique_common")
    acc = ET.SubElement(tech, "accessor",
                        source=f"#Mesh{i}-weights-array",
                        count=str(len(weights_flat)), stride="1")
    ET.SubElement(acc, "param", name="WEIGHT", type="float")

    # joints block
    joints_block = ET.SubElement(skin, "joints")
    ET.SubElement(joints_block, "input", semantic="JOINT", source=f"#Mesh{i}-joints")
    ET.SubElement(joints_block, "input", semantic="INV_BIND_MATRIX", source=f"#Mesh{i}-bindposes")

    # vertex_weights
    vw = ET.SubElement(skin, "vertex_weights", count=str(mesh_data_count[i]))
    ET.SubElement(vw, "input", semantic="JOINT", source=f"#Mesh{i}-joints", offset="0")
    ET.SubElement(vw, "input", semantic="WEIGHT", source=f"#Mesh{i}-weights", offset="1")
    vcount = ET.SubElement(vw, "vcount")
    vcount.text = " ".join(str(x) for x in vcount_list)
    v = ET.SubElement(vw, "v")
    v.text = " ".join(str(x) for x in vw_pairs)

    # --- Visual Scene ---
    lib_scene = ET.SubElement(collada, "library_visual_scenes")
    scene = ET.SubElement(lib_scene, "visual_scene", id="Scene", name="Scene")
    armature_node = ET.SubElement(scene, "node", id="Armature", name="Armature", type="NODE")

    # kumpulkan semua bones yang dipakai + parent chain
    export_bones = set(mesh_bones[i])
    for b in list(mesh_bones[i]):
        p = bone_parrent[b]
        while p >= 0 and p < len(bone_parrent) and p not in export_bones:
            export_bones.add(p)
            p = bone_parrent[p]

    # buat node JOINT untuk setiap bone yang akan diekspor
    bone_nodes = {}
    for b in export_bones:
        node = ET.Element("node", id=bone_name[b], name=bone_name[b], sid=bone_name[b], type="JOINT")
        mat = ET.SubElement(node, "matrix")
        mat.text = make_matrix(
            bone_local_position_x[b],
            bone_local_position_y[b],
            bone_local_position_z[b],
            bone_rotation_x[b],
            bone_rotation_y[b],
            bone_rotation_z[b]
        )
        bone_nodes[b] = node

    # susun hierarki parent-child
    for b in export_bones:
        parent = bone_parrent[b]
        if parent in bone_nodes:
            bone_nodes[parent].append(bone_nodes[b])
        else:
            armature_node.append(bone_nodes[b])

    # tambahkan node mesh i yang meng‑instance controller
    mesh_node = ET.SubElement(armature_node, "node", id=f"Object{i}", name=f"Object{i}")
    inst_ctrl = ET.SubElement(mesh_node, "instance_controller", url=f"#Mesh{i}-skin")
    # skeleton root: ambil bone pertama yang tidak punya parent
    root_idx = next((idx for idx in mesh_bones[i] if bone_parrent[idx] < 0), mesh_bones[i][0])
    ET.SubElement(inst_ctrl, "skeleton").text = f"#{bone_name[root_idx]}"

    # Scene root
    sc = ET.SubElement(collada, "scene")
    ET.SubElement(sc, "instance_visual_scene", url="#Scene")

    # Simpan ke file
    tree = ET.ElementTree(collada)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
def export_as_one_dae(filename):
    """
    Robust COLLADA exporter yang sinkron 100% dengan fungsi import_from_dae.
    Mendukung Real Materials dengan Image Texture Binding (.png) otomatis dari folder yang sama.
    """
    global mesh_count, mesh_data_count, mesh_bones_count, mesh_bones, mesh_bones_weight
    global mesh_vertex_x, mesh_vertex_y, mesh_vertex_z, mesh_normal_x, mesh_normal_y, mesh_normal_z
    global mesh_uv_u, mesh_uv_v, mesh_material_count, mesh_material_texture, mesh_material_faces_count
    global mesh_face, bone_count, bone_parrent, bone_name
    global bone_local_position_x, bone_local_position_y, bone_local_position_z
    global bone_rotation_x, bone_rotation_y, bone_rotation_z, texture

    # --- Helper Matriks & Rotasi ---
    def mat_mult(a, b):
        r = [0.0]*16
        for i in range(4):
            for j in range(4):
                s = 0.0
                for k in range(4): s += a[i*4 + k] * b[k*4 + j]
                r[i*4 + j] = s
        return r

    def mat_inverse(a):
        inv = [0.0]*16
        m = a
        inv[0] = m[5]*m[10]*m[15] - m[5]*m[11]*m[14] - m[9]*m[6]*m[15] + m[9]*m[7]*m[14] + m[13]*m[6]*m[11] - m[13]*m[7]*m[10]
        inv[4] = -m[4]*m[10]*m[15] + m[4]*m[11]*m[14] + m[8]*m[6]*m[15] - m[8]*m[7]*m[14] - m[12]*m[6]*m[11] + m[12]*m[7]*m[10]
        inv[8] = m[4]*m[9]*m[15] - m[4]*m[11]*m[13] - m[8]*m[5]*m[15] + m[8]*m[7]*m[13] + m[12]*m[5]*m[11] - m[12]*m[7]*m[9]
        inv[12] = -m[4]*m[9]*m[14] + m[4]*m[10]*m[13] + m[8]*m[5]*m[14] - m[8]*m[6]*m[13] - m[12]*m[5]*m[10] + m[12]*m[6]*m[9]
        inv[1] = -m[1]*m[10]*m[15] + m[1]*m[11]*m[14] + m[9]*m[2]*m[15] - m[9]*m[3]*m[14] - m[13]*m[2]*m[11] + m[13]*m[3]*m[10]
        inv[5] = m[0]*m[10]*m[15] - m[0]*m[11]*m[14] - m[8]*m[2]*m[15] + m[8]*m[3]*m[14] + m[12]*m[2]*m[11] - m[12]*m[3]*m[10]
        inv[9] = -m[0]*m[9]*m[15] + m[0]*m[11]*m[13] + m[8]*m[1]*m[15] - m[8]*m[3]*m[13] - m[12]*m[1]*m[11] + m[12]*m[3]*m[9]
        inv[13] = m[0]*m[9]*m[14] - m[0]*m[10]*m[13] - m[8]*m[1]*m[14] + m[8]*m[2]*m[13] + m[12]*m[1]*m[10] - m[12]*m[2]*m[9]
        inv[2] = m[1]*m[6]*m[15] - m[1]*m[7]*m[14] - m[5]*m[2]*m[15] + m[5]*m[3]*m[14] + m[13]*m[2]*m[7] - m[13]*m[3]*m[6]
        inv[6] = -m[0]*m[6]*m[15] + m[0]*m[7]*m[14] + m[4]*m[2]*m[15] - m[4]*m[3]*m[14] - m[12]*m[2]*m[7] + m[12]*m[3]*m[6]
        inv[10] = m[0]*m[5]*m[15] - m[0]*m[7]*m[13] - m[4]*m[1]*m[15] + m[4]*m[3]*m[13] + m[12]*m[1]*m[7] - m[12]*m[3]*m[5]
        inv[14] = -m[0]*m[5]*m[14] + m[0]*m[6]*m[13] + m[4]*m[1]*m[14] - m[4]*m[2]*m[13] - m[12]*m[1]*m[6] + m[12]*m[2]*m[5]
        inv[3] = -m[1]*m[6]*m[11] + m[1]*m[7]*m[10] + m[5]*m[2]*m[11] - m[5]*m[3]*m[10] - m[9]*m[2]*m[7] + m[9]*m[3]*m[6]
        inv[7] = m[0]*m[6]*m[11] - m[0]*m[7]*m[10] - m[4]*m[2]*m[11] + m[4]*m[3]*m[10] + m[8]*m[2]*m[7] - m[8]*m[3]*m[6]
        inv[11] = -m[0]*m[5]*m[11] + m[0]*m[7]*m[9] + m[4]*m[1]*m[11] - m[4]*m[3]*m[9] - m[8]*m[1]*m[7] + m[8]*m[3]*m[5]
        inv[15] = m[0]*m[5]*m[10] - m[0]*m[6]*m[9] - m[4]*m[1]*m[10] + m[4]*m[2]*m[9] + m[8]*m[1]*m[6] - m[8]*m[2]*m[5]
        det = m[0]*inv[0] + m[1]*inv[4] + m[2]*inv[8] + m[3]*inv[12]
        if abs(det) < 1e-12: return [1.0,0,0,0, 0,1.0,0,0, 0,0,1.0,0, 0,0,0,1.0]
        return [x / det for x in inv]

    def make_matrix(px, py, pz, rx, ry, rz):
        cx, cy, cz = math.cos(rx), math.cos(ry), math.cos(rz)
        sx, sy, sz = math.sin(rx), math.sin(ry), math.sin(rz)
        m00, m01, m02 = cy*cz, -cy*sz, sy
        m10, m11, m12 = sx*sy*cz+cx*sz, -sx*sy*sz+cx*cz, -sx*cy
        m20, m21, m22 = -cx*sy*cz+sx*sz, cx*sy*sz+sx*cz, cx*cy
        return f"{m00} {m01} {m02} {px} {m10} {m11} {m12} {py} {m20} {m21} {m22} {pz} 0 0 0 1"

    def rotate_3d_x(x, y, z, angle_deg):
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a

    mesh_material_mappings = []
    unique_materials = sorted(list(set(texture)))

    collada = ET.Element("COLLADA", {"xmlns": "http://www.collada.org/2005/11/COLLADASchema", "version": "1.4.1"})
    
    asset = ET.SubElement(collada, "asset")
    ET.SubElement(asset, "up_axis").text = "Z_UP"

    # =================================================================
    # [BARU] DUKUNGAN LINK GAMBAR TEKSTUR (.png otomatis selevel folder)
    # =================================================================
    # 1. Library Images (Mendaftarkan path file gambar eksternal)
    lib_images = ET.SubElement(collada, "library_images")
    for mat_name in unique_materials:
        img_node = ET.SubElement(lib_images, "image", id=f"{mat_name}-image", name=f"{mat_name}-image")
        # Menggunakan path relatif langsung ("head.png") agar Blender mencari di folder yang sama dengan file DAE
        ET.SubElement(img_node, "init_from").text = f"{mat_name}.png"

    # 2. Library Effects (Konfigurasi Sampler2D & Surface Tekstur)
    lib_effects = ET.SubElement(collada, "library_effects")
    for mat_name in unique_materials:
        eff = ET.SubElement(lib_effects, "effect", id=f"{mat_name}-effect")
        profile = ET.SubElement(eff, "profile_COMMON")
        
        # Buat parameter 2D Surface yang merujuk ke Image ID
        newparam_surf = ET.SubElement(profile, "newparam", sid=f"{mat_name}-surface")
        surf = ET.SubElement(newparam_surf, "surface", type="2D")
        ET.SubElement(surf, "init_from").text = f"{mat_name}-image"
        
        # Buat parameter Sampler2D yang membungkus Surface tersebut
        newparam_samp = ET.SubElement(profile, "newparam", sid=f"{mat_name}-sampler")
        samp = ET.SubElement(newparam_samp, "sampler2D")
        ET.SubElement(samp, "source").text = f"{mat_name}-surface"
        
        technique = ET.SubElement(profile, "technique", sid="common")
        lambert = ET.SubElement(technique, "lambert")
        diffuse = ET.SubElement(lambert, "diffuse")
        
        # Definisikan elemen tekstur nyata alih-alih sekadar warna flat <color>
        tex_el = ET.SubElement(diffuse, "texture", texture=f"{mat_name}-sampler", texcoord="UVSET0")

    # 3. Library Materials
    lib_materials = ET.SubElement(collada, "library_materials")
    for mat_name in unique_materials:
        material_node = ET.SubElement(lib_materials, "material", id=mat_name, name=mat_name)
        ET.SubElement(material_node, "instance_effect", url=f"#{mat_name}-effect")

    # =================================================================
    # 4. Library Geometries (Vertex, Normal, UV)
    # =================================================================
    lib_geom = ET.SubElement(collada, "library_geometries")
    for i in range(mesh_count):
        v_count = mesh_data_count[i]
        geom = ET.SubElement(lib_geom, "geometry", id=f"Mesh{i}", name=f"Mesh{i}")
        mesh = ET.SubElement(geom, "mesh")

        # --- A. POSITIONS DATA ---
        pos_source = ET.SubElement(mesh, "source", id=f"Mesh{i}-positions")
        pos_array = ET.SubElement(pos_source, "float_array", id=f"Mesh{i}-positions-array", count=str(v_count * 3))
        verts_flat = []
        for j in range(v_count):
            vx, vy, vz = mesh_vertex_x[i][j], mesh_vertex_y[i][j], mesh_vertex_z[i][j]
            rx, ry, rz = rotate_3d_x(vx, vy, vz, -90)
            verts_flat.extend([rx, -rz, ry])
        pos_array.text = " ".join(str(round(v, 6)) for v in verts_flat)
        tech_pos = ET.SubElement(pos_source, "technique_common")
        acc_pos = ET.SubElement(tech_pos, "accessor", source=f"#Mesh{i}-positions-array", count=str(v_count), stride="3")
        for ax in ["X", "Y", "Z"]: ET.SubElement(acc_pos, "param", name=ax, type="float")

        # --- B. NORMALS DATA ---
        norm_source = ET.SubElement(mesh, "source", id=f"Mesh{i}-normals")
        norm_array = ET.SubElement(norm_source, "float_array", id=f"Mesh{i}-normals-array", count=str(v_count * 3))
        norms_flat = []
        for j in range(v_count):
            nx, ny, nz = mesh_normal_x[i][j], mesh_normal_y[i][j], mesh_normal_z[i][j]
            
            # KOREKSI: Putar aksis normal agar selaras dengan posisi vertex
            rnx, rny, rnz = rotate_3d_x(nx, ny, nz, -90)
            transformed_nx, transformed_ny, transformed_nz = rnx, -rnz, rny
            
            # Normalisasi vektor hasil rotasi agar panjangnya tepat 1.0 (standar COLLADA)
            length = (transformed_nx**2 + transformed_ny**2 + transformed_nz**2)**0.5
            if length > 0.0: 
                transformed_nx /= length
                transformed_ny /= length
                transformed_nz /= length
            else:
                transformed_nx, transformed_ny, transformed_nz = 0.0, 0.0, 1.0 # fallback default Z-up
                
            norms_flat.extend([transformed_nx, transformed_ny, transformed_nz])
            
        norm_array.text = " ".join(str(round(n, 6)) for n in norms_flat)
        tech_norm = ET.SubElement(norm_source, "technique_common")
        acc_norm = ET.SubElement(tech_norm, "accessor", source=f"#Mesh{i}-normals-array", count=str(v_count), stride="3")
        for ax in ["X", "Y", "Z"]: ET.SubElement(acc_norm, "param", name=ax, type="float")

        # --- C. UV DATA ---
        uv_source = ET.SubElement(mesh, "source", id=f"Mesh{i}-uvs")
        uv_array = ET.SubElement(uv_source, "float_array", id=f"Mesh{i}-uvs-array", count=str(v_count * 2))
        uvs_flat = []
        for j in range(v_count):
            uvs_flat.extend([mesh_uv_u[i][j], mesh_uv_v[i][j]])
        uv_array.text = " ".join(str(round(u, 6)) for u in uvs_flat)
        tech_uv = ET.SubElement(uv_source, "technique_common")
        acc_uv = ET.SubElement(tech_uv, "accessor", source=f"#Mesh{i}-uvs-array", count=str(v_count), stride="2")
        ET.SubElement(acc_uv, "param", name="S", type="float")
        ET.SubElement(acc_uv, "param", name="T", type="float")

        # --- D. VERTICES BLOCK ---
        vertices = ET.SubElement(mesh, "vertices", id=f"Mesh{i}-vertices")
        ET.SubElement(vertices, "input", semantic="POSITION", source=f"#Mesh{i}-positions")

        # --- E. MULTI-MATERIAL & TRIANGLES BLOCK ---
        mesh_mats = []
        for j in range(mesh_material_count[i]):
            tex_idx = mesh_material_texture[i][j]
            mat_name = texture[tex_idx] if tex_idx < len(texture) else f"Material_{tex_idx}"
            mesh_mats.append(mat_name)

            tris_list = []
            for k in range(mesh_material_faces_count[i][j]):
                face_indices = mesh_face[i][j][k]
                if len(face_indices) < 3:
                    continue
                
                # Segitiga pertama (Pasti searah bawaan)
                tris_list.append([face_indices[0], face_indices[1], face_indices[2]])
                
                # Triangulasi fan/strip untuk sisa vertex (Quad / Polygon)
                for n in range(1, len(face_indices) - 2):
                    if n % 2 == 1:
                        # Balik urutan vertex (v3 dulu baru v2) agar Winding Order COLLADA konsisten
                        v1, v2, v3 = face_indices[n], face_indices[n+2], face_indices[n+1]
                    else:
                        v1, v2, v3 = face_indices[n], face_indices[n+1], face_indices[n+2]
                    tris_list.append([v1, v2, v3])

            if not tris_list:
                continue

            tris_element = ET.SubElement(mesh, "triangles", count=str(len(tris_list)), material=mat_name)
            ET.SubElement(tris_element, "input", semantic="VERTEX", source=f"#Mesh{i}-vertices", offset="0")
            ET.SubElement(tris_element, "input", semantic="NORMAL", source=f"#Mesh{i}-normals", offset="1")
            ET.SubElement(tris_element, "input", semantic="TEXCOORD", source=f"#Mesh{i}-uvs", offset="2", set="0")

            p_values = []
            for tri in tris_list:
                for idx in tri:
                    p_values.extend([idx, idx, idx])
            
            p_elem = ET.SubElement(tris_element, "p")
            p_elem.text = " ".join(str(x) for x in p_values)

        mesh_material_mappings.append(mesh_mats)

    # =================================================================
    # 5. Library Controllers (Skinning Data)
    # =================================================================
    lib_ctrl = ET.SubElement(collada, "library_controllers")
    world_mats = {}
    identity = [1.0,0,0,0, 0,1.0,0,0, 0,0,1.0,0, 0,0,0,1.0]
    
    for b in range(bone_count):
        chain = []
        p = b
        while p >= 0 and p < bone_count:
            chain.append(p)
            p = bone_parrent[p]
        mat = identity[:]
        for node in reversed(chain):
            local = make_matrix(
                bone_local_position_x[node], bone_local_position_y[node], bone_local_position_z[node],
                bone_rotation_x[node], bone_rotation_y[node], bone_rotation_z[node]
            )
            local_list = [float(x) for x in local.split()] if isinstance(local, str) else local
            mat = mat_mult(mat, local_list)
        world_mats[b] = mat

    global_roots = [idx for idx, p in enumerate(bone_parrent) if p < 0]
    fallback_root = global_roots[0] if global_roots else 0

    for i in range(mesh_count):
        v_count = mesh_data_count[i]
        ctrl = ET.SubElement(lib_ctrl, "controller", id=f"Mesh{i}-skin")
        skin = ET.SubElement(ctrl, "skin", source=f"#Mesh{i}")
        ET.SubElement(skin, "bind_shape_matrix").text = "1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1"

        desired_slots = mesh_bones_count[i] if i < len(mesh_bones_count) else 8
        mb = mesh_bones[i] if i < len(mesh_bones) else [fallback_root]*desired_slots
        
        slot_bones = []
        for sidx in range(desired_slots):
            b = mb[sidx] if sidx < len(mb) else None
            if isinstance(b, int) and 0 <= b < bone_count:
                slot_bones.append((b, bone_name[b]))
            else:
                slot_bones.append((None, f"__pad_mesh{i}_slot{sidx}"))

        src_joints = ET.SubElement(skin, "source", id=f"Mesh{i}-joints")
        name_array = ET.SubElement(src_joints, "Name_array", id=f"Mesh{i}-joints-array", count=str(len(slot_bones)))
        name_array.text = " ".join(name for (_, name) in slot_bones)
        tech_j = ET.SubElement(src_joints, "technique_common")
        acc_j = ET.SubElement(tech_j, "accessor", source=f"#Mesh{i}-joints-array", count=str(len(slot_bones)), stride="1")
        ET.SubElement(acc_j, "param", name="JOINT", type="Name")

        bindpose_list = []
        for gb_idx, _ in slot_bones:
            if gb_idx is None: bindpose_list.extend(identity)
            else: bindpose_list.extend(mat_inverse(world_mats.get(gb_idx, identity)))
        
        src_bind = ET.SubElement(skin, "source", id=f"Mesh{i}-bindposes")
        float_array_b = ET.SubElement(src_bind, "float_array", id=f"Mesh{i}-bindposes-array", count=str(len(bindpose_list)))
        float_array_b.text = " ".join(str(round(x, 6)) for x in bindpose_list)
        tech_b = ET.SubElement(src_bind, "technique_common")
        acc_b = ET.SubElement(tech_b, "accessor", source=f"#Mesh{i}-bindposes-array", count=str(len(slot_bones)), stride="16")
        ET.SubElement(acc_b, "param", name="TRANSFORM", type="float4x4")

        weights_flat = []
        vcount_list = []
        vw_pairs = []
        weight_counter = 0

        for vtx in range(v_count):
            weights = mesh_bones_weight[i][vtx] if (i < len(mesh_bones_weight) and vtx < len(mesh_bones_weight[i])) else [0.0]*desired_slots
            mapped_pairs = []
            for local_slot_idx, w in enumerate(weights):
                if w <= 1e-5: continue
                mapped_pairs.append((local_slot_idx, w))
            
            total_w = sum(w for _, w in mapped_pairs)
            if total_w > 0.0: mapped_pairs = [(slot, w/total_w) for slot, w in mapped_pairs]
            else: mapped_pairs = [(0, 1.0)]

            vcount_list.append(len(mapped_pairs))
            for slot_idx, w in mapped_pairs:
                vw_pairs.extend([slot_idx, weight_counter])
                weights_flat.append(w)
                weight_counter += 1

        src_weights = ET.SubElement(skin, "source", id=f"Mesh{i}-weights")
        float_array_w = ET.SubElement(src_weights, "float_array", id=f"Mesh{i}-weights-array", count=str(len(weights_flat)))
        float_array_w.text = " ".join(str(round(w, 6)) for w in weights_flat)
        tech_w = ET.SubElement(src_weights, "technique_common")
        acc_w = ET.SubElement(tech_w, "accessor", source=f"#Mesh{i}-weights-array", count=str(len(weights_flat)), stride="1")
        ET.SubElement(acc_w, "param", name="WEIGHT", type="float")

        joints_block = ET.SubElement(skin, "joints")
        ET.SubElement(joints_block, "input", semantic="JOINT", source=f"#Mesh{i}-joints")
        ET.SubElement(joints_block, "input", semantic="INV_BIND_MATRIX", source=f"#Mesh{i}-bindposes")

        vw_el = ET.SubElement(skin, "vertex_weights", count=str(v_count))
        ET.SubElement(vw_el, "input", semantic="JOINT", source=f"#Mesh{i}-joints", offset="0")
        ET.SubElement(vw_el, "input", semantic="WEIGHT", source=f"#Mesh{i}-weights", offset="1")
        ET.SubElement(vw_el, "vcount").text = " ".join(str(x) for x in vcount_list)
        ET.SubElement(vw_el, "v").text = " ".join(str(x) for x in vw_pairs)

    # =================================================================
    # 6. Library Visual Scenes
    # =================================================================
    lib_scene = ET.SubElement(collada, "library_visual_scenes")
    scene = ET.SubElement(lib_scene, "visual_scene", id="Scene", name="Scene")
    armature_node = ET.SubElement(scene, "node", id="Armature", name="Armature", type="NODE")

    bone_nodes = {}
    for b in range(bone_count):
        node = ET.Element("node", id=bone_name[b], name=bone_name[b], sid=bone_name[b], type="JOINT")
        mat_elem = ET.SubElement(node, "matrix")
        mat_elem.text = make_matrix(
            bone_local_position_x[b], bone_local_position_y[b], bone_local_position_z[b],
            bone_rotation_x[b], bone_rotation_y[b], bone_rotation_z[b]
        )
        bone_nodes[b] = node

    for b in range(bone_count):
        parent = bone_parrent[b]
        if parent >= 0 and parent < bone_count and parent in bone_nodes:
            bone_nodes[parent].append(bone_nodes[b])
        else:
            armature_node.append(bone_nodes[b])

    root_idx = next((i for i, p in enumerate(bone_parrent) if p < 0), 0)
    for i in range(mesh_count):
        mesh_node = ET.SubElement(armature_node, "node", id=f"Object{i}", name=f"Object{i}")
        inst_ctrl = ET.SubElement(mesh_node, "instance_controller", url=f"#Mesh{i}-skin")
        ET.SubElement(inst_ctrl, "skeleton").text = f"#{bone_name[root_idx]}"
        
        if i < len(mesh_material_mappings) and mesh_material_mappings[i]:
            bind_mat = ET.SubElement(inst_ctrl, "bind_material")
            tech_bmat = ET.SubElement(bind_mat, "technique_common")
            for mat_name in mesh_material_mappings[i]:
                # Hubungkan target material ke mapping simbol segitiga di atas
                inst_m = ET.SubElement(tech_bmat, "instance_material", symbol=mat_name, target=f"#{mat_name}")
                # Kaitkan input TEXCOORD "0" (yaitu UVSET0 dari elemen <triangles>) ke target pemetaan material
                ET.SubElement(inst_m, "bind_vertex_input", semantic="UVSET0", input_semantic="TEXCOORD", input_set="0")

    sc = ET.SubElement(collada, "scene")
    ET.SubElement(sc, "instance_visual_scene", url="#Scene")

    tree = ET.ElementTree(collada)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    return True
def parse_dae_geometry(geom, ns):
    """
    Versi ringkas: Hanya membaca Vertices, UVs, dan Faces_raw tanpa Normal DAE.
    """
    vertices = []
    uvs = []
    faces_raw = []
    materials = []

    mesh = geom.find("c:mesh", ns)
    if mesh is None:
        return vertices, uvs, faces_raw, materials

    # 1. Ambil semua source data (Float Arrays)
    sources = {}
    for source in mesh.findall("c:source", ns):
        float_array = source.find("c:float_array", ns)
        if float_array is None:
            continue
        values = list(map(float, float_array.text.strip().split()))
        
        accessor = source.find("c:technique_common/c:accessor", ns)
        if accessor is not None and "stride" in accessor.attrib:
            stride = int(accessor.attrib["stride"])
        else:
            stride = 3
            
        sources[source.attrib["id"]] = (values, stride)

    # 2. Ambil data Posisi Vertex (POSITION)
    for verts in mesh.findall("c:vertices", ns):
        inp_pos = verts.find("c:input[@semantic='POSITION']", ns)
        if inp_pos is not None:
            pos_id = inp_pos.attrib["source"][1:]
            if pos_id in sources:
                values, stride = sources[pos_id]
                for i in range(0, len(values), stride):
                    vertices.append(tuple(values[i:i+stride]))

    # 3. Ambil data UV (TEXCOORD)
    for inp in mesh.findall(".//c:input[@semantic='TEXCOORD']", ns):
        src_id = inp.attrib["source"][1:]
        if src_id in sources:
            values, stride = sources[src_id]
            if not uvs:
                for i in range(0, len(values), stride):
                    uvs.append(tuple(values[i:i+stride]))

    # 4. Ambil data Poligon / Faces
    face_elements = mesh.findall("c:triangles", ns) + mesh.findall("c:polylist", ns)
    
    for tris in face_elements:
        mat = tris.attrib.get("material", "default")
        if mat not in materials:
            materials.append(mat)
        mat_id = materials.index(mat)

        inputs = tris.findall("c:input", ns)
        input_map = {inp.attrib["semantic"]: int(inp.attrib["offset"]) for inp in inputs}
        
        p_elem = tris.find("c:p", ns)
        if p_elem is None or not p_elem.text:
            continue
            
        p = list(map(int, p_elem.text.strip().split()))
        stride = max(input_map.values()) + 1

        for i in range(0, len(p), stride * 3):
            indices = []
            uv_indices = []
            
            for j in range(3):
                base = i + j * stride
                if base + max(input_map.values()) >= len(p):
                    break
                    
                v_idx = p[base + input_map["VERTEX"]]
                indices.append(v_idx)
                
                if "TEXCOORD" in input_map:
                    uv_idx = p[base + input_map["TEXCOORD"]]
                    uv_indices.append((v_idx, uv_idx))
            
            if len(indices) == 3:
                faces_raw.append((mat_id, indices, uv_indices))

    return vertices, uvs, faces_raw, materials
def normalize_dae(vertices, uvs, faces_raw, materials):
    # --- Normalisasi dengan kombinasi unik (v_idx, vt_idx) ---
    vertices_norm = []
    uvs_norm = []
    faces_norm = [[] for _ in materials]

    index_map = {}   # (v_idx, vt_idx) → new_index
    next_index = 0

    for mat_id, indices, uv_indices in faces_raw:
        tri = []
        for v_idx, vt_idx in uv_indices:
            key = (v_idx, vt_idx)
            if key not in index_map:
                index_map[key] = next_index
                next_index += 1
                # simpan vertex
                vertices_norm.append(vertices[v_idx])
                if vt_idx is not None and 0 <= vt_idx < len(uvs):
                    uvs_norm.append(uvs[vt_idx])
                else:
                    uvs_norm.append((0.0, 0.0))
            tri.append(index_map[key])
        faces_norm[mat_id].append(tri)

    return vertices_norm, uvs_norm, faces_norm, index_map
def merge_duplicate_vertices(vertices_norm, uvs_norm, faces_norm, index_map_old):
    merged_vertices = []
    merged_uvs = []
    remap_spatial = {}       # spatial_key -> new_index
    old_to_new = {}          # old_idx -> new_index
    
    new_index = 0

    # 1. Gabungkan vertex & buat mapping dari old_idx ke new_index
    for old_key, old_idx in index_map_old.items():
        v = vertices_norm[old_idx]
        uv = uvs_norm[old_idx]
        
        # Key berdasarkan koordinat & UV
        spatial_key = (
            round(v[0], 6), round(v[1], 6), round(v[2], 6),
            round(uv[0], 6), round(uv[1], 6)
        )
        
        if spatial_key not in remap_spatial:
            remap_spatial[spatial_key] = new_index
            merged_vertices.append(v)
            merged_uvs.append(uv)
            new_index += 1
            
        old_to_new[old_idx] = remap_spatial[spatial_key]

    # 2. Remap faces menggunakan array old_to_new (Jauh lebih cepat & aman)
    for mat_faces in faces_norm:
        for tri in mat_faces:
            for k in range(len(tri)):
                tri[k] = old_to_new[tri[k]]

    # Buat index_map_new (old_key -> new_index) untuk dikembalikan
    index_map_new = {old_key: old_to_new[old_idx] for old_key, old_idx in index_map_old.items()}

    return merged_vertices, merged_uvs, faces_norm, index_map_new
def find_texture_name_for_material(root, mat_name, ns):
    """
    Cari nama file texture untuk material dengan nama mat_name.
    Mengembalikan string nama texture (tanpa path), atau None jika tidak ditemukan.
    """
    # cari elemen material yang cocok
    mat_elem = None
    for m in root.findall(".//c:material", ns):
        # material bisa punya id atau name; cocokkan dengan mat_name
        if m.get("id") == mat_name or m.get("name") == mat_name:
            mat_elem = m
            break
    if mat_elem is None:
        return None

    # ambil effect via instance_effect
    inst_eff = mat_elem.find(".//c:instance_effect", ns)
    if inst_eff is None:
        return None
    eff_url = inst_eff.get("url", "").lstrip("#")
    if not eff_url:
        return None

    # cari effect
    eff_elem = root.find(f".//c:effect[@id='{eff_url}']", ns)
    if eff_elem is None:
        return None

    # cari sampler/texture di profile_COMMON -> technique -> diffuse/texture atau <texture> references
    # 1) cari <texture> di diffuse/lambert/phong
    tex_symbol = None
    tex_node = eff_elem.find(".//c:profile_COMMON//c:technique//c:diffuse//c:texture", ns)
    if tex_node is not None:
        tex_symbol = tex_node.get("texture")

    # 2) jika tidak ada, coba cari <newparam> yang mengandung <sampler2D> lalu ambil source -> newparam surface -> init_from
    if tex_symbol:
        # newparam sampler2D yang punya nama tex_symbol
        sampler = eff_elem.find(f".//c:newparam[@sid='{tex_symbol}']//c:sampler2D//c:source", ns)
        if sampler is not None:
            surface_sid = sampler.text
        else:
            surface_sid = None
    else:
        # coba cari newparam sampler2D pertama
        sampler = eff_elem.find(".//c:newparam//c:sampler2D//c:source", ns)
        surface_sid = sampler.text if sampler is not None else None

    if surface_sid:
        # cari newparam surface dengan sid == surface_sid dan ambil init_from (image id)
        surface = eff_elem.find(f".//c:newparam[@sid='{surface_sid}']//c:surface//c:init_from", ns)
        if surface is not None and surface.text:
            image_id = surface.text
            # cari library_images untuk id ini dan ambil nama file (atau langsung cari image element)
            img = root.find(f".//c:library_images//c:image[@id='{image_id}']//c:init_from", ns)
            if img is not None and img.text:
                # ambil basename (tanpa path)
                return img.text.split("/")[-1].split("\\")[-1]
            # jika image element tidak ada, coba cari image dengan id dan ambil text child
            img_elem = root.find(f".//c:library_images//c:image[@id='{image_id}']", ns)
            if img_elem is not None:
                init = img_elem.find(".//c:init_from", ns)
                if init is not None and init.text:
                    return init.text.split("/")[-1].split("\\")[-1]

    # 3) fallback: coba cari <profile_COMMON>//<technique>//<diffuse>//<texture> attribute 'texture' -> newparam -> surface -> init_from (sudah dicoba),
    # jika semua gagal, return None
    return None
def import_from_dae_mesh(filepath):
    """
    Versi sederhana: hanya tambah mesh + material.
    Bones dan weights diisi dummy (nol / default).
    Mengasumsikan variabel global yang sama seperti di kode asli tersedia.
    """
    global mesh_count, texture_count
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {"c": "http://www.collada.org/2005/11/COLLADASchema"}

    for geom in root.findall(".//c:geometry", ns):
        mesh_count += 1
        i = mesh_count - 1

        # --- Parse geometry (menggunakan fungsi helper Anda) ---
        vertices, uvs, faces_raw, materials = parse_dae_geometry(geom, ns)

        # --- Normalisasi dan indexing (menggunakan helper Anda) ---
        vertices_norm, uvs_norm, faces_norm, index_map = normalize_dae(vertices, uvs, faces_raw, materials)

        # --- (Opsional) merge duplicate vertices jika ada helper ---
        try:
            vertices_norm, uvs_norm, faces_norm, index_map = merge_duplicate_vertices(vertices_norm, uvs_norm, faces_norm, index_map)
        except NameError:
            # Jika merge_duplicate_vertices tidak tersedia, lanjut tanpa merge
            pass

        # --- Setup header/struktur mesh (salin template index 0) ---
        mesh_header.append(copy.deepcopy(mesh_header[0]))
        mesh_bones_header_offset.append(copy.deepcopy(mesh_bones_header_offset[0]))
        mesh_bones_count.append(8)
        mesh_data_header_offset.append(copy.deepcopy(mesh_data_header_offset[0]))
        mesh_data_start_offset.append(copy.deepcopy(mesh_data_start_offset[0]))
        mesh_flag.append(120831)
        read_flag(i)
        mesh_data_lenght.append((mesh_flag_decode[i] + 10) * 4 if mesh_flag_boolean[i] else 36)
        mesh_material_header_offset.append(copy.deepcopy(mesh_material_header_offset[0]))
        mesh_material.append([])
        mesh_material_faces_header_offset.append([])
        mesh_material_faces_start_offset.append([])
        mesh_faces_header.append([])
        mesh_face_count.append([])
        mesh_face_offset.append([])
        mesh_face.append([])
        mesh_data_count.append(len(vertices_norm))
        mesh_data.append([])
        mesh_bones_weight.append([])
        mesh_uv_u.append([])
        mesh_uv_v.append([])
        mesh_vertex_color.append([])
        mesh_normal_x.append([])
        mesh_normal_y.append([])
        mesh_normal_z.append([])
        mesh_vertex_x.append([])
        mesh_vertex_y.append([])
        mesh_vertex_z.append([])

        # --- Isi vertex/UV/color (rotasi/konversi sama seperti kode asli) ---
        for j, (vx, vy, vz) in enumerate(vertices_norm):
            coord_x = vx
            coord_y = vz
            coord_z = -vy
            orig_x, orig_y, orig_z = rotate_3d_x(coord_x, coord_y, coord_z, 90)
            mesh_vertex_x[i].append(orig_x)
            mesh_vertex_y[i].append(orig_y)
            mesh_vertex_z[i].append(orig_z)

            # default normal (dummy)
            mesh_normal_x[i].append(0.0)
            mesh_normal_y[i].append(1.0)
            mesh_normal_z[i].append(0.0)

            # UV (pastikan uvs_norm panjangnya sama dengan vertices_norm)
            if j < len(uvs_norm):
                u, v = uvs_norm[j]
            else:
                u, v = 0.0, 0.0
            mesh_uv_u[i].append(u)
            mesh_uv_v[i].append(v)

            # warna vertex default putih
            mesh_vertex_color[i].append((255, 255, 255, 255))

        # --- Bones & weights: isi dummy (tidak membaca controller sama sekali) ---
        # tambahkan entry bones (8 zeros) agar struktur konsisten
        mesh_bones.append([0] * 8)
        # weights: untuk setiap vertex, buat list 8 float nol
        mesh_bones_weight[i] = [[0.0] * 8 for _ in range(len(vertices_norm))]

        # --- Dummy mesh data per-vertex ---
        for _ in range(len(vertices_norm)):
            mesh_data[i].append(b'\x00' * mesh_data_lenght[i])

        # --- Materials & faces ---
        mesh_material_count.append(len(materials))
        mesh_material_texture.append([])
        mesh_material_faces_count.append([])

        for j, mat_name in enumerate(materials):
            # salin material template index 0
            mesh_material[i].append(copy.deepcopy(mesh_material[0][0]))
            texture_count += 1
            mesh_material_texture[i].append(texture_count - 1)

            # faces untuk material j
            mesh_material_faces_count[i].append(len(faces_norm[j]))
            mesh_material_faces_header_offset[i].append(0)
            mesh_material_faces_start_offset[i].append(0)

            mesh_faces_header[i].append([])
            mesh_face_count[i].append([])
            mesh_face_offset[i].append([])
            mesh_face[i].append([])

            for tri in faces_norm[j]:
                triangle = [int(v) for v in tri]
                mesh_faces_header[i][j].append(copy.deepcopy(mesh_faces_header[0][0][0]))
                mesh_face_count[i][j].append(len(triangle))
                mesh_face_offset[i][j].append(0)
                mesh_face[i][j].append(triangle)
            # ambil nama file texture dari material (tanpa ekstensi)
            tex_name_found = find_texture_name_for_material(root, mat_name, ns)

            if tex_name_found:
                base = os.path.basename(tex_name_found)
                # hapus ekstensi terakhir saja (berdasarkan titik terakhir)
                name_no_ext = os.path.splitext(base)[0]
            else:
                name_no_ext = mat_name

            # bersihkan karakter non-ASCII, hapus null, strip spasi, dan potong ke 16 char
            tex_name = name_no_ext.encode("ascii", errors="ignore").decode("ascii")
            tex_name = tex_name.replace("\x00", "").strip()[:16]

            # pastikan tidak ada ekstensi tersisa (seharusnya tidak perlu, tapi aman)
            if "." in tex_name and tex_name.lower().endswith(tuple(["tga","png","jpg","jpeg","bmp","dds"])):
                tex_name = tex_name.rsplit(".", 1)[0][:16]


            # potong ke 16 karakter maksimal
            tex_name = tex_name[:16]

            texture.append(tex_name)
    return True
def import_from_dae_weight(filepath, verbose=False):
    """
    Simple edit-only COLLADA weight importer.
    - Edits existing mesh_bones[i] and mesh_bones_weight[i] for i in range(mesh_count).
    - Assumes identity mapping DAE-vertex-index -> internal mesh vertex index.
    - Pads/truncates slot list to mesh_bones_count[i] and ensures mesh_bones_weight shape
      equals [mesh_data_count[i]][mesh_bones_count[i]].
    """
    ns = {"c": "http://www.collada.org/2005/11/COLLADASchema"}
    tree = ET.parse(filepath)
    root = tree.getroot()

    controllers = root.findall(".//c:controller", ns)
    if not controllers:
        if verbose:
            print("No controllers found in DAE.")
        return False

    # fallback root index if needed
    try:
        global_roots = [idx for idx, p in enumerate(bone_parrent) if p < 0]
        root_idx = global_roots[0] if global_roots else 0
    except Exception:
        root_idx = 0

    for i in range(mesh_count):
        # preserve old sample for validation (mesh 0 vertex 0)
        old_sample = None
        if i == 0 and mesh_bones_weight and len(mesh_bones_weight) > 0 and len(mesh_bones_weight[0]) > 0:
            old_sample = copy.deepcopy(mesh_bones_weight[0][0])

        # pick controller: prefer id "Mesh{i}-skin", else controllers[i] if exists
        ctrl = None
        expected_id = f"Mesh{i}-skin"
        for c in controllers:
            if (c.get("id") or "") == expected_id:
                ctrl = c
                break
        if ctrl is None:
            if i < len(controllers):
                ctrl = controllers[i]

        if ctrl is None:
            # no controller for this mesh -> keep existing data or fill zeros
            if verbose:
                print(f"Mesh {i}: no controller found, leaving weights unchanged or filling zeros.")
            # ensure arrays exist
            if len(mesh_bones) <= i:
                mesh_bones.append([0] * mesh_bones_count[i])
            if len(mesh_bones_weight) <= i:
                mesh_bones_weight.append([[0.0] * mesh_bones_count[i] for _ in range(mesh_data_count[i])])
            continue

        skin = ctrl.find("c:skin", ns)
        if skin is None:
            if verbose:
                print(f"Mesh {i}: skin element missing, leaving weights unchanged.")
            continue

        # --- Name_array -> slot names ---
        name_array_el = skin.find(".//c:Name_array", ns)
        slot_names = []
        if name_array_el is not None and name_array_el.text:
            slot_names = name_array_el.text.strip().split()

        # map slot names -> global bone indices (fallback 0)
        desired_slots = mesh_bones_count[i]
        slot_map = []
        for nm in slot_names:
            if nm.startswith("__pad_"):
                slot_map.append(0)
            else:
                try:
                    slot_map.append(bone_name.index(nm))
                except ValueError:
                    slot_map.append(0)

        # pad/truncate to desired_slots
        if len(slot_map) < desired_slots:
            slot_map += [0] * (desired_slots - len(slot_map))
        elif len(slot_map) > desired_slots:
            slot_map = slot_map[:desired_slots]

        # overwrite mesh_bones[i]
        if len(mesh_bones) <= i:
            # ensure list exists
            while len(mesh_bones) <= i:
                mesh_bones.append([0] * desired_slots)
        mesh_bones[i] = list(slot_map)

        # --- find weight float array (prefer accessor param WEIGHT) ---
        weight_values = []
        for src in skin.findall("c:source", ns):
            fa = src.find("c:float_array", ns)
            if fa is None or not fa.text:
                continue
            acc = src.find("c:technique_common/c:accessor", ns)
            if acc is not None:
                params = [p.get("name","").upper() for p in acc.findall("c:param", ns)]
                if "WEIGHT" in params:
                    try:
                        weight_values = [float(x) for x in fa.text.strip().split()]
                        break
                    except:
                        continue
        if not weight_values:
            fa = skin.find(".//c:source/c:float_array", ns)
            if fa is not None and fa.text:
                try:
                    weight_values = [float(x) for x in fa.text.strip().split()]
                except:
                    weight_values = []

        # --- read vertex_weights ---
        vw = skin.find("c:vertex_weights", ns)
        if vw is None:
            if verbose:
                print(f"Mesh {i}: no vertex_weights found -> leaving zeros.")
            # ensure mesh_bones_weight shape exists
            if len(mesh_bones_weight) <= i:
                mesh_bones_weight.append([[0.0]*desired_slots for _ in range(mesh_data_count[i])])
            continue

        vcount_el = vw.find("c:vcount", ns)
        v_el = vw.find("c:v", ns)
        if vcount_el is None or v_el is None or not vcount_el.text or not v_el.text:
            if verbose:
                print(f"Mesh {i}: malformed vcount/v -> leaving zeros.")
            if len(mesh_bones_weight) <= i:
                mesh_bones_weight.append([[0.0]*desired_slots for _ in range(mesh_data_count[i])])
            continue

        vcount_list = [int(x) for x in vcount_el.text.strip().split()]
        v_list = [int(x) for x in v_el.text.strip().split()]
        dae_vertex_count = len(vcount_list)

        # validation: DAE vertex count vs internal
        if dae_vertex_count != mesh_data_count[i]:
            if verbose:
                print(f"Mesh {i}: DAE vertex count {dae_vertex_count} != internal mesh_data_count {mesh_data_count[i]}.")
                print("Assuming identity mapping where possible; if you merged/normalized vertices, provide index_map workflow.")
        # prepare internal accumulators
        internal_vertices = mesh_data_count[i]
        accum = [[0.0]*desired_slots for _ in range(internal_vertices)]

        # parse v pairs (identity mapping DAE idx -> internal idx)
        cursor = 0
        for dae_idx, vc in enumerate(vcount_list):
            internal_idx = dae_idx if dae_idx < internal_vertices else None
            for _ in range(vc):
                if cursor + 1 >= len(v_list):
                    break
                joint_local = v_list[cursor]
                weight_idx = v_list[cursor+1]
                cursor += 2
                wval = weight_values[weight_idx] if (0 <= weight_idx < len(weight_values)) else 0.0
                if internal_idx is None:
                    continue
                if 0 <= joint_local < desired_slots:
                    accum[internal_idx][joint_local] += wval

        # normalize and write to mesh_bones_weight (overwrite)
        # ensure mesh_bones_weight list exists and sized
        if len(mesh_bones_weight) <= i:
            mesh_bones_weight.append([[0.0]*desired_slots for _ in range(internal_vertices)])
        else:
            # pad/truncate rows
            if len(mesh_bones_weight[i]) < internal_vertices:
                for _ in range(internal_vertices - len(mesh_bones_weight[i])):
                    mesh_bones_weight[i].append([0.0]*desired_slots)
            elif len(mesh_bones_weight[i]) > internal_vertices:
                mesh_bones_weight[i] = mesh_bones_weight[i][:internal_vertices]
            # ensure each row length
            for vi in range(internal_vertices):
                row = mesh_bones_weight[i][vi]
                if len(row) < desired_slots:
                    mesh_bones_weight[i][vi] = row + [0.0]*(desired_slots - len(row))
                elif len(row) > desired_slots:
                    mesh_bones_weight[i][vi] = row[:desired_slots]

        for vi in range(internal_vertices):
            row = accum[vi]
            total = sum(row)
            if total > 0.0:
                mesh_bones_weight[i][vi] = [float(w/total) for w in row]
            else:
                mesh_bones_weight[i][vi] = [0.0]*desired_slots

        # validation for mesh 0 vertex 0
        if i == 0 and old_sample is not None:
            new_sample = mesh_bones_weight[0][0]
            def approx_equal(a,b,tol=1e-6):
                if len(a) != len(b): return False
                for x,y in zip(a,b):
                    if abs(x-y) > tol:
                        return False
                return True
            same = approx_equal(old_sample, new_sample)
            if verbose:
                print("Validation mesh 0 vertex 0 equal before/after import:", same)
                print(" old:", old_sample)
                print(" new:", new_sample)
            if not same and verbose:
                print("Warning: vertex0 weights changed — Blender/DAE may have reordered vertices or normalized weights differently.")

        if verbose:
            print(f"Mesh {i}: imported slots={desired_slots}, vertices={internal_vertices}")

    return True
def import_from_dae(filepath, verbose=False):
    """
    Mengimpor Mesh DAE dengan DUMMY Vertex Normals (0.0, 1.0, 0.0) 
    dan memetakan data Bone Weight ke dalam struktur global YOBJ.
    Transformasi koordinat dan tekstur menggunakan logika dari import_from_dae_mesh.
    """
    global mesh_count, texture_count, bone_name
    
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {"c": "http://www.collada.org/2005/11/COLLADASchema"}

    # Ambil semua controller (skinning data) dari DAE
    controllers = root.findall(".//c:controller", ns)

    for geom_idx, geom in enumerate(root.findall(".//c:geometry", ns)):
        mesh_count += 1
        i = mesh_count - 1

        # 1. Parse geometry asli dari DAE
        vertices, uvs, faces_raw, materials = parse_dae_geometry(geom, ns)

        # 2. Normalisasi & Gabungkan duplikasi
        vertices_norm, uvs_norm, faces_norm, index_map = normalize_dae(vertices, uvs, faces_raw, materials)
        
        # Tampung hasil merge dengan aman
        try:
            m_verts, m_uvs, m_faces, m_idx_map = merge_duplicate_vertices(
                vertices_norm, uvs_norm, faces_norm, index_map
            )
            if len(m_verts) > 0:
                vertices_norm = m_verts
                uvs_norm = m_uvs
                faces_norm = m_faces
                index_map = m_idx_map
        except Exception as e:
            if verbose:
                print(f"Gagal melakukan merge_duplicate_vertices, gunakan data normalisasi asli. Error: {e}")

        # Proteksi jika data kosong
        internal_vertices_count = len(vertices_norm)
        if internal_vertices_count == 0:
            if verbose:
                print(f"Warning: Geometry {geom.get('id')} tidak menghasilkan vertex data. Skip.")
            mesh_count -= 1
            continue

        # 3. Setup header & alokasi struktur YOBJ
        mesh_header.append(copy.deepcopy(mesh_header[0]))
        mesh_bones_header_offset.append(copy.deepcopy(mesh_bones_header_offset[0]))
        
        desired_slots = 8  # Slot standard WWE YOBJ
        mesh_bones_count.append(desired_slots)
        
        mesh_data_header_offset.append(copy.deepcopy(mesh_data_header_offset[0]))
        mesh_data_start_offset.append(copy.deepcopy(mesh_data_start_offset[0]))
        mesh_flag.append(120831)
        read_flag(i)
        
        mesh_data_lenght.append((mesh_flag_decode[i] + 10) * 4 if mesh_flag_boolean[i] else 36)
        mesh_material_header_offset.append(copy.deepcopy(mesh_material_header_offset[0]))
        
        mesh_material.append([])
        mesh_material_faces_header_offset.append([])
        mesh_material_faces_start_offset.append([])
        mesh_faces_header.append([])
        mesh_face_count.append([])
        mesh_face_offset.append([])
        mesh_face.append([])
        
        mesh_data_count.append(internal_vertices_count)
        mesh_data.append([])
        mesh_uv_u.append([])
        mesh_uv_v.append([])
        mesh_vertex_color.append([])
        mesh_normal_x.append([])
        mesh_normal_y.append([])
        mesh_normal_z.append([])
        mesh_vertex_x.append([])
        mesh_vertex_y.append([])
        mesh_vertex_z.append([])

        # =================================================================
        # 4. ISI DATA TRANSFORMATION GEOMETRI & DUMMY NORMALS (SAMA DENGAN MESH)
        # =================================================================
        for j, (vx, vy, vz) in enumerate(vertices_norm):
            coord_x = vx
            coord_y = vz
            coord_z = -vy
            orig_x, orig_y, orig_z = rotate_3d_x(coord_x, coord_y, coord_z, 90)
            mesh_vertex_x[i].append(orig_x)
            mesh_vertex_y[i].append(orig_y)
            mesh_vertex_z[i].append(orig_z)

            # --- DUMMY NORMAL (Selalu 0.0, 1.0, 0.0) ---
            mesh_normal_x[i].append(0.0)
            mesh_normal_y[i].append(1.0)
            mesh_normal_z[i].append(0.0)

            # UV & Color Mapping
            if j < len(uvs_norm):
                u, v = uvs_norm[j]
            else:
                u, v = 0.0, 0.0
            mesh_uv_u[i].append(u)
            mesh_uv_v[i].append(v)

            mesh_vertex_color[i].append((255, 255, 255, 255))

        for _ in range(internal_vertices_count):
            mesh_data[i].append(b'\x00' * mesh_data_lenght[i])

        # =================================================================
        # 5. PARSE & RE-MAP BONE WEIGHTS SECARA SINKRON
        # =================================================================
        geom_id = geom.get("id") or ""
        ctrl = None
        for c in controllers:
            skin_el = c.find("c:skin", ns)
            if skin_el is not None and skin_el.get("source")[1:] == geom_id:
                ctrl = c
                break
        if ctrl is None and geom_idx < len(controllers):
            ctrl = controllers[geom_idx]

        current_mesh_bones = [0] * desired_slots
        current_mesh_weights = [[0.0] * desired_slots for _ in range(internal_vertices_count)]

        if ctrl is not None:
            skin = ctrl.find("c:skin", ns)
            if skin is not None:
                name_array_el = skin.find(".//c:Name_array", ns)
                slot_names = name_array_el.text.strip().split() if (name_array_el is not None and name_array_el.text) else []

                global_bone_ids = []
                for nm in slot_names:
                    if nm.startswith("__pad_"):
                        global_bone_ids.append(0)
                    else:
                        try:
                            global_bone_ids.append(bone_name.index(nm))
                        except (ValueError, NameError):
                            global_bone_ids.append(0)

                weight_values = []
                for src in skin.findall("c:source", ns):
                    fa = src.find("c:float_array", ns)
                    if fa is None or not fa.text:
                        continue
                    acc = src.find("c:technique_common/c:accessor", ns)
                    if acc is not None:
                        params = [p.get("name", "").upper() for p in acc.findall("c:param", ns)]
                        if "WEIGHT" in params:
                            weight_values = [float(x) for x in fa.text.strip().split()]
                            break
                if not weight_values:
                    fa = skin.find(".//c:source/c:float_array", ns)
                    if fa is not None and fa.text:
                        weight_values = [float(x) for x in fa.text.strip().split()]

                vw = skin.find("c:vertex_weights", ns)
                if vw is not None:
                    vcount_el = vw.find("c:vcount", ns)
                    v_el = vw.find("c:v", ns)
                    
                    if vcount_el is not None and v_el is not None and vcount_el.text and v_el.text:
                        vcount_list = [int(x) for x in vcount_el.text.strip().split()]
                        v_list = [int(x) for x in v_el.text.strip().split()]

                        dae_vertex_count = len(vcount_list)
                        dae_accumulated_weights = [{} for _ in range(dae_vertex_count)]

                        cursor = 0
                        for dae_v_idx, vc in enumerate(vcount_list):
                            for _ in range(vc):
                                if cursor + 1 >= len(v_list):
                                    break
                                joint_local = v_list[cursor]
                                weight_idx = v_list[cursor + 1]
                                cursor += 2
                                
                                wval = weight_values[weight_idx] if 0 <= weight_idx < len(weight_values) else 0.0
                                
                                if 0 <= joint_local < len(global_bone_ids) and wval > 0.0:
                                    g_bone = global_bone_ids[joint_local]
                                    dae_accumulated_weights[dae_v_idx][g_bone] = dae_accumulated_weights[dae_v_idx].get(g_bone, 0.0) + wval

                        mesh_wide_bones = set()
                        for v_dict in dae_accumulated_weights:
                            for g_bone, wval in v_dict.items():
                                if wval > 0.01:
                                    mesh_wide_bones.add(g_bone)
                        
                        mesh_wide_bones = sorted(list(mesh_wide_bones))
                        
                        if len(mesh_wide_bones) > desired_slots:
                            mesh_wide_bones = mesh_wide_bones[:desired_slots]
                        else:
                            mesh_wide_bones += [0] * (desired_slots - len(mesh_wide_bones))
                        
                        current_mesh_bones = mesh_wide_bones

                        for (old_v_idx, old_vt_idx), new_index in index_map.items():
                            if 0 <= old_v_idx < dae_vertex_count and 0 <= new_index < internal_vertices_count:
                                v_dict = dae_accumulated_weights[old_v_idx]
                                for slot_pos, g_bone in enumerate(current_mesh_bones):
                                    if g_bone in v_dict:
                                        current_mesh_weights[new_index][slot_pos] = v_dict[g_bone]

                        for vi in range(internal_vertices_count):
                            row = current_mesh_weights[vi]
                            total = sum(row)
                            if total > 0.0:
                                current_mesh_weights[vi] = [float(w / total) for w in row]
                            else:
                                current_mesh_weights[vi] = [1.0] + [0.0] * (desired_slots - 1)

        mesh_bones.append(current_mesh_bones)
        mesh_bones_weight.append(current_mesh_weights)

        # =================================================================
        # 6. Materials & faces setup (SAMA DENGAN MESH)
        # =================================================================
        mesh_material_count.append(len(materials))
        mesh_material_texture.append([])
        mesh_material_faces_count.append([])

        for j, mat_name in enumerate(materials):
            mesh_material[i].append(copy.deepcopy(mesh_material[0][0]))
            texture_count += 1
            mesh_material_texture[i].append(texture_count - 1)

            mesh_material_faces_count[i].append(len(faces_norm[j]))
            mesh_material_faces_header_offset[i].append(0)
            mesh_material_faces_start_offset[i].append(0)

            mesh_faces_header[i].append([])
            mesh_face_count[i].append([])
            mesh_face_offset[i].append([])
            mesh_face[i].append([])

            for tri in faces_norm[j]:
                triangle = [int(v) for v in tri]
                mesh_faces_header[i][j].append(copy.deepcopy(mesh_faces_header[0][0][0]))
                mesh_face_count[i][j].append(len(triangle))
                mesh_face_offset[i][j].append(0)
                mesh_face[i][j].append(triangle)

            tex_name_found = find_texture_name_for_material(root, mat_name, ns)

            if tex_name_found:
                base = os.path.basename(tex_name_found)
                name_no_ext = os.path.splitext(base)[0]
            else:
                name_no_ext = mat_name

            tex_name = name_no_ext.encode("ascii", errors="ignore").decode("ascii")
            tex_name = tex_name.replace("\x00", "").strip()[:16]

            if "." in tex_name and tex_name.lower().endswith(tuple(["tga","png","jpg","jpeg","bmp","dds"])):
                tex_name = tex_name.rsplit(".", 1)[0][:16]

            tex_name = tex_name[:16]
            texture.append(tex_name)

        if verbose:
            print(f"Mesh {i} Berhasil! Jumlah Vertex (mesh_data_count): {internal_vertices_count}")
            
    return True
def reset_variables():
    global header, all_offset, mesh_count, bone_count, texture_count
    global mesh_header_start_offset, bones_start_offset, texture_offset, model_name_offset, model_count
    global mesh_header, mesh_bones_header_offset, mesh_bones_count, mesh_bones
    global mesh_data_header_offset, mesh_data_start_offset, mesh_data_lenght, mesh_data_count, mesh_data
    global mesh_flag, mesh_flag_boolean, mesh_flag_binary, mesh_flag_decode
    global mesh_bones_weight, mesh_uv_u, mesh_uv_v, mesh_vertex_color
    global mesh_normal_x, mesh_normal_y, mesh_normal_z
    global mesh_vertex_x, mesh_vertex_y, mesh_vertex_z
    global mesh_material_header_offset, mesh_material_count, mesh_material
    global mesh_material_texture, mesh_material_faces_count, mesh_material_faces_header_offset, mesh_material_faces_start_offset
    global mesh_faces_header, mesh_face_count, mesh_face_offset, mesh_face
    global new_mesh_header_start_offset, new_bones_start_offset
    global new_mesh_header_offset, new_mesh_bones_header_offset, new_mesh_data_header_offset
    global new_mesh_data_start_offset, new_mesh_data_count
    global new_mesh_material_header_offset, new_mesh_material_offset, new_mesh_material_count, new_mesh_material
    global new_mesh_material_faces_start_offset, new_mesh_material_faces_header_offset
    global new_mesh_faces_header_offset, new_mesh_face_offset
    global bone, bone_name, bone_local_position_x, bone_local_position_y, bone_local_position_z, bone_local_position_w
    global bone_rotation_x, bone_rotation_y, bone_rotation_z, bone_parrent
    global bone_global_position_x, bone_global_position_y, bone_global_position_z, bone_unknown_float
    global new_bone_offset
    global texture, new_texture_start_offset, new_texture_offset
    global model_name, new_model_name_offset
    global FILE_HEADER

    header = b''
    all_offset = []
    mesh_count = 0
    bone_count = 0
    texture_count = 0
    mesh_header_start_offset = 0
    bones_start_offset = 0
    texture_offset = 0
    model_name_offset = 0
    model_count = 0
    mesh_header = []
    mesh_bones_header_offset = []
    mesh_bones_count = []
    mesh_bones = []
    mesh_data_header_offset = []
    mesh_data_start_offset = []
    mesh_data_lenght = []
    mesh_data_count = []
    mesh_data = []
    mesh_flag = []
    mesh_flag_boolean = []
    mesh_flag_binary = []
    mesh_flag_decode = []
    mesh_bones_weight = []
    mesh_uv_u = []
    mesh_uv_v = []
    mesh_vertex_color = []
    mesh_normal_x = []
    mesh_normal_y = []
    mesh_normal_z = []
    mesh_vertex_x = []
    mesh_vertex_y = []
    mesh_vertex_z = []
    mesh_material_header_offset = []
    mesh_material_count = []
    mesh_material = []
    mesh_material_texture = []
    mesh_material_faces_count = []
    mesh_material_faces_header_offset = []
    mesh_material_faces_start_offset = []
    mesh_faces_header = []
    mesh_face_count = []
    mesh_face_offset = []
    mesh_face = []
    new_mesh_header_start_offset = 0
    new_bones_start_offset = 0
    new_mesh_header_offset = []
    new_mesh_bones_header_offset = []
    new_mesh_data_header_offset = []
    new_mesh_data_start_offset = []
    new_mesh_data_count = []
    new_mesh_material_header_offset = []
    new_mesh_material_offset = []
    new_mesh_material_count = []
    new_mesh_material = []
    new_mesh_material_faces_start_offset = []
    new_mesh_material_faces_header_offset = []
    new_mesh_faces_header_offset = []
    new_mesh_face_offset = []
    bone = []
    bone_name = []
    bone_local_position_x = []
    bone_local_position_y = []
    bone_local_position_z = []
    bone_local_position_w = []
    bone_rotation_x = []
    bone_rotation_y = []
    bone_rotation_z = []
    bone_parrent = []
    bone_global_position_x = []
    bone_global_position_y = []
    bone_global_position_z = []
    bone_unknown_float = []
    new_bone_offset = []
    texture = []
    new_texture_start_offset = 0
    new_texture_offset = []
    model_name = ''
    new_model_name_offset = 0
    FILE_HEADER = 8

    # Kosongkan listbox GUI kalau ada
    try:
        object_listbox.delete(0, tk.END)
    except:
        pass
def browse_file():
    global base_file
    filepath = filedialog.askopenfilename(
        title="Pilih file",
        filetypes=[("YOBJ files", "*.yobj"), ("All files", "*.*")]
    )
    if not filepath:
        return

    file_path_var.set(filepath)

    try:
        base_file = open(filepath, "rb")
        # setelah pilih file, reset variabel lalu baca isi file
        reset_variables()
        read_file(base_file)
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {filepath}")
def read_file(b):
    # f adalah objek file (base_file)
    try:
        # jalankan semua prosedur pembacaan
        read_header(b)
        read_mesh_header(b)
        for i in range(mesh_count):
            read_mesh_header_bones(b, i)
            read_mesh_data_header(b, i)
            read_flag(i)
            read_mesh_data(b, i)
            read_mesh_material(b, i)
            read_mesh_faces_header(b, i)
            read_mesh_faces(b, i)
        read_bones(b)
        read_texture(b)
        read_model_name(b)
        # tampilkan daftar mesh di listbox
        print_mesh_listbox()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file: {e}")
def write_file(t):
    try:
        cleanup_duplicate_textures()
        write_header(t)
        write_mesh_header(t)
        for i in range(mesh_count):
            write_mesh_header_bones(t, i)
            write_mesh_data_header(t, i)
            write_mesh_data(t, i)
            write_mesh_material(t, i)
            write_mesh_faces_header(t, i)
            write_mesh_faces(t, i)
        write_bones(t)
        write_texture(t)
        write_model_name(t)
        generate_pof0(t)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menulis file: {e}")
def print_mesh_listbox():
    # kosongkan listbox dulu
    object_listbox.delete(0, tk.END)

    # isi listbox dengan data mesh
    for i in range(mesh_count):
        line = f"Object {i}, Mesh Data {mesh_data_count[i]}, Material {mesh_material_count[i]}"
        object_listbox.insert(tk.END, line)
def rebuild_yobj():
    global base_file,target_file
    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)


    messagebox.showinfo("Sukses", f"Rebuild File Berhasil.")
def duplicate_selected_object():
    global base_file,target_file

    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]

    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1

    duplicate_mesh(base_file, a)
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)


    messagebox.showinfo("Sukses", f"Object {a} berhasil diduplikasi.")
def remove_selected_object():
    global base_file,target_file

    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]

    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1

    remove_mesh(a)
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)

    messagebox.showinfo("Sukses", f"Object {a} berhasil dihapus.")
def export_object():
    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]  # index mesh yang dipilih
    default_filename = f"Object{a}.obj"

    # buka dialog simpan file dengan nama default
    filepath = filedialog.asksaveasfilename(
        defaultextension=".obj",
        initialfile=default_filename,
        filetypes=[("OBJ files", "*.obj"), ("All files", "*.*")]
    )

    if filepath:
        # turunkan nama .mtl dari path .obj
        mtlpath = os.path.splitext(filepath)[0] + ".mtl"

        # ekspor ke lokasi yang dipilih user
        export_obj(a, filepath, mtlpath)
        export_mtl(a, mtlpath)
        messagebox.showinfo("Sukses", f"Object {a} Exported to OBJ.")
def import_object():
    global base_file, target_file

    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]  # index mesh yang dipilih

    filepath = filedialog.askopenfilename(
        defaultextension=".obj",
        filetypes=[("OBJ files", "*.obj"), ("All files", "*.*")]
    )

    if filepath:
        success = import_obj(a, filepath)

        base_path = base_file.name
        base_name, base_ext = os.path.splitext(base_path)
        target_path = f"{base_name}-new{base_ext}"

        try:
            target_file = open(target_path, "wb")
        except IOError:
            messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
            return 1
        make_new_file(target_file)

        try:
            target_file = open(target_path, "r+b")
        except IOError:
            messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
            return 1

        write_file(target_file)
        target_file.close()
        backup_file(base_file, target_file)

        # tutup base_file lama
        base_file.close()

        # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
        base_file = open(base_path, "rb")

        reset_variables()
        read_file(base_file)

        if success:
            messagebox.showinfo("Sukses", f"Object {a} imported from OBJ.")
        else:
            messagebox.showerror("Error", "Import gagal: jumlah vertex tidak sesuai.")
def export_all_object():
    # ambil nama file YOBJ
    base_path = base_file.name
    base_dir = os.path.dirname(base_path)
    base_name, base_ext = os.path.splitext(os.path.basename(base_path))
    export_dir = os.path.join(base_dir, f"@{base_name}{base_ext}")
    os.makedirs(export_dir, exist_ok=True)


    # loop semua mesh
    for i in range(mesh_count):
        obj_filename = f"Object{i}.obj"
        mtl_filename = f"Object{i}.mtl"
        obj_path = os.path.join(export_dir, obj_filename)
        mtl_path = os.path.join(export_dir, mtl_filename)

        export_obj(i, obj_path, mtl_path)
        export_mtl(i, mtl_path)

    messagebox.showinfo("Sukses", f"Semua Object diekspor ke folder {export_dir}")
def import_all_object():
    global base_file, target_file

    # ambil nama file YOBJ
    base_path = base_file.name
    base_dir = os.path.dirname(base_path)
    base_name, base_ext = os.path.splitext(os.path.basename(base_path))
    import_dir = os.path.join(base_dir, f"@{base_name}{base_ext}")

    if not os.path.isdir(import_dir):
        messagebox.showwarning("Peringatan", f"Folder {import_dir} tidak ditemukan.")
        return

    sukses = 0
    gagal = 0

    # loop semua mesh
    for i in range(mesh_count):
        obj_filename = f"Object{i}.obj"
        obj_path = os.path.join(import_dir, obj_filename)

        if os.path.isfile(obj_path):
            ok = import_obj(i, obj_path)
            if ok:
                sukses += 1
            else:
                gagal += 1
        else:
            gagal += 1

    # setelah import semua OBJ, tulis ulang file YOBJ
    target_path = os.path.join(base_dir, f"{base_name}-new{base_ext}")

    try:
        target_file = open(target_path, "wb")
        make_new_file(target_file)
        target_file.close()

        target_file = open(target_path, "r+b")
        write_file(target_file)
        target_file.close()
        backup_file(base_file, target_file)

        # tutup base_file lama
        base_file.close()

        # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
        base_file = open(base_path, "rb")

        reset_variables()
        read_file(base_file)

        messagebox.showinfo(
            "Import All OBJ",
            f"Import selesai.\nBerhasil: {sukses}\nGagal: {gagal}\nFile baru: {target_path}"
        )
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
def export_object_dat():
    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]  # index mesh yang dipilih
    default_filename = f"Object{a}.dat"

    # buka dialog simpan file dengan nama default
    filepath = filedialog.asksaveasfilename(
        defaultextension=".dat",
        initialfile=default_filename,
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )

    if filepath:
        # ekspor data mesh ke lokasi yang dipilih user
        export_object_data(a, filepath)
        messagebox.showinfo("Sukses", f"Object {a} Data Exported.")
def import_object_dat():
    global base_file, target_file

    # dialog pilih file .dat
    filepath = filedialog.askopenfilename(
        defaultextension=".dat",
        filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
    )

    if not filepath:
        return

    try:
        # panggil prosedur import dat (yang sudah kita buat)
        import_object_data(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Import gagal: {e}")
        return

    # buat target file baru
    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1

    # tulis ulang file dengan object baru di paling bawah
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)

    # mesh_count sudah bertambah otomatis di import_object_data
    messagebox.showinfo("Sukses", f"Object {mesh_count} berhasil diimport dari DAT.")
def import_custom_object():
    global base_file, target_file

    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    source_index = selection[0]  # mesh asal template

    filepath = filedialog.askopenfilename(
        defaultextension=".obj",
        filetypes=[("OBJ files", "*.obj"), ("All files", "*.*")]
    )

    if filepath:
        success = import_custom_obj(filepath, source_index)

        base_path = base_file.name
        base_name, base_ext = os.path.splitext(base_path)
        target_path = f"{base_name}-new{base_ext}"

        try:
            target_file = open(target_path, "wb")
        except IOError:
            messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
            return 1
        make_new_file(target_file)

        try:
            target_file = open(target_path, "r+b")
        except IOError:
            messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
            return 1

        write_file(target_file)
        target_file.close()
        backup_file(base_file, target_file)

        # tutup base_file lama
        base_file.close()

        # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
        base_file = open(base_path, "rb")

        reset_variables()
        read_file(base_file)

        if success:
            messagebox.showinfo("Sukses", f"Object {source_index} imported from OBJ.")
        else:
            messagebox.showerror("Error", "Import gagal: jumlah vertex/UV tidak sesuai.")
def export_dae_GUI():
    selection = object_listbox.curselection()
    if not selection:
        messagebox.showwarning("Peringatan", "Tidak ada object yang dipilih.")
        return

    a = selection[0]  # index mesh yang dipilih
    default_filename = f"Object{a}.dae"

    # buka dialog simpan file dengan nama default
    filepath = filedialog.asksaveasfilename(
        defaultextension=".dae",
        initialfile=default_filename,
        filetypes=[("DAE files", "*.dae"), ("All files", "*.*")]
    )

    if filepath:
        # ekspor ke lokasi yang dipilih user
        export_dae(a, filepath)
        messagebox.showinfo("Sukses", f"Object {a} Exported to DAE.")
import os
from tkinter import filedialog, messagebox

def export_as_one_dae_GUI():
    # ambil nama file input
    base_path = base_file.name
    base_dir = os.path.dirname(base_path)
    base_name, _ = os.path.splitext(os.path.basename(base_path))

    # default nama output .dae
    default_name = base_name + ".dae"

    filepath = filedialog.asksaveasfilename(
        defaultextension=".dae",
        initialfile=default_name,   # ganti dari "AllObjects.dae"
        initialdir=base_dir,        # default folder sama dengan input
        filetypes=[("Collada files", "*.dae"), ("All files", "*.*")]
    )
    if filepath:
        export_as_one_dae(filepath)
        messagebox.showinfo("Sukses", f"Semua Object + Bones diekspor ke {filepath}")
def import_from_dae_mesh_GUI():
    global base_file, target_file

    # dialog pilih file .dae
    filepath = filedialog.askopenfilename(
        defaultextension=".dae",
        filetypes=[("DAE files", "*.dae"), ("All files", "*.*")]
    )

    if not filepath:
        return

    try:
        # panggil prosedur import dae (yang sudah kita buat)
        import_from_dae(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Import gagal: {e}")
        return

    # buat target file baru
    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1

    # tulis ulang file dengan object baru di paling bawah
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)

    # mesh_count sudah bertambah otomatis di import_object_data
    messagebox.showinfo("Sukses", f"Object berhasil diimport dari DAE.")
def import_from_dae_weight_GUI():
    global base_file, target_file

    # dialog pilih file .dae
    filepath = filedialog.askopenfilename(
        defaultextension=".dae",
        filetypes=[("DAE files", "*.dae"), ("All files", "*.*")]
    )

    if not filepath:
        return

    try:
        # panggil prosedur import dae (yang sudah kita buat)
        import_from_dae_weight(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"Import gagal: {e}")
        return

    # buat target file baru
    base_path = base_file.name
    base_name, base_ext = os.path.splitext(base_path)
    target_path = f"{base_name}-new{base_ext}"

    try:
        target_file = open(target_path, "wb")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1
    make_new_file(target_file)

    try:
        target_file = open(target_path, "r+b")
    except IOError:
        messagebox.showerror("Error", f"Tidak bisa membuka {target_path}")
        return 1

    # tulis ulang file dengan object baru di paling bawah
    write_file(target_file)
    target_file.close()
    backup_file(base_file, target_file)

    # tutup base_file lama
    base_file.close()

    # buka ulang base_file ke file hasil rebuild (yang sudah rename jadi .yobj)
    base_file = open(base_path, "rb")

    reset_variables()
    read_file(base_file)

    # mesh_count sudah bertambah otomatis di import_object_data
    messagebox.showinfo("Sukses", f"Weight berhasil diimport dari DAE.")

# --- GUI Setup ---
root = tk.Tk()
root.title("YOBJ Mesh/Object Editor PSP")

file_path_var = tk.StringVar()

# File browse
tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, textvariable=file_path_var, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Object listbox
tk.Label(root, text="Objects:").grid(row=1, column=0, padx=10, pady=10)
object_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=80)
object_listbox.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Baris 1: Duplicate, Remove, Rebuild
row1_frame = tk.Frame(root)
row1_frame.grid(row=2, column=0, columnspan=3, pady=5)

tk.Button(row1_frame, text="Duplicate", command=duplicate_selected_object).pack(side=tk.LEFT, padx=5)
tk.Button(row1_frame, text="Remove", command=remove_selected_object).pack(side=tk.LEFT, padx=5)
tk.Button(row1_frame, text="Rebuild", command=rebuild_yobj).pack(side=tk.LEFT, padx=5)
tk.Button(row1_frame, text="Export .OBJ", command=export_object).pack(side=tk.LEFT, padx=5)
tk.Button(row1_frame, text="Export All .OBJ with .MTL", command=export_all_object).pack(side=tk.LEFT, padx=5)
# Baris 2: Export Selected, Import Selected
row2_frame = tk.Frame(root)
row2_frame.grid(row=3, column=0, columnspan=3, pady=5)
tk.Button(row2_frame, text="Export Object Data", command=export_object_dat).pack(side=tk.LEFT, padx=5)
tk.Button(row2_frame, text="Import Object Data", command=import_object_dat).pack(side=tk.LEFT, padx=5)
tk.Button(row2_frame, text="Import .OBJ", command=import_object).pack(side=tk.LEFT, padx=5)
tk.Button(row2_frame, text="Import All .OBJ", command=import_all_object).pack(side=tk.LEFT, padx=5)
# Baris 3: Export Selected, Import Selected
row3_frame = tk.Frame(root)
row3_frame.grid(row=4, column=0, columnspan=3, pady=5)
tk.Button(row3_frame, text="Export All As One .DAE", command=export_as_one_dae_GUI).pack(side=tk.LEFT, padx=5)
tk.Button(row3_frame, text="Import All from .DAE (Add New)", command=import_from_dae_mesh_GUI).pack(side=tk.LEFT, padx=5)
tk.Button(row3_frame, text="Import All from .DAE (Replace Weight)", command=import_from_dae_weight_GUI).pack(side=tk.LEFT, padx=5)
root.mainloop()