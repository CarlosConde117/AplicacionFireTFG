

ListaMapas =[["Seleccione mapa existente"]]

ListaModelosCamaras = [["Seleccione modelo existente"],["Prueba", "1", "2", "3", "4", "5", "200"]]

ListaArchivosDem = [["Seleccione archivo"],["PruebaDEM","C:", 0]] #[Nombre,Directorio,estado] estado = 0 ---> archivo cargado

ListaArchivosPuntuaciones = [["Seleccione archivo"],["PruebaPuntuaciones","C:", 0]] #[Nombre,Directorio,estado] estado = 0 ---> archivo cargado


ListaArchivosShape = [["Seleccione archivo"],["PruebaShape","C:", 0]] #[Nombre,Directorio,estado] estado = 0 ---> archivo cargado


ListaParametrosOptimizador = []

directorioDEM=""
directorioShape =""
directorioWeight=""



#VARIABLES POP UP ID

ModeloSeleccionadoID = ""
NumeroRestantesID = 0

#Variables dibujo

ListaPuntos = []


#VARIABLES MAPAS CACHE

ListaPoligonosCache= []  #[[Poligono1],[Poligono2]]
ListaCirculosCache = []
ListaMakerCache = []



#LISTA CAMARAS POSICIONADAS
ListaCamarasPosicionadas = []  # [id,modelo,posicion,superfice,puntuacion,numeroFila,dibujada]  ----- una lista por cada camara


#VARIABLES CAMARAS

listaPuntos = []
puntosX = []
puntosY = []
finLecturaLog = False
