import numpy as np
import pandas as pd

class Raster2xyz(object):

    def __init__(self, verbose=True):
      pass

    def __geotrCoords(self, gtr, x, y):
      try:
        gtr_x = x
        gtr_y = y

        return(gtr_x, gtr_y)

      except Exception as err:
        self.__logger.error("Error getting geotransformed coordinates: {0}".format(err))

    def __getXyzData(self, raster_values, no_data):

        try:
            y, x = np.where(raster_values != no_data)
            data_vals = np.extract(raster_values != no_data, raster_values)

            return(x, y, data_vals)

        except Exception as err:
            print("Error getting XYZ data: {0}".format(err))

    def __buildXyzData(self, gtr_x, gtr_y, data_vals):

        try:
            data_dict = {
                "x": gtr_x,
                "y": gtr_y,
                "z": data_vals
            }

            return pd.DataFrame(data_dict)

        except Exception as err:
            print("Error building XYZ data: {0}".format(err))
    
    def __convert_meta(self, meta):
      return (meta[2], meta[0], meta[1], meta[5], meta[3], meta[4])
    
    def translate_from_cropped(self, crop_result, no_data=-9999):

      # Clean the received data
      raster, meta = crop_result
      meta = self.__convert_meta(meta['transform'])

      # Prepare the transformation
      x, y, data_vals = self.__getXyzData(raster, no_data)
      gtr_x, gtr_y = self.__geotrCoords(meta, x, y)

      return self.__buildXyzData(gtr_x, gtr_y, data_vals), (meta[0], meta[3])


raster2xyz = Raster2xyz()