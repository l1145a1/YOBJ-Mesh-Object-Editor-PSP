import struct
import sys
import os
import shutil
import copy

header = b''
all_offset=[]
mesh_count=0
bone_count=0
texture_count=0
mesh_header_offset=0
bone_offset=0
texture_offset=0
model_name_offset=0
model_count=0
mesh_header=[]
mesh_bones_header_offset=[]
mesh_bones_header=[]
mesh_data_header_offset=[]
mesh_data_offset=[]
mesh_data_count=[]
mesh_data_flag=[]
mesh_data=[]
mesh_flag_boolean=[]
mesh_flag_binary=[]
mesh_flag_decode=[]
mesh_data_lenght=[]
mesh_vertex_offset = []
mesh_vertex_x=[]
mesh_vertex_y=[]
mesh_vertex_z=[]
mesh_uv_offset = []
mesh_uv_x=[]
mesh_uv_y=[]
mesh_material_offset=[]
mesh_material_count=[]
mesh_material=[]
mesh_faces_count=[]
mesh_faces_header_offset=[]
mesh_faces_start_offset=[]
mesh_face_count=[]
mesh_face_offset=[]
mesh_faces_header=[]
mesh_face=[]
new_mesh_header_offset=[]
new_mesh_bones_header_offset=[]
new_mesh_data_header_offset=[]
new_mesh_data_offset=[]
new_mesh_data_count=[]
new_mesh_material_offset=[]
new_mesh_material_count=[]
new_mesh_material=[]
new_mesh_faces_start_offset=[]
new_mesh_faces_header_offset=[]
new_mesh_face_offset=[]
bone=[]
texture=[]
model_name=''
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
    global mesh_count, bone_count, texture_count, mesh_header_offset, bone_offset, texture_offset, model_name_offset, model_count, header
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
    mesh_header_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Mesh Header Offset at offset {b.tell()-4}, Value {mesh_header_offset}")
    bone_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Bone Offset at offset {b.tell()-4}, Value {bone_offset}")
    texture_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Texture Offset at offset {b.tell()-4}, Value {texture_offset}")
    model_name_offset=struct.unpack('<I', b.read(4))[0]
    print(f"Read Model Name Offset at offset {b.tell()-4}, Value {model_name_offset}")
    model_count=struct.unpack('<I', b.read(4))[0]
    print(f"Read Model Count at offset {b.tell()-4}, Value {model_count}")
    pass
def read_mesh_header(b):
    global mesh_count, mesh_header_offset, new_mesh_header_offset, mesh_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        print(f"Read Mesh Header, Object {i}, Offset {b.tell()}")
        mesh_header.append(b.read(64))
        pass
    pass
def read_bones_mesh_offset_header(b):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_bones_header_offset, mesh_bones_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(8)
        mesh_bones_header_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Mesh Bones Header Offset, Object {i}, Value {mesh_bones_header_offset[i]}")
        b.read(52)
        pass
    pass
def read_bones_mesh_header(b):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_bones_header_offset, mesh_bones_header
    for i in range(mesh_count):
        b.seek(mesh_bones_header_offset[i]+8)
        print(f"Read Mesh Bones Header, Object {i}, Lenght 48, Offset {b.tell()}")
        mesh_bones_header.append(b.read(48))
        pass
    pass
def read_mesh_data_header(b):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_data_header_offset, mesh_data_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(24)
        mesh_data_header_offset.append(struct.unpack('<I', b.read(4))[0])
        b.read(36)
        pass
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(40)
        mesh_data_count.append(struct.unpack('<I', b.read(4))[0])
        b.read(20)
        pass
    for i in range(mesh_count):
        print(f"Read Mesh Data Header, Object {i}, Count {mesh_data_count[i]}, Offset {mesh_data_header_offset[i]}")
        pass
    for i in range(mesh_count):
        b.seek(mesh_data_header_offset[i]+8)
        print(f"Read Mesh Data Offset, Object {i}, Offset {b.tell()}")
        mesh_data_offset.append(struct.unpack('<I', b.read(4))[0])
        pass
    pass
def read_data_flag_header(b):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_data_header_offset, mesh_data_header, mesh_data_flag
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(28)
        mesh_data_flag.append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Object {i} Data Flag: {mesh_data_flag[i]}")
        b.read(32)
        pass
    pass
def read_mesh_data(b):
    global mesh_flag_boolean, mesh_flag_binary, mesh_flag_decode, mesh_data_lenght, mesh_data
    for i in range(mesh_count):
        b.seek(mesh_data_offset[i] + 8)
        # Kalkulasi panjang Mesh Data
        mesh_flag_boolean.append(mesh_data_flag[i] & 1536 != 0)
        print(f"Convert Flag to Boolean: {mesh_flag_boolean[i]}")
        mesh_flag_binary.append(format(mesh_data_flag[i], '032b')[::-1])
        print(f"Convert Flag to Binary: {mesh_flag_binary[i]}")
        mesh_flag_decode.append(int(mesh_flag_binary[i][16:13:-1], 2))
        print(f"Decode Flag Binary to Integer: {mesh_flag_decode[i]}")
        if mesh_flag_boolean[i]:
            mesh_data_lenght.append((mesh_flag_decode[i] + 10) * 4)
            mesh_data_lenght_total = mesh_data_lenght[i] * mesh_data_count[i]
        else:
            mesh_data_lenght.append(36)
            mesh_data_lenght_total = 36 * mesh_data_count[i]
        print(f"Data Length Total: {mesh_data_lenght_total}")
        mesh_data.append(b.read(mesh_data_lenght_total))
        print(f"Read Mesh Data, Object {i}, Offset {mesh_data_offset[i]}, Length {mesh_data_lenght[i]}")
def read_mesh_vertex(b,i):
    global mesh_vertex_offset, mesh_vertex_x, mesh_vertex_y, mesh_vertex_z
    b.seek(mesh_data_offset[i] + 8)
    mesh_vertex_offset.append([])
    mesh_vertex_x.append([])
    mesh_vertex_y.append([])
    mesh_vertex_z.append([])
    for j in range(mesh_data_count[i]):
        # Tentukan offset berdasarkan flag
        if mesh_flag_boolean[i]:
            offset = (b.tell() + mesh_data_lenght[i]) - 12
        else:
            offset = mesh_data_offset[i] + 36
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
    pass
def read_mesh_uv(b, i):
    global mesh_uv_offset, mesh_uv_x, mesh_uv_y
    b.seek(mesh_data_offset[i] + 8)
    mesh_uv_offset.append([])
    mesh_uv_x.append([])
    mesh_uv_y.append([])

    for j in range(mesh_data_count[i]):
        flag_start_offset=b.tell()
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

        mesh_uv_x[i].append(u)
        mesh_uv_y[i].append(v)

        print(f"Read UV, Object {i}, Index {j}, U {u}, V {v}")
        if mesh_flag_boolean[i]:
            b.read(mesh_data_lenght[i]-(b.tell()-flag_start_offset))
        else:
            b.read(36-8)
def read_material_header_mesh(b):
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(4)
        mesh_material_count.append(struct.unpack('<I', b.read(4))[0])
        b.read(4)
        mesh_material_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Mesh Material Header, Object {i}, Count {mesh_material_count[i]}, Offset {mesh_material_offset[i]}")
        b.read(48)
        pass
    pass
def read_material_mesh(b):
    for i in range(mesh_count):
        b.seek(mesh_material_offset[i]+8)
        mesh_material.append([])
        for j in range(mesh_material_count[i]):
            offset=b.tell()
            mesh_material[i].append(b.read(144))
            print(f"Read Mesh Material, Object {i}, Material {j}, offset {offset}")
            pass
        pass
    pass
def read_mesh_faces(b,i):
    b.seek(mesh_material_offset[i]+8)
    mesh_faces_count.append([])
    mesh_faces_header_offset.append([])
    mesh_faces_start_offset.append([])
    for j in range(mesh_material_count[i]):
        b.read(132)
        mesh_faces_count[i].append(struct.unpack('<I', b.read(4))[0])
        mesh_faces_header_offset[i].append(struct.unpack('<I', b.read(4))[0])
        mesh_faces_start_offset[i].append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Mesh Faces Header, Object {i}, Material {j}, Count {mesh_faces_count[i][j]}, Offset {mesh_faces_header_offset[i][j]}")
        pass
    for j in range(mesh_material_count[i]):
        mesh_face_count.append([])
        mesh_face_offset.append([])
        mesh_faces_header.append([])
        mesh_face.append([])
        mesh_face_count[i].append([])
        mesh_face_offset[i].append([])
        mesh_faces_header[i].append([])
        mesh_face[i].append([])
        b.seek(mesh_faces_header_offset[i][j]+8)
        for k in range(mesh_faces_count[i][j]):
            print(f"Read Mesh Face Header, Object {i}, Material {j}, Face {k} Offset {b.tell()}")
            mesh_faces_header[i][j].append(b.read(16))
            pass
        b.seek(mesh_faces_header_offset[i][j]+8)
        for k in range(mesh_faces_count[i][j]):
            b.read(8)
            mesh_face_count[i][j].append(struct.unpack('<I', b.read(4))[0])
            mesh_face_offset[i][j].append(struct.unpack('<I', b.read(4))[0])
            pass
        for k in range(mesh_faces_count[i][j]):
            b.seek(mesh_face_offset[i][j][k] + 8)
            mesh_face[i][j].append([])  # siapkan list untuk face ke-k
            for l in range(mesh_face_count[i][j][k]):  # jumlah elemen dalam face
                val = struct.unpack('<H', b.read(2))[0]  # baca 2 byte
                mesh_face[i][j][k].append(val)
            print(f"Read Face, Object {i}, Material {j}, Faces {k}, "
                f"Offset {mesh_face_offset[i][j][k]}, "
                f"Values {mesh_face[i][j][k]}")
            pass
        pass
    pass
def read_bones(b):
    global bone_count, bone_offset
    b.seek(bone_offset+8)
    print(f"Read {bone_count} Bones at offset {b.tell()}")
    for i in range(bone_count):
        bone.append(b.read(80))
        pass
        pass
def read_texture(b):
    global texture_count, texture_offset
    b.seek(texture_offset+8)
    print(f"Read {texture_count} Texture at offset {b.tell()}")
    for i in range(texture_count):
        texture.append(b.read(16))
        pass
        pass
def read_model_name(b):
    global model_name_offset
    b.seek(model_name_offset+8)
    print(f"Read Model Name at offset {b.tell()}")
    model_name=b.read(16).decode('ascii')
    pass
def write_header(t):
    t.seek(0,os.SEEK_END)
    print(f"Write Header at offset {t.tell()}")
    t.write(header)
    pass
def write_mesh_header(t):
    global mesh_count, mesh_header_offset, new_mesh_header_offset, mesh_header
    t.seek(0,os.SEEK_END)
    for i in range(mesh_count):
        print(f"Write Mesh Header, Object {i}, Offset {t.tell()}")
        new_mesh_header_offset.append(t.tell())
        t.write(mesh_header[i])
        pass
    t.seek(24)
    t.write(struct.pack('<I',mesh_count))
    t.seek(36)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_header_offset[0]-8))
    print(f"Write New Mesh Header Offset at offset 36, Value {new_mesh_header_offset[0]-8}")
    pass
def write_bones_mesh_header(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_bones_header_offset.append(t.tell())
    t.write(mesh_bones_header[i])
    t.seek(new_mesh_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_bones_header_offset[i]-8))
    print(f"Write New Mesh Bones Header, Object {i}, Offset {new_mesh_bones_header_offset[i]}, Lenght 48")
    pass
def write_mesh_data(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_data_header_offset.append(t.tell())
    t.write(b'\x00' * 4)
    t.write(b'\x00' * 12)
    new_mesh_data_offset.append(t.tell())
    t.write(mesh_data[i])
    padding(t)
    t.seek(new_mesh_data_header_offset[i])
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_offset[i]-8))
    t.seek(new_mesh_bones_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_offset[i]-8))
    t.seek(new_mesh_header_offset[i])
    t.read(24)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_data_header_offset[i]-8))
    print(f"Write New Mesh Data Header, Object {i}, Offset {new_mesh_data_offset[i]}, Lenght {len(mesh_data[i])}")
    pass

def write_mesh_vertex(t, i):
    t.seek(new_mesh_data_offset[i])
    print(f"Seek to offset {t.tell()} for Object {i}")
    # tulis ulang vertex
    for j in range(mesh_data_count[i]):
        # skip header sesuai flag
        if mesh_flag_boolean[i]:
            t.read(mesh_data_lenght[i] - 12)
        else:
            t.read(36)
        t.write(struct.pack('<f', mesh_vertex_x[i][j]))
        t.write(struct.pack('<f', mesh_vertex_y[i][j]))
        t.write(struct.pack('<f', mesh_vertex_z[i][j]))
        print(f"Write Vertex, Object {i}, Index {j}, "
              f"X {mesh_vertex_x[i][j]}, Y {mesh_vertex_y[i][j]}, Z {mesh_vertex_z[i][j]}, "
              f"Offset {t.tell() - 12}")

def write_mesh_uv(t, i):
    t.seek(new_mesh_data_offset[i])
    print(f"Seek to offset {t.tell()} for Object {i}")

    for j in range(mesh_data_count[i]):
        flag_start_offset = t.tell()

        # kalau ada flag, lompat sesuai decode
        if mesh_flag_boolean[i]:
            t.seek(t.tell() + ((mesh_flag_decode[i] + 1) * 4))
        # kalau tidak ada flag, langsung di posisi sekarang

        # tulis ulang U,V
        t.write(struct.pack('<f', mesh_uv_x[i][j]))
        t.write(struct.pack('<f', mesh_uv_y[i][j]))

        print(f"Write UV, Object {i}, Index {j}, "
              f"U {mesh_uv_x[i][j]}, V {mesh_uv_y[i][j]}, "
              f"Offset {t.tell() - 8}")

        # skip sisa blok, jangan diubah
        if mesh_flag_boolean[i]:
            t.read(mesh_data_lenght[i] - (t.tell() - flag_start_offset))
        else:
            t.read(36 - 8)

def write_material_mesh(t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_material_offset.append(t.tell())
    for j in range(mesh_material_count[i]):
        t.write(mesh_material[i][j])
        pass
    t.seek(new_mesh_header_offset[i])
    t.read(12)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_material_offset[i]-8))
    print(f"Write New Mesh Material, Object {i}, Offset {new_mesh_material_offset[i]}, Lenght {len(mesh_material[i])}")
    pass
def write_mesh_faces(t,i):
    new_mesh_faces_start_offset.append([])
    new_mesh_faces_header_offset.append([])
    for j in range(mesh_material_count[i]):
        new_mesh_face_offset.append([])
        new_mesh_face_offset[i].append([])
        t.seek(0,os.SEEK_END)
        new_mesh_faces_header_offset[i].append(t.tell())
        for k in range(mesh_faces_count[i][j]):
            print(f"Write Mesh Faces Header, Object {i}, Material {j} Offset {t.tell()}")
            t.write(mesh_faces_header[i][j][k])
            pass
        new_mesh_faces_start_offset[i].append(t.tell())
        for k in range(mesh_faces_count[i][j]):
            new_mesh_face_offset[i][j].append(t.tell())
            # tulis tiap elemen face (2 byte)
            for l in mesh_face[i][j][k]:
                t.write(struct.pack('<H', l))
            padding(t)
            pass
        pass
        t.seek(new_mesh_faces_header_offset[i][j])
        for k in range(mesh_faces_count[i][j]):
            t.read(12)
            all_offset.append(t.tell())
            t.write(struct.pack('<I',new_mesh_face_offset[i][j][k]-8))
            pass
        pass
    t.seek(new_mesh_material_offset[i])
    for j in range(mesh_material_count[i]):
        t.read(136)
        all_offset.append(t.tell())
        t.write(struct.pack('<I',new_mesh_faces_header_offset[i][j]-8))
        all_offset.append(t.tell())
        t.write(struct.pack('<I',new_mesh_faces_start_offset[i][j]-8))
        pass
        pass
def write_bones(t):
    global bone_count, bone_offset
    t.seek(0,os.SEEK_END)
    new_bone_offset=t.tell()
    print(f"Write {bone_count} Bones at offset {t.tell()}")
    for i in range(bone_count):
        t.write(bone[i])
        pass
    t.seek(28)
    t.write(struct.pack('<I',bone_count))
    t.seek(40)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_bone_offset-8))
    pass
def write_texture(t):
    global texture_count, texture_offset
    t.seek(0,os.SEEK_END)
    new_texture_offset=t.tell()
    print(f"Write {texture_count} Texture at offset {t.tell()}")
    for i in range(texture_count):
        t.write(texture[i])
        pass
    t.seek(32)
    t.write(struct.pack('<I',texture_count))
    t.seek(44)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_texture_offset-8))
    pass
def write_model_name(t):
    global model_name_offset
    t.seek(0,os.SEEK_END)
    new_model_name_offset=t.tell()
    print(f"Write Model Name at offset {t.tell()}")
    t.write(model_name.encode('ascii'))
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
    return count
def generate_pof0(t):
    t.seek(0,os.SEEK_END)
    new_pof0_offset=t.tell()
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
    t.seek(new_pof0_lenght_offset)
    t.write(struct.pack('<I',new_pof0_lenght))
    t.seek(4)
    t.write(struct.pack('<I',new_pof0_offset-8))
    t.seek(12)
    t.write(struct.pack('<I',new_pof0_offset-8))
    pass
def print_mesh():
    print(f"Mesh List: ")
    for i in range(mesh_count):
        print(f"Object {i}, Data {mesh_data_count[i]}, Material {mesh_material_count[i]}")
        pass
    pass
def duplicate_mesh(b,i):
    global mesh_count
    # mesh count+1
    mesh_count=mesh_count+1

    #mesh_header
    mesh_header.append(copy.deepcopy(mesh_header[i]))

    #mesh_bones_header
    mesh_bones_header_offset.append(mesh_bones_header_offset[i])
    mesh_bones_header.append(mesh_bones_header[i])

    #mesh_data
    mesh_data_header_offset.append(mesh_data_header_offset[i])
    mesh_data_count.append(mesh_data_count[i])
    mesh_data_offset.append(mesh_data_offset[i])
    mesh_data.append(mesh_data[i])

    #mesh_material
    mesh_material_count.append(mesh_material_count[i])
    mesh_material_offset.append(mesh_material_offset[i])
    mesh_material.append(mesh_material[i])

    read_faces_mesh(b,mesh_count-1)
    pass
def remove_mesh(i):
    global mesh_count

    # mesh count+1
    mesh_count=mesh_count-1

    #mesh_header
    del mesh_header[i]

    #mesh_bones_header
    del mesh_bones_header_offset[i]
    del mesh_bones_header[i]

    #mesh_data
    del mesh_data_header_offset[i]
    del mesh_data_count[i]
    del mesh_data_offset[i]
    del mesh_data[i]

    #mesh_material
    del mesh_material_count[i]
    del mesh_material_offset[i]
    del mesh_material[i]

    #mesh_faces
    del mesh_faces_count[i]
    del mesh_faces_header_offset[i]
    del mesh_faces_start_offset[i]

    #mesh_face
    del mesh_face_count[i]
    del mesh_face_offset[i]
    del mesh_faces_header[i]
    del mesh_face[i]
    pass

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
    read_bones_mesh_offset_header(base_file)
    read_bones_mesh_header(base_file)
    read_mesh_data_header(base_file)
    read_data_flag_header(base_file)
    read_mesh_data(base_file)
    read_material_header_mesh(base_file)
    read_material_mesh(base_file)
    for i in range(mesh_count):
        read_mesh_vertex(base_file,i)
        read_mesh_uv(base_file,i)
        read_mesh_faces(base_file,i)
        pass
    print_mesh()
    
    #menjalankan perintah spesifik
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
    #contoh perintah spesifik
    #duplicate_mesh(base_file,a)

    #menulis perubahan ke target_file
    write_header(target_file)
    write_mesh_header(target_file)
    for i in range(mesh_count):
        write_bones_mesh_header(target_file,i)
        write_mesh_data(target_file,i)
        write_material_mesh(target_file,i)
        write_mesh_faces(target_file,i)
        write_mesh_vertex(target_file,i)
        write_mesh_uv(target_file,i)
    write_bones(target_file)
    write_texture(target_file)
    write_model_name(target_file)
    generate_pof0(target_file)
    base_file.close()
    target_file.close()

    return 0

if __name__ == "__main__":
    main()
