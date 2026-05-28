# YOBJ-Mesh-Object-Editor-PSP
YOBJ Mesh/Object Editor PSP is a utility program for managing and modifying `.yobj` files used in WWE Games for PSP. These files typically contain multiple mesh objects bundled together. This tool provides a user-friendly way to organize, duplicate, and remove individual meshes within a `.yobj` file.

## Features

- **Duplicate**: Easily clone any mesh object contained in a `.yobj` file.  
- **Remove**: Remove unnecessary or unused meshes from the file.  
- **Rebuild**: Automatically organizes and rewrites the internal structure of the `.yobj` file for better readability and consistency.  
- **Export to OBJ**: Export meshes into `.OBJ` format including **Vertices, UVs, Faces, and Normals**, along with `.MTL` material files for texture references.  
- **Export to DAE**: Export meshes into `.DAE` (COLLADA) format, primarily used for **weight and bone modifications** in Blender or other 3D tools.  
- **Import from OBJ**: Import `.OBJ` files back into the `.yobj` structure, allowing modification of **vertex positions and normals** while preserving UVs and faces.  
- **Import from DAE**: Import `.DAE` files to integrate meshes with updated **weights, bones, and rigging data** for in‑game compatibility. This feature also supports **adding new custom meshes** into the `.yobj` file.
