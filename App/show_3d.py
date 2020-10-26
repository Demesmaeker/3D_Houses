import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

import open3d as o3d

pcd = o3d.io.read_point_cloud("../Outputs/df.txt", format='xyz')