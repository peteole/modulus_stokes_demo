import select_geometry
channel_length=2
channel_height=0.5
polygon_points=select_geometry.create_polygon((channel_length,channel_height))
print("Selected points:", polygon_points)

import meshing
meshing.mesh_polygon(channel_length, channel_height,polygon_points, 'meshes/test/0')