from typing import List
import gmsh

import pyvista as pv
import numpy as np
import json

def mesh_polygon(channel_length:float, channel_height:float, polygon_points:List[float], filename:str):
        
    # Initialize Gmsh
    gmsh.initialize(["", "-bin"])
    # gmsh.option.set("General.Terminal", 1)  # Uncomment to see output in terminal

    # Step 1: Define the Geometry
    gmsh.model.add("WindChannel")
    mesh_size = 0.02

    # Define Points (Corner Points of the Rectangle - Wind Channel)
    p1 = gmsh.model.geo.addPoint(0.0, 0.0, 0.0, mesh_size)
    p2 = gmsh.model.geo.addPoint(channel_length, 0.0, 0.0, mesh_size)
    p3 = gmsh.model.geo.addPoint(channel_length, channel_height, 0.0, mesh_size)
    p4 = gmsh.model.geo.addPoint(0.0, channel_height, 0.0, mesh_size)

    #polygon_points = [(0.5, 0.1), (1.5, 0.2), (1.0, 0.4)]
    # Define the Polygon (Triangular Polygon inside the channel)
    # p5 = gmsh.model.geo.addPoint(0.5, 0.1, 0.0, mesh_size)
    # p6 = gmsh.model.geo.addPoint(1.5, 0.1, 0.0, mesh_size)
    # p7 = gmsh.model.geo.addPoint(1.0, 0.4, 0.0, mesh_size)
    polygon_gmsh_points = [gmsh.model.geo.addPoint(x, y, 0.0, mesh_size) for x, y in polygon_points]

    # Define Lines for the Wind Channel
    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)

    # # Define Lines for the Polygon (Triangle)
    # l5 = gmsh.model.geo.addLine(p5, p6)
    # l6 = gmsh.model.geo.addLine(p6, p7)
    # l7 = gmsh.model.geo.addLine(p7, p5)
    polygon_lines = [gmsh.model.geo.addLine(polygon_gmsh_points[i], polygon_gmsh_points[(i+1)%len(polygon_gmsh_points)]) for i in range(len(polygon_gmsh_points))]

    # Define Surface Loops
    ll1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])  # Loop for the outer rectangle (wind channel)
    ll2 = gmsh.model.geo.addCurveLoop(polygon_lines)      # Loop for the inner triangle (polygon)

    # Define Plane Surfaces
    s1 = gmsh.model.geo.addPlaneSurface([ll1, ll2])  # Surface for the wind channel with the polygon inside

    # Step 2: Define the Mesh
    # Synchronize to prepare for mesh generation
    gmsh.model.geo.synchronize()

    # Step 3: Mesh Generation
    # Generate 2D mesh
    gmsh.model.mesh.generate(2)

    # Save the mesh to a binary file
    gmsh.write("tmp.vtk")

    # Finalize Gmsh
    gmsh.finalize()


    grid=pv.read("tmp.vtk").extract_geometry()
    points = grid.points
    num_points = grid.number_of_points

    grid.point_data["marker"]=np.zeros(num_points)
    
    edges=grid.extract_feature_edges()
    edge_points=edges.points
    # mark all edge points with 4
    grid.point_data["marker"][np.where(np.isin(grid.points,edge_points).all(axis=1))] = 4

    # set marker to 1 at inlet and 2 at outlet
    grid.point_data["marker"][points[:,0]==0.0]=1
    grid.point_data["marker"][points[:,0]==channel_length]=2

    # set marker to 3 at top and bottom walls
    grid.point_data["marker"][points[:,1]==0.0]=3
    grid.point_data["marker"][points[:,1]==channel_height]=3

    for target in ["p","u","v"]:
        grid.point_data[target]=np.zeros(num_points)


    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    grid.save(f"{filename}.vtp")