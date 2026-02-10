import struct
import sys
import os
import shutil
import copy
import math
import tkinter as tk
from tkinter import filedialog

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
mesh_header_offset=[]
mesh_header=[]
mesh_bones_header_offset=[]
mesh_bones_count=[]
mesh_bones=[]
mesh_data_header_offset=[]
mesh_data_start_offset=[]
mesh_data_offset=[]
mesh_data_lenght=[]
mesh_data_count=[]
mesh_data=[]
mesh_flag=[]
mesh_flag_boolean=[]
mesh_flag_binary=[]
mesh_flag_decode=[]
mesh_vertex_offset = []
mesh_vertex_x=[]
mesh_vertex_y=[]
mesh_vertex_z=[]
mesh_uv_offset = []
mesh_uv_u=[]
mesh_uv_v=[]
mesh_material_header_offset=[]
mesh_material_offset=[]
mesh_material_count=[]
mesh_material=[]
mesh_material_texture=[]
mesh_material_faces_count=[]
mesh_material_faces_header_offset=[]
mesh_material_faces_start_offset=[]
mesh_faces_header=[]
mesh_faces_header_offset=[]
mesh_face_count=[]
mesh_face_offset=[]
mesh_face=[]
new_bones_start_offset=0
new_mesh_header_offset=[]
new_mesh_bones_header_offset=[]
new_mesh_data_header_offset=[]
new_mesh_data_start_offset=[]
new_mesh_data_offset=[]
new_mesh_data_count=[]
new_mesh_uv_offset=[]
new_mesh_vertex_offset=[]
new_mesh_material_header_offset=[]
new_mesh_material_offset=[]
new_mesh_material_count=[]
new_mesh_material=[]
new_mesh_material_faces_start_offset=[]
new_mesh_material_faces_header_offset=[]
new_mesh_faces_header_offset=[]
new_mesh_face_offset=[]
bone_offset=[]
bone=[]
new_bone_offset=[]
bone_name=[]
bone_parrent=[]
texture=[]
new_texture_start_offset=0
new_texture_offset=[]
model_name=''
new_model_name_offset=0
FILE_HEADER = 8

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
        mesh_header_offset.append(b.tell())
        print(f"Read Mesh Header, Object {i}, Offset {b.tell()}")
        mesh_header.append(b.read(64))
        b.seek(mesh_header_offset[i])
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
#read_procedure
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
    mesh_data_offset.append([])
    mesh_data.append([])
    mesh_uv_offset.append([])
    mesh_uv_u.append([])
    mesh_uv_v.append([])
    mesh_vertex_offset.append([])
    mesh_vertex_x.append([])
    mesh_vertex_y.append([])
    mesh_vertex_z.append([])
    for j in range(mesh_data_count[i]):
        mesh_data_offset[i].append(b.tell())
        mesh_data[i].append(b.read(mesh_data_lenght[i]))
        print(f"Index {j}, Offset {mesh_data_offset[i][j]}")
    for j in range(mesh_data_count[i]):
        b.seek(mesh_data_offset[i][j]) # Read UV
        # Tentukan offset berdasarkan flag
        if mesh_flag_boolean[i]:
            offset = b.tell() + ((mesh_flag_decode[i] + 1) * 4)
        else:
            offset = b.tell()  # UV langsung di Mesh Data Offset
        b.seek(offset)
        mesh_uv_offset[i].append(b.tell())
        # baca U, V (float 4 byte)
        u = struct.unpack('<f', b.read(4))[0]
        v = struct.unpack('<f', b.read(4))[0]
        mesh_uv_u[i].append(u)
        mesh_uv_v[i].append(v)
        print(f"Read UV, Object {i}, Index {j}, U {u}, V {v}")
    for j in range(mesh_data_count[i]):
        b.seek(mesh_data_offset[i][j]) # Read Vertex
        if mesh_flag_boolean[i]:
            offset = (b.tell() + mesh_data_lenght[i]) - 12
        else:
            offset = mesh_data_start_offset[i] + 36
        b.seek(offset)
        mesh_vertex_offset[i].append(b.tell())
        # baca X, Y, Z (float 4 byte)
        x = struct.unpack('<f', b.read(4))[0]
        y = struct.unpack('<f', b.read(4))[0]
        z = struct.unpack('<f', b.read(4))[0]

        mesh_vertex_x[i].append(x)
        mesh_vertex_y[i].append(y)
        mesh_vertex_z[i].append(z)

        print(f"Read Vertex, Object {i}, Index {j}, X {x}, Y {y}, Z {z}")
def read_mesh_material(b,i):
    b.seek(mesh_material_header_offset[i]+8)
    mesh_material.append([])
    mesh_material_offset.append([])
    mesh_material_texture.append([])
    mesh_material_faces_count.append([])
    mesh_material_faces_header_offset.append([])
    mesh_material_faces_start_offset.append([])
    for j in range(mesh_material_count[i]):
        offset=b.tell()
        mesh_material_offset[i].append(offset)
        mesh_material[i].append(b.read(144))
        b.seek(mesh_material_offset[i][j])
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
    mesh_faces_header_offset.append([])
    mesh_faces_header.append([])
    mesh_face_count.append([])
    mesh_face_offset.append([])
    for j in range(mesh_material_count[i]):
        b.seek(mesh_material_faces_header_offset[i][j]+8)
        mesh_faces_header_offset[i].append([])
        mesh_faces_header[i].append([])
        mesh_face_count[i].append([])
        mesh_face_offset[i].append([])
        for k in range(mesh_material_faces_count[i][j]):
            offset=b.tell()
            mesh_faces_header_offset[i][j].append(offset)
            mesh_faces_header[i][j].append(b.read(16))
            print(f"Read Mesh Face Header, Object {i}, Material {j}, Face {k} Offset {offset}")
            b.seek(mesh_faces_header_offset[i][j][k])
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
        bone_offset.append(offset)
        bone.append(b.read(80))
        b.seek(offset)
        bone_name.append(b.read(16).decode("ascii").rstrip("\x00"))
        b.read(32)
        bone_parrent.append(struct.unpack('<I', b.read(4))[0])
        b.read(28)
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
def write_header(t):
    t.seek(0,os.SEEK_END)
    print(f"Write Header at offset {t.tell()}")
    t.write(header)
    pass
def write_mesh_header(t):
    global mesh_count, mesh_header_start_offset, new_mesh_header_offset, mesh_header
    t.seek(0,os.SEEK_END)
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
    t.write(struct.pack('<I',new_mesh_header_offset[0]-8))
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
    new_mesh_data_offset.append([])
    for j in range(mesh_data_count[i]):
        new_mesh_data_offset[i].append(t.tell())
        t.write(mesh_data[i][j])
        print(f"Write New Mesh Data, Object {i}, Offset {new_mesh_data_offset[i][j]}, Lenght {mesh_data_lenght[i]}")
    new_mesh_uv_offset.append([])
    for j in range(mesh_data_count[i]): # write UV
        t.seek(new_mesh_data_offset[i][j])
        if mesh_flag_boolean[i]:
            offset = t.tell() + ((mesh_flag_decode[i] + 1) * 4)
        else:
            offset = t.tell()  # UV langsung di Mesh Data Offset
        t.seek(offset)
        new_mesh_uv_offset[i].append(t.tell())
        # Tulis U, V (float 4 byte)
        t.write(struct.pack('<f',mesh_uv_u[i][j]))
        t.write(struct.pack('<f',mesh_uv_v[i][j]))
        print(f"Write UV, Object {i}, Index {j}, Offset {offset}")
    new_mesh_vertex_offset.append([])
    for j in range(mesh_data_count[i]):
        t.seek(new_mesh_data_offset[i][j]) # write Vertex
        if mesh_flag_boolean[i]:
            offset = (t.tell() + mesh_data_lenght[i]) - 12
        else:
            offset = mesh_data_start_offset[i] + 36
        t.seek(offset)
        new_mesh_vertex_offset[i].append(t.tell())
        # Tulis X, Y, Z (float 4 byte)
        t.write(struct.pack('<f',mesh_vertex_x[i][j]))
        t.write(struct.pack('<f',mesh_vertex_y[i][j]))
        t.write(struct.pack('<f',mesh_vertex_z[i][j]))
        print(f"Write Vertex, Object {i}, Index {j}, Offset {offset}")
    t.seek(new_mesh_bones_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_start_offset[i]-8))
    t.seek(new_mesh_data_header_offset[i])
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_start_offset[i]-8))
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
        t.read(32)
        t.write(struct.pack('<I',bone_parrent[i]))
        t.read(28)
        parent_name = ""
        try:
            parent_idx = bone_parrent[i]
            if 0 <= parent_idx < len(bone_name):
                parent_name = bone_name[parent_idx]
        except Exception:
            parent_name = ""
        print(f"Write Bones, Index {i}, {bone_name[i]}, Parent {bone_parrent[i]}({parent_name})")
        pass
    t.seek(28)
    t.write(struct.pack('<I',bone_count))
    t.seek(40)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_bones_start_offset-8))
    pass
def write_texture(t):
    global texture_count, texture_offset, new_texture_start_offset
    t.seek(0,os.SEEK_END)
    new_texture_start_offset=t.tell()
    for i in range(texture_count):
        t.seek(0,os.SEEK_END)
        new_texture_offset.append(t.tell())
        t.write(texture[i].encode("ascii").ljust(16, b"\x00"))
        print(f"Write Texture, Index {i}, {texture[i]}")
        pass
    t.seek(32)
    t.write(struct.pack('<I',texture_count))
    t.seek(44)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_texture_start_offset-8))
    pass
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
        pass
    new_pof0_end_offset=t.tell()
    new_pof0_lenght=new_pof0_end_offset-new_pof0_start_offset
    print(f"POF0 Lenght {new_pof0_lenght}")
    t.seek(new_pof0_lenght_offset)
    t.write(struct.pack('<I',new_pof0_lenght))
    pass
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
    mesh_header_offset.append(copy.deepcopy(mesh_header_offset[i]))
    mesh_header.append(copy.deepcopy(mesh_header[i]))
    mesh_material_count.append(copy.deepcopy(mesh_material_count[i]))
    mesh_bones_header_offset.append(copy.deepcopy(mesh_bones_header_offset[i]))
    mesh_material_header_offset.append(copy.deepcopy(mesh_material_header_offset[i]))
    mesh_data_header_offset.append(copy.deepcopy(mesh_data_header_offset[i]))
    mesh_flag.append(copy.deepcopy(mesh_flag[i]))
    mesh_data_count.append(copy.deepcopy(mesh_data_count[i]))

    #re-read
    read_mesh_header_bones(b,mesh_count-1)
    read_mesh_data_header(b,mesh_count-1)
    read_flag(mesh_count-1)
    read_mesh_data(b,mesh_count-1)
    read_mesh_material(b,mesh_count-1)
    read_mesh_faces_header(b,mesh_count-1)
    read_mesh_faces(b,mesh_count-1)
    print(f"Mesh {i}, Duplicated.")
def remove_mesh(i):
    global mesh_count

    # mesh count+1
    mesh_count=mesh_count-1

    #mesh
    del mesh_header_offset[i]
    del mesh_header[i]
    del mesh_bones_header_offset[i]
    del mesh_bones_count[i]
    del mesh_bones[i]
    del mesh_data_header_offset[i]
    del mesh_data_start_offset[i]
    del mesh_data_offset[i]
    del mesh_data_lenght[i]
    del mesh_data_count[i]
    del mesh_data[i]
    del mesh_flag[i]
    del mesh_flag_boolean[i]
    del mesh_flag_binary[i]
    del mesh_flag_decode[i]
    del mesh_vertex_offset[i]
    del mesh_vertex_x[i]
    del mesh_vertex_y[i]
    del mesh_vertex_z[i]
    del mesh_uv_offset[i]
    del mesh_uv_u[i]
    del mesh_uv_v[i]
    del mesh_material_header_offset[i]
    del mesh_material_offset[i]
    del mesh_material_count[i]
    del mesh_material[i]
    del mesh_material_texture[i]
    del mesh_material_faces_count[i]
    del mesh_material_faces_header_offset[i]
    del mesh_material_faces_start_offset[i]
    del mesh_faces_header[i]
    del mesh_faces_header_offset[i]
    del mesh_face_count[i]
    del mesh_face_offset[i]
    del mesh_face[i]
    print(f"Mesh {i}, Removed.")
    pass
def export_obj(i):
    lines = []
    lines.append(f"# Exported Object {i}")

    # vertex
    for j in range(mesh_data_count[i]):
        lines.append(f"v {mesh_vertex_x[i][j]} {mesh_vertex_y[i][j]} {mesh_vertex_z[i][j]}")

    # uv
    for j in range(mesh_data_count[i]):
        lines.append(f"vt {mesh_uv_u[i][j]} {mesh_uv_v[i][j]}")

    # faces dengan pola ganjil-genap + usemtl
    for j in range(mesh_material_count[i]):
        # ambil id tekstur dari material
        tex_id = mesh_material_texture[i][j]          # misalnya 2
        tex_name_bytes = texture[tex_id]              # misalnya b'blood\x00\x00...'
        tex_name = tex_name_bytes.decode('utf-8').strip('\x00')
        lines.append(f"usemtl {tex_name}")
        for k in range(mesh_material_faces_count[i][j]):
            face_indices = mesh_face[i][j][k]

            if len(face_indices) < 3:
                continue

            # baris pertama
            lines.append(
                f"f {face_indices[0]+1}/{face_indices[0]+1} "
                f"{face_indices[1]+1}/{face_indices[1]+1} "
                f"{face_indices[2]+1}/{face_indices[2]+1}"
            )

            # baris berikutnya zig-zag
            for n in range(1, len(face_indices) - 2):
                if n % 2 == 1:  # ganjil
                    v1 = face_indices[n]
                    v2 = face_indices[n+2]
                    v3 = face_indices[n+1]
                else:           # genap
                    v1 = face_indices[n]
                    v2 = face_indices[n+1]
                    v3 = face_indices[n+2]

                lines.append(
                    f"f {v1+1}/{v1+1} {v2+1}/{v2+1} {v3+1}/{v3+1}"
                )

    obj_text = "\n".join(lines)
    print(obj_text)
    return obj_text    
def export_mtl(i):
    lines = []
    lines.append(f"# Exported Material for Object {i}")

    # loop semua material di object i
    for j in range(mesh_material_count[i]):
        tex_id = mesh_material_texture[i][j]
        tex_name_bytes = texture[tex_id]
        tex_name = tex_name_bytes.decode('utf-8').strip('\x00')

        # definisi material
        lines.append(f"newmtl {tex_name}")
        lines.append("Ka 1.000 1.000 1.000")   # ambient color
        lines.append("Kd 1.000 1.000 1.000")   # diffuse color
        lines.append("Ks 0.000 0.000 0.000")   # specular color
        lines.append("d 1.0")                  # opacity
        lines.append("illum 2")                # shading model
        lines.append(f"map_Kd {tex_name}.png") # file tekstur (ubah sesuai ekstensi)

    mtl_text = "\n".join(lines)
    print(mtl_text)
    return mtl_text

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} infile outfile")
        return 1

    try:
        base_file = open(sys.argv[1], "rb")
    except IOError:
        print(f"Cannot open {sys.argv[1]}")
        return 1

    #membaca file base_file
    read_header(base_file)
    read_model_name(base_file)
    read_bones(base_file)
    read_texture(base_file)
    read_mesh_header(base_file)
    for i in range(mesh_count):
        read_mesh_header_bones(base_file,i)
        read_mesh_data_header(base_file,i)
        read_flag(i)
        read_mesh_data(base_file,i)
        read_mesh_material(base_file,i)
        read_mesh_faces_header(base_file,i)
        read_mesh_faces(base_file,i)
    read_bones(base_file)
    read_texture(base_file)
    read_model_name(base_file)
    print_mesh()
    a=int(input("Answer: "))
    try:
        target_file = open(sys.argv[2], "wb")
    except IOError:
        print(f"Cannot open {sys.argv[2]}")
        return 1
    make_new_file(target_file)
    try:
        target_file = open(sys.argv[2], "r+b")
    except IOError:
        print(f"Cannot open {sys.argv[2]}")
        return 1
    duplicate_mesh(base_file, a)
    write_header(target_file)
    write_mesh_header(target_file)
    for i in range(mesh_count):
        write_mesh_header_bones(target_file,i)
        write_mesh_data_header(target_file,i)
        write_mesh_data(target_file,i)
        write_mesh_material(target_file,i)
        write_mesh_faces_header(target_file,i)
        write_mesh_faces(target_file,i)
    write_bones(target_file)
    write_texture(target_file)
    write_model_name(target_file)
    generate_pof0(target_file)
    base_file.close()
    target_file.close()

    return 0

if __name__ == "__main__":
    main()
