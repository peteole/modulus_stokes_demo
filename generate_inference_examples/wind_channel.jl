using Gmsh

# Initialize Gmsh
gmsh.initialize(["","-bin"])
#gmsh.option.set("General.Terminal", 1)

# Step 1: Define the Geometry
gmsh.model.add("WindChannel")
mesh_size=0.02

# Define Points (Corner Points of the Rectangle - Wind Channel)
p1 = gmsh.model.geo.addPoint(0.0, 0.0, 0.0, mesh_size)
p2 = gmsh.model.geo.addPoint(2.0, 0.0, 0.0, mesh_size)
p3 = gmsh.model.geo.addPoint(2.0, 0.5, 0.0, mesh_size)
p4 = gmsh.model.geo.addPoint(0.0, 0.5, 0.0, mesh_size)

# Define the Polygon (Triangular Polygon inside the channel)
p5 = gmsh.model.geo.addPoint(0.5, 0.1, 0.0, mesh_size)
p6 = gmsh.model.geo.addPoint(1.5, 0.1, 0.0, mesh_size)
p7 = gmsh.model.geo.addPoint(1.0, 0.4, 0.0, mesh_size)

# Define Lines for the Wind Channel
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

# Define Lines for the Polygon (Triangle)
l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p5)

# Define Surface Loops
ll1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])  # Loop for the outer rectangle (wind channel)
ll2 = gmsh.model.geo.addCurveLoop([l5, l6, l7])      # Loop for the inner triangle (polygon)

# Define Plane Surfaces
s1 = gmsh.model.geo.addPlaneSurface([ll1, ll2])  # Surface for the wind channel with the polygon inside

# Step 2: Define the Mesh
# Set mesh element size on the lines
#gmsh.model.mesh.setCharacteristicLength([p1, p2, p3, p4, p5, p6, p7], 0.05)

# Step 3: Mesh Generation
# Generate 2D mesh
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)

# Save the mesh to a file
gmsh.
gmsh.write("wind_channel.vtk")

# Finalize Gmsh
gmsh.finalize()