import numpy as np
import pandas as pd
import rasterio as rio
import open3d as o3d
import matplotlib.pyplot as plt

def set_path_dsm(province):
    '''
    Take the name of a waloon province.
    Return the path of the corresponding dsm.
    '''
    wal_dsm = f"/home/demes/Documents/Ressources/Wallonia/DSM 2013-2014/RELIEF_WALLONIE_MNS_2013_2014_GEOTIFF_31370_PROV_{province}/RELIEF_WALLONIE_MNS_2013_2014.tif"
    return wal_dsm

def set_path_dtm(province):
    '''
    Take the name of a waloon province.
    Return the path of the corresponding dtm.
    '''
    wal_dtm = f"/home/demes/Documents/Ressources/Wallonia/DTM 2013-2014/RELIEF_WALLONIE_MNT_2013_2014_GEOTIFF_31370_PROV_{province}/RELIEF_WALLONIE_MNT_2013_2014.tif"
    return wal_dtm


def get_mask(path, shape):
    '''
    Take a path and a shape.
    Using rasterio, return a masked image of the shape asked, with the meta-datas.
    '''
    with rio.open(path) as tif_file:  
        out_image, out_transform = rio.mask.mask(tif_file, shapes=shape, all_touched=True, crop=True)
        out_meta = tif_file.meta

        # Remove the third axis (check if also in Flanders)
        out_image = np.moveaxis(out_image.squeeze(), -1, 0)

        # Update the new tiff file metadata
        out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[0],
                     "width": out_image.shape[1],
                     "transform": out_transform })
                     #'nodata': no_data})
    return out_image, out_meta


def get_dataframe(datas):
    '''
    Take datas with the xyz position in a dataframe + the bases coordinates
    Return the dataframe modified wwith the bases coordinates.
    '''

    raw_df= datas[0]
    bases = datas[1]

    df = pd.DataFrame()

    df['x'] = raw_df['x'] + bases[1]
    df['y'] = raw_df['y'] + bases[0]
    df['z'] = raw_df['z']

    return df


def get_chm_df(df_dsm, df_dtm):
    df = pd.DataFrame()

    df['x'] = df_dsm['x']
    df['y'] = df_dsm['y']
    df['z'] = df_dsm['z'] - df_dtm['z']

    return df


def show_pcd(df):
    '''
    Take a dataframe of points cloud.
    Show the visualisation in open3d in points cloud form.
    '''
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(df.to_numpy())
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    o3d.visualization.draw_geometries([pcd])


def show_poisson(df):
    '''
    Take a dataframe of points cloud.
    This function use poisson, like a clothes englobing the points.
    Show the 3D representation, in open3d.
    '''

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(df.to_numpy())
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=10, linear_fit =True)

    densities = np.asarray(densities)
    density_colors = plt.get_cmap('viridis')(
        (densities - densities.min()) / (densities.max() - densities.min()))
    density_colors = density_colors[:, :3]
    density_mesh = o3d.geometry.TriangleMesh()
    density_mesh.vertices = poisson_mesh.vertices
    density_mesh.triangles = poisson_mesh.triangles
    density_mesh.triangle_normals = poisson_mesh.triangle_normals
    density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)

    vertices_to_remove = densities < np.quantile(densities, 0.01)
    density_mesh.remove_vertices_by_mask(vertices_to_remove)

    o3d.visualization.draw_geometries([density_mesh])