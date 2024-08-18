# How the input works

The input is a `.vtp` file with the input geometry as well as the target field for calculating the accuracy of the prediction.

The file is a VTK XML PolyData file with a 2d unstructured mesh. The points are 3d but the third coordinate is always 0. The cells are triangles.

The nodes have the following fields:

- `marker`: integer, defining the boundary condition of the node. The boundary conditions are (reverse engineered from example data):
  - 0: Free boundary (inner nodes)
  - 1: Inlet or outlet
  - 2: ???
  - 3: ???
  - 4: Wall
- Target fields:
  - `u`: float, the x component of the target field
  - `v`: float, the y component of the target field
  - `p`: float, the pressure field

The graph is built in `modulus/modulus/datapipes/gnn/stokes_dataset.py`.