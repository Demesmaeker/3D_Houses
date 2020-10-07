import numpy
import pandas
import rasterio
from rasterio.plot import show

fp = r'App/Resources/01_DSM/GeoTIFF/01_DSM.tif'
img = rasterio.open(fp)
show(img)