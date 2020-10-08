import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import rasterio as rio
from rasterio.plot import show
import earthpy as et
import earthpy.plot as ep

number = 5

# DSM
dsm_path = f'F:/Resources/Flandre/DSM/DHMVIIDSMRAS1m_k{number:02d}/GeoTIFF/DHMVIIDSMRAS1m_k{number:02d}.tif'
# img = rio.open(dsm_path)
# show(img)

# DTM
dtm_path = f'F:/Resources/Flandre/DTM/DHMVIIDTMRAS1m_k{number:02d}/GeoTIFF/DHMVIIDTMRAS1m_k{number:02d}.tif'
# img = rio.open(dtm_path)
# show(img)

