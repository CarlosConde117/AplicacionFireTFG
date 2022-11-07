import folium
import os
import shutil


#FUNCIONA CORRECTAMENTE, GUARDA DIRECTORIO EN XML
import numpy as np


def cargarMapa(latitud ,longitud , nombre):


    mapa = folium.Map(location=[latitud, longitud], zoom_start= 14)




    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\Mapas\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)

    from ArchivosXML.FuncionesXML import insertaNuevoMapa
    insertaNuevoMapa(nombre,directorioDestino,latitud,longitud)

    from VariablesGlobales.VarGlo import ListaMapas
    ListaMapas.clear()
    ListaMapas.append(["Seleccione mapa existente"])




def dibujaCirculo(latitud,longitud,nombre,radio,relleno = False):
    mapa = folium.Map(location=[latitud, longitud], zoom_start=14)

    folium.Circle(
        radius=radio,
        location=[latitud, longitud],
        color="crimson",
        fill=relleno,
    ).add_to(mapa)

    #FUNCIONES DIBUJAR POLIGONOS CACHE

    from ArchivosXML.FuncionesXML import BuscaCirculos,BuscaMaker,BuscaPoligonos,PopUpCamara
    BuscaCirculos()
    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import ListaCirculosCache,ListaMakerCache,ListaPoligonosCache
    if len(ListaCirculosCache) > 0:
        for i in range(len(ListaCirculosCache)):
            folium.Circle(
                radius=float(ListaCirculosCache[i][2]),
                location=[float(ListaCirculosCache[i][0]), float(ListaCirculosCache[i][1])],
                color="crimson",
                fill=relleno,
            ).add_to(mapa)

    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            id = ListaMakerCache[i][2]
            TextoPopUp = PopUpCamara(id)
            folium.Marker(
                location=[ListaMakerCache[i][0], ListaMakerCache[i][1]],
                icon=folium.Icon(color='lightgray', icon='glyphicon glyphicon-camera',popup = TextoPopUp)
            ).add_to(mapa)

    if len(ListaPoligonosCache) > 0:
        for poligono in ListaPoligonosCache :
            folium.Polygon(
                poligono,
                weight=2,
                fill=True,
                fill_color="orange",
                fill_opacity=0.4
            ).add_to(mapa)



    #Insertamos el nuevo circulo en el archivo cache

    from ArchivosXML.FuncionesXML import InsertaCirculoCache
    List = [latitud, longitud, radio]
    InsertaCirculoCache(str(List))


    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\MapasCache\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)



def dibujaPoligono(ListaPuntos,latCentral,lonCentral,nombre,rellenoCirculo = False): #PASARLE LISTA DE TUPLAS

    mapa = folium.Map(location=[latCentral, lonCentral], zoom_start=14)

    folium.Polygon(
        ListaPuntos,
        weight=2,
        fill=True,
        fill_color="orange",
        fill_opacity=0.4
    ).add_to(mapa)

    # FUNCIONES DIBUJAR POLIGONOS CACHE

    from ArchivosXML.FuncionesXML import BuscaCirculos, BuscaMaker, BuscaPoligonos,PopUpCamara
    BuscaCirculos()
    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import ListaCirculosCache, ListaMakerCache, ListaPoligonosCache
    if len(ListaCirculosCache) > 0:
        for i in range(len(ListaCirculosCache)):
            folium.Circle(
                radius=float(ListaCirculosCache[i][2]),
                location=[float(ListaCirculosCache[i][0]), float(ListaCirculosCache[i][1])],
                color="crimson",
                fill=rellenoCirculo,
            ).add_to(mapa)

    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            id = ListaMakerCache[i][2]
            TextoPopUp = PopUpCamara(id)
            folium.Marker(
                location=[ListaMakerCache[i][0], ListaMakerCache[i][1]],
                icon=folium.Icon(color='lightgray', icon='glyphicon glyphicon-camera', popup = TextoPopUp)
            ).add_to(mapa)

    if len(ListaPoligonosCache) > 0:
        for poligono in ListaPoligonosCache:
            folium.Polygon(
                poligono,
                weight=2,
                fill=True,
                fill_color="orange",
                fill_opacity=0.4
            ).add_to(mapa)

    #Insertamos el nuevo Poligono en el cache

    from ArchivosXML.FuncionesXML import InsertaPoligonoCache
    listaAux = []
    for punto in ListaPuntos:
            lat = punto[0]
            long = punto[1]
            cadenaTexto = str(lat) + ";" + str(long)
            listaAux.append(cadenaTexto)

    InsertaPoligonoCache(str(listaAux))





    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\MapasCache\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)



def PintaCamara(Lat,Long,nombre,id,rellenoCirculo = False):
    from ArchivosXML.FuncionesXML import PopUpCamara
    texto = PopUpCamara(id)
    mapa = folium.Map(location=[Lat, Long], zoom_start=14)
    folium.Marker(
        location=[Lat, Long],
        icon=folium.Icon(color='green', icon='glyphicon glyphicon-camera', popup= texto, tooltip= 'Información modelo')
    ).add_to(mapa)

    # FUNCIONES DIBUJAR POLIGONOS CACHE

    from ArchivosXML.FuncionesXML import BuscaCirculos, BuscaMaker, BuscaPoligonos
    BuscaCirculos()
    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import ListaCirculosCache, ListaMakerCache, ListaPoligonosCache
    if len(ListaCirculosCache) > 0:
        for i in range(len(ListaCirculosCache)):
            folium.Circle(
                radius=float(ListaCirculosCache[i][2]),
                location=[float(ListaCirculosCache[i][0]), float(ListaCirculosCache[i][1])],
                color="crimson",
                fill=rellenoCirculo,
            ).add_to(mapa)

    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            id = ListaMakerCache[i][2]
            texto = PopUpCamara(id)
            folium.Marker(
                location=[ListaMakerCache[i][0], ListaMakerCache[i][1]],
                icon=folium.Icon(color='green', icon='glyphicon glyphicon-camera', popup = texto)
            ).add_to(mapa)

    if len(ListaPoligonosCache) > 0:
        for poligono in ListaPoligonosCache:
            folium.Polygon(
                poligono,
                weight=2,
                fill=True,
                fill_color="orange",
                fill_opacity=0.4
            ).add_to(mapa)

    #Insertamos la camara en los archivos cache
    from ArchivosXML.FuncionesXML import InsertaMakerCache
    Lista = [[Lat,Long]]
    InsertaMakerCache(str(Lista),id)




    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\MapasCache\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)


def PintaCamaraCache(Lat,Long, nombre):
    mapa = folium.Map(location=[Lat, Long], zoom_start=14)


    # FUNCIONES DIBUJAR POLIGONOS CACHE

    from ArchivosXML.FuncionesXML import BuscaCirculos, BuscaMaker, BuscaPoligonos

    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import  ListaMakerCache


    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            folium.Marker(
                location=[ListaMakerCache[i][0], ListaMakerCache[i][1]],
                icon=folium.Icon(color='green', icon='glyphicon glyphicon-camera')
            ).add_to(mapa)


    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\MapasCache\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)


def eliminaCamara(Lat,Long,nombre,id,rellenoCirculo = False):
    mapa = folium.Map(location=[Lat, Long], zoom_start=14)


    # FUNCIONES DIBUJAR POLIGONOS CACHE

    from ArchivosXML.FuncionesXML import BuscaCirculos, BuscaMaker, BuscaPoligonos,eliminaMaher
    eliminaMaher(id)
    BuscaCirculos()
    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import ListaCirculosCache, ListaMakerCache, ListaPoligonosCache
    if len(ListaCirculosCache) > 0:
        for i in range(len(ListaCirculosCache)):
            folium.Circle(
                radius=float(ListaCirculosCache[i][2]),
                location=[float(ListaCirculosCache[i][0]), float(ListaCirculosCache[i][1])],
                color="crimson",
                fill=rellenoCirculo,
            ).add_to(mapa)

    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            folium.Marker(
                location=[float(ListaMakerCache[i][0]), float(ListaMakerCache[i][1])],
                icon=folium.Icon(color='green', icon='glyphicon glyphicon-camera')
            ).add_to(mapa)

    if len(ListaPoligonosCache) > 0:
        for poligono in ListaPoligonosCache:
            folium.Polygon(
                poligono,
                weight=2,
                fill=True,
                fill_color="orange",
                fill_opacity=0.4
            ).add_to(mapa)


    mapa.save(nombre + ".html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\' + nombre + '.html'
    directorioDestino = directorio + '\\MapasCache\\' + nombre + '.html'

    shutil.move(directorioOrigen, directorioDestino)



def muestraTiff ():
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

    m = folium.Map(location=[centre_lat, centre_lon],zoom_start=14)


    # Overlay raster (RGB) called img using add_child() function (opacity and bounding box set)
    m.add_child(folium.raster_layers.ImageOverlay(img, opacity=.7,
                                                  bounds=bounds_fin))

    from ArchivosXML.FuncionesXML import BuscaCirculos, BuscaMaker, BuscaPoligonos
    BuscaCirculos()
    BuscaMaker()
    BuscaPoligonos()
    from VariablesGlobales.VarGlo import ListaCirculosCache, ListaMakerCache, ListaPoligonosCache
    if len(ListaCirculosCache) > 0:
        for i in range(len(ListaCirculosCache)):
            folium.Circle(
                radius=float(ListaCirculosCache[i][2]),
                location=[float(ListaCirculosCache[i][0]), float(ListaCirculosCache[i][1])],
                color="crimson",
                fill=False,
            ).add_to(m)

    if len(ListaMakerCache) > 0:
        for i in range(len(ListaMakerCache)):
            id = ListaMakerCache[i][2]

            folium.Marker(
                location=[ListaMakerCache[i][0], ListaMakerCache[i][1]],
                icon=folium.Icon(color='green', icon='glyphicon glyphicon-camera', popup="")
            ).add_to(m)

    if len(ListaPoligonosCache) > 0:
        for poligono in ListaPoligonosCache:
            folium.Polygon(
                poligono,
                weight=2,
                fill=True,
                fill_color="orange",
                fill_opacity=0.4
            ).add_to(m)

    # Display map
    m.save("Prueba.html")
    directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    directorioOrigen = directorio + '\\Views\\Prueba.html'
    directorioDestino = directorio + '\\Mapas\\Prueba.html'
    shutil.move(directorioOrigen, directorioDestino)












