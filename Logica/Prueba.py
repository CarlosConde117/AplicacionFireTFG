import os
import shutil

import numpy as np

ruta1 = r'C:/Users/Carlos/Desktop/AplicacionTGF/fire/project'
outPath = ruta1 + '/results/temp_visibility.TIF'
import rasterio as rio
import folium
from pyproj import Transformer

## LC08 RGB Image
in_path = 'RGB.TIF'

dst_crs = 'EPSG:3035'

with rio.open(outPath) as src:
    boundary = src.bounds
    img = src.read(1)
    nodata = src.nodata

    img[img == nodata] = np.nan
    min_lon, min_lat, max_lon, max_lat = src.bounds

## Conversion from UTM to WGS84 CRS
bounds_orig = [[min_lat, min_lon], [max_lat, max_lon]]

bounds_fin = []

for item in bounds_orig:
    # converting to lat/lon
    lat = item[0]
    lon = item[1]

    proj = Transformer.from_crs('EPSG:3035', 'EPSG:4326', always_xy=True)

    lon_n, lat_n = proj.transform(lon, lat)

    bounds_fin.append([lat_n, lon_n])

# Finding the centre latitude & longitude
centre_lon = bounds_fin[0][1] + (bounds_fin[1][1] - bounds_fin[0][1]) / 2
centre_lat = bounds_fin[0][0] + (bounds_fin[1][0] - bounds_fin[0][0]) / 2

m = folium.Map(location=[centre_lat, centre_lon],
               tiles='Stamen Terrain', zoom_start=10)

# Overlay raster (RGB) called img using add_child() function (opacity and bounding box set)
m.add_child(folium.raster_layers.ImageOverlay(img,opacity=.7,
                                              bounds=bounds_fin))

# Display map
m.save("Prueba.html")
directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directorioOrigen = directorio + '\\Views\\Prueba.html'
directorioDestino = directorio + '\\Mapas\\Prueba.html'
shutil.move(directorioOrigen, directorioDestino)