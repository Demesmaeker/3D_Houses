class Raster2xyz(object):

    def __init__(self, verbose=True):
      pass

    def __geotrCoords(self, gtr, x, y):
      #(167938.0000000021, 1.0, 0.0, 147400.99999999837, 0.0, -1.0)
      #[  0   1   2 ... 124 125 126]
      #[  0   0   0 ... 118 118 118]
      print(x)
      print(y)
      print(gtr)
      try:
        gtr_x = gtr[0] + (x) * gtr[1] + (y) * gtr[2]
        gtr_y = gtr[3] + (x) * gtr[4] + (y) * gtr[5]

        #gtr_x = x
        #gtr_y = 

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

      return self.__buildXyzData(gtr_x, gtr_y, data_vals)


raster2xyz = Raster2xyz()