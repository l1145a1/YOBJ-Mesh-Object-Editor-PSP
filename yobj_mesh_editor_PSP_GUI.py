import struct
import sys
import os
import shutil
import copy
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
# Deklarasi variabel global
base_file = None
target_file = None
header = None
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
mesh_vertice_header_offset=[]
mesh_vertice_offset=[]
mesh_vertice_count=[]
mesh_vertice=[]
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
new_mesh_vertice_header_offset=[]
new_mesh_vertice_offset=[]
new_mesh_vertice_count=[]
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
def reset_variables():
    global base_file, target_file  # Deklarasi ulang variabel global
    global all_offset, mesh_count, bone_count, texture_count, mesh_header_offset, header
    global bone_offset, texture_offset, model_name_offset, model_count
    global mesh_header, mesh_bones_header_offset, mesh_bones_header
    global mesh_vertice_header_offset, mesh_vertice_offset, mesh_vertice_count, mesh_vertice
    global mesh_material_offset, mesh_material_count, mesh_material
    global mesh_faces_count, mesh_faces_header_offset, mesh_faces_start_offset
    global mesh_face_count, mesh_face_offset, mesh_faces_header, mesh_face
    global new_mesh_header_offset, new_mesh_bones_header_offset
    global new_mesh_vertice_header_offset, new_mesh_vertice_offset, new_mesh_vertice_count
    global new_mesh_material_offset, new_mesh_material_count, new_mesh_material
    global new_mesh_faces_start_offset, new_mesh_faces_header_offset, new_mesh_face_offset
    global bone, texture, model_name

    base_file = None
    target_file = None
    header = None
    all_offset = []
    mesh_count = 0
    bone_count = 0
    texture_count = 0
    mesh_header_offset = 0
    bone_offset = 0
    texture_offset = 0
    model_name_offset = 0
    model_count = 0
    mesh_header = []
    mesh_bones_header_offset = []
    mesh_bones_header = []
    mesh_vertice_header_offset = []
    mesh_vertice_offset = []
    mesh_vertice_count = []
    mesh_vertice = []
    mesh_material_offset = []
    mesh_material_count = []
    mesh_material = []
    mesh_faces_count = []
    mesh_faces_header_offset = []
    mesh_faces_start_offset = []
    mesh_face_count = []
    mesh_face_offset = []
    mesh_faces_header = []
    mesh_face = []
    new_mesh_header_offset = []
    new_mesh_bones_header_offset = []
    new_mesh_vertice_header_offset = []
    new_mesh_vertice_offset = []
    new_mesh_vertice_count = []
    new_mesh_material_offset = []
    new_mesh_material_count = []
    new_mesh_material = []
    new_mesh_faces_start_offset = []
    new_mesh_faces_header_offset = []
    new_mesh_face_offset = []
    bone = []
    texture = []
    model_name = ''
    FILE_HEADER = 8

def backup_file(file_path):
    # Cek apakah file_path valid
    if not os.path.isfile(file_path):
        print(f"File {file_path} tidak ditemukan.")
        return

    # Membuat nama file backup
    backup_path = file_path + ".bak"

    try:
        # Salin isi file ke backup
        with open(file_path, "rb") as original_file:
            with open(backup_path, "wb") as backup_file:
                backup_file.write(original_file.read())
        print(f"Backup berhasil: {backup_path}")
    except IOError as e:
        print(f"Gagal membuat backup: {e}")
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
def read_header(b,t):
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
def read_mesh_header(b,t):
    global mesh_count, mesh_header_offset, new_mesh_header_offset, mesh_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        print(f"Read Mesh Header, Object {i}, Offset {b.tell()}")
        mesh_header.append(b.read(64))
        pass
    pass
def read_bones_mesh_offset_header(b,t):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_bones_header_offset, mesh_bones_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(8)
        mesh_bones_header_offset.append(struct.unpack('<I', b.read(4))[0])
        print(f"Read Mesh Bones Header Offset, Object {i}, Value {mesh_bones_header_offset[i]}")
        b.read(52)
        pass
    pass
def read_bones_mesh_header(b,t):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_bones_header_offset, mesh_bones_header
    for i in range(mesh_count):
        b.seek(mesh_bones_header_offset[i]+8)
        print(f"Read Mesh Bones Header, Object {i}, Lenght 48, Offset {b.tell()}")
        mesh_bones_header.append(b.read(48))
        pass
    pass
def read_vertice_mesh_header(b,t):
    global mesh_count, mesh_header_offset, mesh_bones_header, mesh_vertice_header_offset, mesh_vertice_header
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(24)
        mesh_vertice_header_offset.append(struct.unpack('<I', b.read(4))[0])
        b.read(36)
        pass
    b.seek(mesh_header_offset+8)
    for i in range(mesh_count):
        b.read(40)
        mesh_vertice_count.append(struct.unpack('<I', b.read(4))[0])
        b.read(20)
        pass
    for i in range(mesh_count):
        print(f"Read Mesh Vertice Header, Object {i}, Count {mesh_vertice_count[i]}, Offset {mesh_vertice_header_offset[i]}")
        pass
    for i in range(mesh_count):
        b.seek(mesh_vertice_header_offset[i]+8)
        print(f"Read Mesh Vertice Offset, Object {i}, Offset {b.tell()}")
        mesh_vertice_offset.append(struct.unpack('<I', b.read(4))[0])
        pass
    pass
def read_vertice_mesh(b,t):
    for i in range(mesh_count):
        b.seek(mesh_vertice_offset[i]+8)
        offset=b.tell()
        vertice_lenght=mesh_vertice_count[i]*68
        mesh_vertice.append(b.read(vertice_lenght))
        print(f"Read Mesh Vertice, Object {i}, Offset {offset}, Lenght {vertice_lenght}")
        pass
    pass
def read_material_header_mesh(b,t):
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
def read_material_mesh(b,t):
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
def read_faces_mesh(b,t,i):
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
            b.seek(mesh_face_offset[i][j][k]+8)
            lenght=mesh_face_count[i][j][k]*2
            mesh_face[i][j].append(b.read(lenght))
            print(f"Read Face, Object {i}, Material {j}, Face {k}, Count {mesh_face_count[i][j][k]}, Offset {mesh_face_offset[i][j][k]}")
            pass
        pass
    pass
def read_bones(b,t):
    global bone_count, bone_offset
    b.seek(bone_offset+8)
    print(f"Read {bone_count} Bones at offset {b.tell()}")
    for i in range(bone_count):
        bone.append(b.read(80))
        pass
        pass
def read_texture(b,t):
    global texture_count, texture_offset
    b.seek(texture_offset+8)
    print(f"Read {texture_count} Texture at offset {b.tell()}")
    for i in range(texture_count):
        texture.append(b.read(16))
        pass
        pass
def read_model_name(b,t):
    global model_name_offset
    b.seek(model_name_offset+8)
    print(f"Read Model Name at offset {b.tell()}")
    model_name=b.read(16).decode('ascii')
    pass
def write_header(b,t):
    t.seek(0,os.SEEK_END)
    print(f"Write Header at offset {t.tell()}")
    t.write(header)
    pass
def write_mesh_header(b,t):
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
def write_bones_mesh_header(b,t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_bones_header_offset.append(t.tell())
    t.write(mesh_bones_header[i])
    t.seek(new_mesh_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_bones_header_offset[i]-8))
    print(f"Write New Mesh Bones Header, Object {i}, Offset {new_mesh_bones_header_offset[i]}, Lenght 48")
    pass
def write_vertice_mesh(b,t,i):
    t.seek(0,os.SEEK_END)
    new_mesh_vertice_header_offset.append(t.tell())
    t.write(b'\x00' * 4)
    t.write(b'\x00' * 12)
    new_mesh_vertice_offset.append(t.tell())
    t.write(mesh_vertice[i])
    padding(t)
    t.seek(new_mesh_vertice_header_offset[i])
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_vertice_offset[i]-8))
    t.seek(new_mesh_bones_header_offset[i])
    t.read(8)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_vertice_offset[i]-8))
    t.seek(new_mesh_header_offset[i])
    t.read(24)
    all_offset.append(t.tell())
    t.write(struct.pack('<I',new_mesh_vertice_header_offset[i]-8))
    print(f"Write New Mesh Vertice Header, Object {i}, Offset {new_mesh_vertice_offset[i]}, Lenght {len(mesh_vertice[i])}")
    pass
def write_material_mesh(b,t,i):
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
def write_faces_mesh(b,t,i):
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
            t.write(mesh_face[i][j][k])
            padding(t)
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
def write_bones(b,t):
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
def write_texture(b,t):
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
def write_model_name(b,t):
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
        print(f"Object {i}, Vertice {mesh_vertice_count[i]}, Material {mesh_material_count[i]}")
        pass
    pass
def duplicate_mesh(b,t,i):
    global mesh_count
    # mesh count+1
    mesh_count=mesh_count+1

    #mesh_header
    mesh_header.append(copy.deepcopy(mesh_header[i]))

    #mesh_bones_header
    mesh_bones_header_offset.append(mesh_bones_header_offset[i])
    mesh_bones_header.append(mesh_bones_header[i])

    #mesh_vertice
    mesh_vertice_header_offset.append(mesh_vertice_header_offset[i])
    mesh_vertice_count.append(mesh_vertice_count[i])
    mesh_vertice_offset.append(mesh_vertice_offset[i])
    mesh_vertice.append(mesh_vertice[i])

    #mesh_material
    mesh_material_count.append(mesh_material_count[i])
    mesh_material_offset.append(mesh_material_offset[i])
    mesh_material.append(mesh_material[i])

    read_faces_mesh(b,t,mesh_count-1)
    pass
def remove_mesh(b,t,i):
    global mesh_count

    # mesh count+1
    mesh_count=mesh_count-1

    #mesh_header
    del mesh_header[i]

    #mesh_bones_header
    del mesh_bones_header_offset[i]
    del mesh_bones_header[i]

    #mesh_vertice
    del mesh_vertice_header_offset[i]
    del mesh_vertice_count[i]
    del mesh_vertice_offset[i]
    del mesh_vertice[i]

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
def browse_file():
    global base_file, target_file  # Menggunakan variabel global
    # File dialog untuk memilih file input
    infile_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("YOBJ Files", "*.yobj")])
    if not infile_path:
        print("File selection canceled")
        return

    # Kosongkan listbox dan reset variabel
    object_listbox.delete(0, tk.END)
    reset_variables()
    # Backup file input
    backup_file(infile_path)
    file_path_var.set(infile_path)  # Menyimpan path input di GUI

    print(f"File imported: {infile_path}")
    print("Ready to read the file!")
    read_file()
def read_file():
    global base_file, target_file  # Menggunakan variabel global

    # Ambil path file dari GUI
    infile_path = file_path_var.get()
    if not infile_path:
        print("No file imported!")
        return

    # Path output (0002-NEW.yobj)
    infile_name = os.path.basename(infile_path)  # Nama file input
    outfile_name = os.path.splitext(infile_name)[0] + "-NEW.yobj"  # Nama file output
    outfile_path = os.path.join(os.path.dirname(infile_path), outfile_name)

    try:
        base_file = open(infile_path, "rb")  # Membuka file input
    except IOError:
        print(f"Cannot open {infile_path}")
        return

    try:
        target_file = open(outfile_path, "wb")  # Membuka file output
    except IOError:
        print(f"Cannot open {outfile_path}")
        return

    make_new_file(target_file)

    try:
        target_file = open(outfile_path, "r+b")  # Membuka ulang file output untuk mode read/write
    except IOError:
        print(f"Cannot open {outfile_path}")
        return

    # Menjalankan prosedur pembacaan seperti di CLI
    read_header(base_file, target_file)
    read_model_name(base_file, target_file)
    read_bones(base_file, target_file)
    read_texture(base_file, target_file)
    read_mesh_header(base_file, target_file)
    read_bones_mesh_offset_header(base_file, target_file)
    read_bones_mesh_header(base_file, target_file)
    read_vertice_mesh_header(base_file, target_file)
    read_vertice_mesh(base_file, target_file)
    read_material_header_mesh(base_file, target_file)
    read_material_mesh(base_file, target_file)
    for i in range(mesh_count):
        read_faces_mesh(base_file, target_file, i)

    # Tampilkan objek di listbox
    print_mesh_to_listbox()

    print(f"File {infile_path} has been read successfully.")

def print_mesh_to_listbox():
    # Mengisi daftar objek ke listbox GUI
    object_listbox.delete(0, tk.END)  # Membersihkan listbox
    for i in range(mesh_count):
        obj_info = f"Object {i}, Vertice {mesh_vertice_count[i]}, Material {mesh_material_count[i]}"
        object_listbox.insert(tk.END, obj_info)

def duplicate_selected_object():
    global base_file, target_file  # Menggunakan variabel global

    selected_index = object_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error","No object selected!")
        return

    selected_object = selected_index[0]
    print(f"Selected Object: {selected_object}")

    try:
        duplicate_mesh(base_file, target_file, selected_object)  # Memanggil prosedur duplicate_mesh
    except Exception as e:
        print(f"Error duplicating object: {e}")
        messagebox.showerror("Error","Error duplicating object")
        return

    write_header(base_file, target_file)
    write_mesh_header(base_file, target_file)
    for i in range(mesh_count):
        write_bones_mesh_header(base_file, target_file, i)
        write_vertice_mesh(base_file, target_file, i)
        write_material_mesh(base_file, target_file, i)
        write_faces_mesh(base_file, target_file, i)
    write_bones(base_file, target_file)
    write_texture(base_file, target_file)
    write_model_name(base_file, target_file)
    generate_pof0(target_file)
    print("Object duplicated successfully!")

    # Close the files before renaming
    if base_file:
        base_file.close()
    if target_file:
        target_file.close()
    # Rename 0002-NEW.yobj menjadi 0002.yobj
    infile_path = file_path_var.get()  # File input asli
    if not infile_path:
        print("No input file specified!")
        return

    # Path file output (0002-NEW.yobj)
    infile_name = os.path.basename(infile_path)
    outfile_name = os.path.splitext(infile_name)[0] + "-NEW.yobj"
    outfile_path = os.path.join(os.path.dirname(infile_path), outfile_name)

    if os.path.exists(outfile_path):
        try:
            os.replace(outfile_path, infile_path)  # Mengganti nama file
            print(f"Replaced {outfile_path} with {infile_path}")
        except OSError as e:
            print(f"Error renaming file: {e}")
            return
    else:
        print(f"Output file {outfile_path} not found. Cannot rename!")
        return

    # Kosongkan listbox dan reset variabel
    object_listbox.delete(0, tk.END)
    reset_variables()

    # Baca ulang file
    read_file()
    messagebox.showinfo("Success", "Object duplicated and POF0 generated")


def remove_selected_object():
    global base_file, target_file  # Menggunakan variabel global

    selected_index = object_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error","No object selected!")
        return

    selected_object = selected_index[0]
    print(f"Selected Object: {selected_object}")

    try:
        remove_mesh(base_file, target_file, selected_object)  # Memanggil prosedur duplicate_mesh
    except Exception as e:
        print(f"Error remove object: {e}")
        messagebox.showerror("Error","Error remove object")
        return

    write_header(base_file, target_file)
    write_mesh_header(base_file, target_file)
    for i in range(mesh_count):
        write_bones_mesh_header(base_file, target_file, i)
        write_vertice_mesh(base_file, target_file, i)
        write_material_mesh(base_file, target_file, i)
        write_faces_mesh(base_file, target_file, i)
    write_bones(base_file, target_file)
    write_texture(base_file, target_file)
    write_model_name(base_file, target_file)
    generate_pof0(target_file)
    print("Object removed successfully!")

    # Close the files before renaming
    if base_file:
        base_file.close()
    if target_file:
        target_file.close()
    # Rename 0002-NEW.yobj menjadi 0002.yobj
    infile_path = file_path_var.get()  # File input asli
    if not infile_path:
        print("No input file specified!")
        return

    # Path file output (0002-NEW.yobj)
    infile_name = os.path.basename(infile_path)
    outfile_name = os.path.splitext(infile_name)[0] + "-NEW.yobj"
    outfile_path = os.path.join(os.path.dirname(infile_path), outfile_name)

    if os.path.exists(outfile_path):
        try:
            os.replace(outfile_path, infile_path)  # Mengganti nama file
            print(f"Replaced {outfile_path} with {infile_path}")
        except OSError as e:
            print(f"Error renaming file: {e}")
            return
    else:
        print(f"Output file {outfile_path} not found. Cannot rename!")
        return

    # Kosongkan listbox dan reset variabel
    object_listbox.delete(0, tk.END)
    reset_variables()

    # Baca ulang file
    read_file()
    messagebox.showinfo("Success", "Object removed and POF0 generated")
    pass

# GUI setup
root = tk.Tk()
root.title("YOBJ Mesh/OBject Editor PSP")

file_path_var = tk.StringVar()

# File browse
tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, textvariable=file_path_var, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Object listbox
tk.Label(root, text="Objects:").grid(row=1, column=0, padx=10, pady=10)
object_listbox = Listbox(root, selectmode=tk.SINGLE, height=10, width=80)
object_listbox.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Duplicate and Remove buttons
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=1, padx=10, pady=10)

duplicate_button = tk.Button(button_frame, text="Duplicate", command=duplicate_selected_object)
duplicate_button.pack(side=tk.LEFT, padx=(0, 10))

remove_button = tk.Button(button_frame, text="Remove", command=remove_selected_object)
remove_button.pack(side=tk.LEFT)

root.mainloop()
