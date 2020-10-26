import numpy as np
import rasterio as rio

def set_path_dsm(province):
    wal_dsm = f"/home/demes/Documents/Ressources/Wallonia/DSM 2013-2014/RELIEF_WALLONIE_MNS_2013_2014_GEOTIFF_31370_PROV_{province}/RELIEF_WALLONIE_MNS_2013_2014.tif"
    return wal_dsm

def set_path_dtm(province):
    wal_dtm = f"/home/demes/Documents/Ressources/Wallonia/DTM 2013-2014/RELIEF_WALLONIE_MNT_2013_2014_GEOTIFF_31370_PROV_{province}/RELIEF_WALLONIE_MNT_2013_2014.tif"
    return wal_dtm

def get_mask(path, shape):
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