import pyvista as pv
import numpy as np
import os

dataset_folder = 'starccm_dataset'
output_folder = 'starccm_vtp'

i=0
for case_file in os.listdir(dataset_folder):
    if case_file.endswith('.case'):
        mb=pv.read(os.path.join(dataset_folder,case_file))
        grid=mb[0]
        poly=grid.extract_geometry()
        p=grid.point_data["Pressure"]
        u=grid.point_data["Velocityi"]
        v=grid.point_data["Velocityj"]

        # clear point data
        poly.clear_point_data()
        poly.point_data["marker"] = np.zeros(poly.n_points,dtype=int)
        poly.point_data["p"]=p
        poly.point_data["u"]=u
        poly.point_data["v"]=v
        
        # iterate over all points and find boundary points

        edges=poly.extract_feature_edges()
        edge_points=edges.points
        # mark all edge points with 4
        poly.point_data["marker"][np.where(np.isin(poly.points,edge_points).all(axis=1))] = 4
        
        min_x,max_x = grid.bounds[0],grid.bounds[1]
        poly.point_data["marker"][poly.points[:,0] == min_x] = 1
        poly.point_data["marker"][poly.points[:,0] == max_x] = 1
        
        poly.save(os.path.join(output_folder,f"res_{i}.vtp"))
        i+=1