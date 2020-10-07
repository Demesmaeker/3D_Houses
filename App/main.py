import numpy
import pandas
import rasterio
from rasterio.plot import show

number = 5

# DSM
fp = f'App/Resources/Flandre/DHMVIIDSMRAS1m_k{number:02d}/GeoTIFF/DHMVIIDSMRAS1m_k{number:02d}.tif'
img = rasterio.open(fp)
show(img)

# DTM
# fp = r'App/Resources/01_DTM/GeoTIFF/01_DTM.tif'
# img = rasterio.open(fp)
# show(img)