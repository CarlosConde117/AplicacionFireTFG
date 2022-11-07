from xml.dom import minidom

from xml.dom.minidom import parse

ListaUnidadesModelos = []  #[[nombre,NumeroUnidades]]

#FUNCIONES MODELOS
def leeDatosModelosDEM():
    from VariablesGlobales.VarGlo import ListaArchivosDem
    ListaArchivosDem.clear()
    ListaArchivosDem.append(["Seleccione archivo"])
    doc = minidom.parse("../ArchivosXML/ArchivosAplicacion.xhtml")

    archivos = doc.getElementsByTagName("archivo")

    for archivo in archivos:
        tipoArchivo = archivo.getElementsByTagName("TipoArchivo")[0].firstChild.data
        if tipoArchivo == "DEM":
            Nombre = archivo.getElementsByTagName("Nombre")[0].firstChild.data
            directorio = archivo.getElementsByTagName("Directorio")[0].firstChild.data
            estado = archivo.getElementsByTagName("Estado")[0].firstChild.data

            ListaArchivosDem.append([Nombre, directorio, estado])

def leeDatosModelosSHAPE():
    from VariablesGlobales.VarGlo import ListaArchivosShape
    ListaArchivosShape.clear()
    ListaArchivosShape.append(["Seleccione archivo"])
    doc = minidom.parse("../ArchivosXML/ArchivosAplicacion.xhtml")

    archivos = doc.getElementsByTagName("archivo")

    for archivo in archivos:
        tipoArchivo = archivo.getElementsByTagName("TipoArchivo")[0].firstChild.data
        if tipoArchivo == "SHAPE":
            Nombre = archivo.getElementsByTagName("Nombre")[0].firstChild.data
            directorio = archivo.getElementsByTagName("Directorio")[0].firstChild.data
            estado = archivo.getElementsByTagName("Estado")[0].firstChild.data

            ListaArchivosShape.append([Nombre, directorio, estado])

def leeDatosModelosPUNT():
    from VariablesGlobales.VarGlo import ListaArchivosPuntuaciones
    ListaArchivosPuntuaciones.clear()
    ListaArchivosPuntuaciones.append(["Seleccione archivo"])
    doc = minidom.parse("../ArchivosXML/ArchivosAplicacion.xhtml")

    archivos = doc.getElementsByTagName("archivo")

    for archivo in archivos:
        tipoArchivo = archivo.getElementsByTagName("TipoArchivo")[0].firstChild.data
        if tipoArchivo == "PUNT":
            Nombre = archivo.getElementsByTagName("Nombre")[0].firstChild.data
            directorio = archivo.getElementsByTagName("Directorio")[0].firstChild.data
            estado = archivo.getElementsByTagName("Estado")[0].firstChild.data

            ListaArchivosPuntuaciones.append([Nombre, directorio, estado])

def insertaModelo(nombre, directorio, tipo, estado):

    doc = parse("../ArchivosXML/ArchivosAplicacion.xhtml")
    raiz = doc.documentElement

    nodo_archivo = doc.createElement("archivo")


    #Escribimos el nodo "Nombre"
    nodo_nombre = doc.createElement("Nombre")
    valor_nodo_nombre = doc.createTextNode(nombre)
    nodo_nombre.appendChild(valor_nodo_nombre)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_archivo.appendChild(nodo_nombre)

    # Escribimos el nodo "DirectorioDEM"
    nodo_directorio = doc.createElement("Directorio")
    valor_nodo_directorio = doc.createTextNode(directorio)
    nodo_directorio.appendChild(valor_nodo_directorio)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_archivo.appendChild(nodo_directorio)

    # Escribimos el nodo "DirectorioPuntuaciones"
    nodo_tipo = doc.createElement("TipoArchivo")
    valor_nodo_tipo = doc.createTextNode(tipo)
    nodo_tipo.appendChild(valor_nodo_tipo)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_archivo.appendChild(nodo_tipo)

    # Escribimos el nodo "DirectorioShape"
    nodo_estado = doc.createElement("Estado")
    valor_nodo_estado = doc.createTextNode(estado)
    nodo_estado.appendChild(valor_nodo_estado)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_archivo.appendChild(nodo_estado)

    raiz.appendChild(nodo_archivo)

    with open('../ArchivosXML/ArchivosAplicacion.xhtml', 'w') as f:

        doc.writexml(f, addindent=' ', encoding='utf-8')


def actualizaEstado(directorioActualiza,tipoArchivo,nuevoEstado):
    doc = parse("../ArchivosXML/ArchivosAplicacion.xhtml")
    raiz = doc.documentElement

    archivos = raiz.getElementsByTagName("archivo")

    for archivo in archivos:
        pn = archivo.parentNode

        directorio = pn.getElementsByTagName("Directorio")[0].firstChild.data
        tipo = pn.getElementsByTagName("TipoArchivo")[0].firstChild.data
        if directorio == directorioActualiza and tipo == tipoArchivo:
            estado = pn.getElementsByTagName("Estado")[0]
            estado.childNodes[0].data = nuevoEstado
        if tipo == tipoArchivo and directorio != directorioActualiza:
            estado = pn.getElementsByTagName("Estado")[0]
            estado.childNodes[0].data = "NoCargado"



    with open('../ArchivosXML/ArchivosAplicacion.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

    pass

def getEstadoArchivo(nombre):
    doc = parse("../ArchivosXML/ArchivosAplicacion.xhtml")
    raiz = doc.documentElement

    archivos = raiz.getElementsByTagName("archivo")

    for archivo in archivos:
        nombreAux = archivo.getElementsByTagName("Nombre")[0].firstChild.data

        if nombreAux == nombre:
            estado = archivo.getElementsByTagName("Estado")[0].firstChild.data

            return estado

def EliminarArchivos(nombre):
    doc = parse("../ArchivosXML/ArchivosAplicacion.xhtml")
    Archivos = doc.getElementsByTagName("archivo")
    for archivo in Archivos:
        nombreAux = archivo.getElementsByTagName("Nombre")[0].firstChild.data

        if nombreAux == nombre:
            archivo.parentNode.removeChild(archivo)

    with open('../ArchivosXML/ArchivosAplicacion.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

#FUNCIONES CAMARAS
def leeModelosCamaras():
    from VariablesGlobales.VarGlo import ListaModelosCamaras
    ListaModelosCamaras.clear()
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    ListaModelosCamaras.append(["Seleccione modelo existente"])
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data
        NumeroUnidades = modelo.getElementsByTagName("numeroUnidades")[0].firstChild.data
        visionAcimutal = modelo.getElementsByTagName("visionAcimutal")[0].firstChild.data
        radioMax = modelo.getElementsByTagName("radioMax")[0].firstChild.data
        radioMin = modelo.getElementsByTagName("radioMin")[0].firstChild.data
        inclinacion = modelo.getElementsByTagName("inclinacion")[0].firstChild.data



        # print(nombre)

        ListaModelosCamaras.append([nombre, visionAcimutal, inclinacion, radioMax, radioMin, NumeroUnidades])

def insertaModeloCamara(nombre,visionAcimutal,inclinacion,radioMax,radioMin,numeroUnidades = "1"):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    nodo_modelo = doc.createElement("modelo")

    nodo_nombre = doc.createElement("nombre")
    valor_nodo_nombre = doc.createTextNode(nombre)
    nodo_nombre.appendChild(valor_nodo_nombre)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_nombre)

    nodo_unidades = doc.createElement("numeroUnidades")
    valor_nodo_unidades = doc.createTextNode(numeroUnidades)
    nodo_unidades.appendChild(valor_nodo_unidades)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_unidades)

    nodo_Acimutal = doc.createElement("visionAcimutal")
    valor_nodo_Acimutal = doc.createTextNode(visionAcimutal)
    nodo_Acimutal.appendChild(valor_nodo_Acimutal)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_Acimutal)


    nodo_radioMax = doc.createElement("radioMax")
    valor_nodo_radioMax = doc.createTextNode(radioMax)
    nodo_radioMax.appendChild(valor_nodo_radioMax)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_radioMax)

    nodo_radioMin = doc.createElement("radioMin")
    valor_nodo_radioMin = doc.createTextNode(radioMin)
    nodo_radioMin.appendChild(valor_nodo_radioMin)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_radioMin)


    nodo_Inclinacion = doc.createElement("inclinacion")
    valor_nodo_Inclinacion = doc.createTextNode(inclinacion)
    nodo_Inclinacion.appendChild(valor_nodo_Inclinacion)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_modelo.appendChild(nodo_Inclinacion)

    raiz.appendChild(nodo_modelo)

    with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

def getTodosModelos():
    from VariablesGlobales.VarGlo import ListaModelosCamaras
    Lista = []
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    Lista.append("Seleccione modelo existente")
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data
        Lista.append(nombre)
    return Lista


def eliminaunaunidad(modeloActualizar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    NumeroUnidades = 0
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data

        if nombre == modeloActualizar:
            NumeroUnidades = modelo.getElementsByTagName("numeroUnidades")[0].firstChild.data
            break
    nuevoNumero = int(NumeroUnidades) -1

    nodoActualiza = doc.getElementsByTagName("nombre")
    for modelo in nodoActualiza:
        if modelo.childNodes[0].data == str(modeloActualizar):
            pn = modelo.parentNode

            numUnidades = pn.getElementsByTagName("numeroUnidades")[0]
            numUnidades.childNodes[0].data = str(nuevoNumero)

            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')
            break


def añadeunaunidad(modeloActualizar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    NumeroUnidades = 0
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data

        if nombre == modeloActualizar:
            NumeroUnidades = modelo.getElementsByTagName("numeroUnidades")[0].firstChild.data
            break
    nuevoNumero = int(NumeroUnidades) + 1

    nodoActualiza = doc.getElementsByTagName("nombre")
    for modelo in nodoActualiza:
        if modelo.childNodes[0].data == str(modeloActualizar):
            pn = modelo.parentNode

            numUnidades = pn.getElementsByTagName("numeroUnidades")[0]
            numUnidades.childNodes[0].data = str(nuevoNumero)

            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')
            break

def reseteaNumeroUnidades():
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    global ListaUnidadesModelos
    for modelo in modelos:
        cont = 0
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data
        camaras = doc.getElementsByTagName("camara")
        for camara in camaras:
            modeloCam = camara.getElementsByTagName("NombreModelo")[0].firstChild.data
            if modeloCam == nombre:
               cont += 1
        ListaUnidadesModelos.append([nombre,cont])

    actualizaListaModelos(ListaUnidadesModelos)

def actualizaListaModelos(ListaUnidades):

    for modeloLista in ListaUnidades:
        doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
        raiz = doc.documentElement
        modelos = raiz.getElementsByTagName("nombre")

        for modelo in modelos:
            if modelo.childNodes[0].data == modeloLista[0]:
                pn = modelo.parentNode

                implementada = pn.getElementsByTagName("numeroUnidades")[0]
                implementada.childNodes[0].data = modeloLista[1]

                with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                    doc.writexml(f, addindent=' ', encoding='utf-8')


def getNumeroUnidades(modeloBuscar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    NumeroUnidades = 0
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data

        if nombre == modeloBuscar:
            NumeroUnidades = modelo.getElementsByTagName("numeroUnidades")[0].firstChild.data
            return NumeroUnidades

def getNumeroTotalUnidades(modeloBuscar):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement
    camaras = raiz.getElementsByTagName("camara")
    cont = 0
    for camara in camaras:
        modeloAux = camara.getElementsByTagName("NombreModelo")[0].firstChild.data

        if modeloAux == modeloBuscar:
            cont += 1
    return cont



def compruebaModelo(modeloBuscar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    modelos = doc.getElementsByTagName("modelo")
    ModeloEncontrado = False
    for modelo in modelos:
        nombre = modelo.getElementsByTagName("nombre")[0].firstChild.data

        if nombre == modeloBuscar:
            ModeloEncontrado = True
            return ModeloEncontrado


def actualizaNumeroModelos(modeloActualizar,numeroUnidades):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    modelos = raiz.getElementsByTagName("nombre")

    for modelo in modelos:
        if modelo.childNodes[0].data == str(modeloActualizar):
            pn = modelo.parentNode

            num = pn.getElementsByTagName("numeroUnidades")[0]
            num.childNodes[0].data = str(numeroUnidades)


            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')


def insertaNuevaCamara(id, nombre, lalitud, longitud, implementada = False):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    nodo_camara = doc.createElement("camara")

    nodo_id = doc.createElement("id")
    valor_nodo_id = doc.createTextNode(id)
    nodo_id.appendChild(valor_nodo_id)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_camara.appendChild(nodo_id)

    nodo_nombre = doc.createElement("NombreModelo")
    valor_nodo_nombre = doc.createTextNode(nombre)
    nodo_nombre.appendChild(valor_nodo_nombre)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_camara.appendChild(nodo_nombre)

    nodo_latitud = doc.createElement("Latitud")
    valor_nodo_latitud = doc.createTextNode(lalitud)
    nodo_latitud.appendChild(valor_nodo_latitud)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_camara.appendChild(nodo_latitud)

    nodo_Longitud = doc.createElement("Longitud")
    valor_nodo_Longitud = doc.createTextNode(longitud)
    nodo_Longitud.appendChild(valor_nodo_Longitud)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_camara.appendChild(nodo_Longitud)

    nodo_Implementada = doc.createElement("Implementada")
    valor_nodo_Implementada = doc.createTextNode(str(implementada))
    nodo_Implementada.appendChild(valor_nodo_Implementada)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_camara.appendChild(nodo_Implementada)

    raiz.appendChild(nodo_camara)

    with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

def actualizaPosicionCamara(id, Nuevalatitud, Nuevalongitud):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    camaras = raiz.getElementsByTagName("id")

    for camara in camaras:
        if camara.childNodes[0].data == str(id):
            pn = camara.parentNode

            latitud = pn.getElementsByTagName("Latitud")[0]
            latitud.childNodes[0].data = str(Nuevalatitud)

            longitud = pn.getElementsByTagName("Longitud")[0]
            longitud.childNodes[0].data = str(Nuevalongitud)

            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')

    actualizaEstadoCamara(id, True)

def getPocionCamaraID(id):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement
    ListaPosciones = []
    camaras = raiz.getElementsByTagName("camara")

    for camara in camaras:
        idAux = camara.getElementsByTagName("id")[0].firstChild.data

        if idAux == id:
            Latitud = camara.getElementsByTagName("Latitud")[0].firstChild.data
            Longitud = camara.getElementsByTagName("Longitud")[0].firstChild.data
            ListaPosciones.append(Latitud)
            ListaPosciones.append( Longitud)
            return ListaPosciones

def getModeloID (id):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    camaras = raiz.getElementsByTagName("camara")

    for camara in camaras:
        idAux = camara.getElementsByTagName("id")[0].firstChild.data

        if idAux == id:
            modelo = camara.getElementsByTagName("NombreModelo")[0].firstChild.data


            return modelo

def getUnidadesImplemntadas(modeloBuscar):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement
    camaras = raiz.getElementsByTagName("camara")
    cont = 0

    for camara in camaras:
        modeloAux = camara.getElementsByTagName("NombreModelo")[0].firstChild.data

        if modeloAux == modeloBuscar:
            implementada = camara.getElementsByTagName("Implementada")[0].firstChild.data
            if implementada == "True":
                cont += 1
    return cont

def totalUnidadesImplementadas():
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement
    camaras = raiz.getElementsByTagName("camara")
    cont = 0

    for camara in camaras:
        implementada = camara.getElementsByTagName("Implementada")[0].firstChild.data
        if implementada == "True":
            cont += 1
    return cont


def getParametroCam(nombreModelo, parametroBuscar):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement
    camaras = raiz.getElementsByTagName("modelo")
    cont = 0

    for camara in camaras:
        modeloAux = camara.getElementsByTagName("nombre")[0].firstChild.data

        if modeloAux == nombreModelo:
            parametro = camara.getElementsByTagName(parametroBuscar)[0].firstChild.data

    return parametro

def eliminarCamaras(modeloBorrar, numeroBorrar):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    Camaras = doc.getElementsByTagName("camara")
    cont = int(numeroBorrar)
    for camara in Camaras:
        modeloAux = camara.getElementsByTagName("NombreModelo")[0].firstChild.data

        if modeloAux == modeloBorrar and cont != 0:

            camara.parentNode.removeChild(camara)
            cont -= 1

            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')


def compruebaId(idBuscar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    camaras = doc.getElementsByTagName("camara")
    IdEncontrado = False
    for camara in camaras:
        id = camara.getElementsByTagName("id")[0].firstChild.data

        if id == idBuscar:
            IdEncontrado = True
            return IdEncontrado

def actualizaEstadoCamara(id, estado):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement


    camaras = raiz.getElementsByTagName("id")

    for camara in camaras:
        if camara.childNodes[0].data == str(id):
            pn = camara.parentNode

            implementada = pn.getElementsByTagName("Implementada")[0]
            implementada.childNodes[0].data = str(estado)


            with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
                doc.writexml(f, addindent=' ', encoding='utf-8')
            break

def seleccionaUnaCamara(modeloUsar):
    doc = minidom.parse("../ArchivosXML/ModelosCamaras.xhtml")
    camaras = doc.getElementsByTagName("camara")
    for camara in camaras:
        modelo = camara.getElementsByTagName("NombreModelo")[0].firstChild.data
        usada = camara.getElementsByTagName("Implementada")[0].firstChild.data
        if modelo == modeloUsar and usada == "False":
            id = camara.getElementsByTagName("id")[0].firstChild.data
            return id
            break

def eliminarCamarasImplementadas():
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    camaras = raiz.getElementsByTagName("id")

    for camara in camaras:
        pn = camara.parentNode
        implementada = pn.getElementsByTagName("Implementada")[0]
        implementada.childNodes[0].data = str(False)

        with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
         doc.writexml(f, addindent=' ', encoding='utf-8')

def inicializaPosiciones():
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    raiz = doc.documentElement

    camaras = raiz.getElementsByTagName("id")

    for camara in camaras:
        pn = camara.parentNode
        latitud = pn.getElementsByTagName("Latitud")[0]
        latitud.childNodes[0].data = "-"

        longitud = pn.getElementsByTagName("Longitud")[0]
        longitud.childNodes[0].data = "-"


        with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
            doc.writexml(f, addindent=' ', encoding='utf-8')


def eliminaModeloCamara(nombreModelo):
    doc = parse("../ArchivosXML/ModelosCamaras.xhtml")
    Modelos = doc.getElementsByTagName("modelo")
    for modelo in Modelos:
        modeloAux = modelo.getElementsByTagName("nombre")[0].firstChild.data

        if modeloAux == nombreModelo:
            modelo.parentNode.removeChild(modelo)

    with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')




#FUNCIONES MAPA

def insertaNuevoMapa(nombre, directorio,latitudIni,longitudIni):#Funcion para insertar un nuevo mapa en xml(nombre,directorio)
        doc = parse("../ArchivosXML/Mapas.xhtml")
        raiz = doc.documentElement

        nodo_mapa = doc.createElement("mapa")


        nodo_nombre = doc.createElement("nombre")
        valor_nodo_nombre = doc.createTextNode(nombre)
        nodo_nombre.appendChild(valor_nodo_nombre)  # Cuelgue el nodo de texto en el nodo name_node
        nodo_mapa.appendChild(nodo_nombre)

        nodo_directorio = doc.createElement("directorioMapa")
        valor_nodo_directorio = doc.createTextNode(directorio)
        nodo_directorio.appendChild(valor_nodo_directorio)  # Cuelgue el nodo de texto en el nodo name_node
        nodo_mapa.appendChild(nodo_directorio)

        nodo_latitud = doc.createElement("LatitudIni")
        valor_nodo_latitud = doc.createTextNode(str(latitudIni))
        nodo_latitud.appendChild(valor_nodo_latitud)  # Cuelgue el nodo de texto en el nodo name_node
        nodo_mapa.appendChild(nodo_latitud)

        nodo_longitud = doc.createElement("LongitudIni")
        valor_nodo_longitud = doc.createTextNode(str(longitudIni))
        nodo_longitud.appendChild(valor_nodo_longitud)  # Cuelgue el nodo de texto en el nodo name_node
        nodo_mapa.appendChild(nodo_longitud)


        raiz.appendChild(nodo_mapa)

        with open('../ArchivosXML/Mapas.xhtml', 'w') as f:
            doc.writexml(f, addindent=' ', encoding='utf-8')

def getMapa(nombreBuscar):#Funcion para buscar el mapa en xml devuelve directorio
    doc = minidom.parse("../ArchivosXML/Mapas.xhtml")
    mapas = doc.getElementsByTagName("mapa")
    Directorio = ""
    for mapa in mapas:
        nombre = mapa.getElementsByTagName("nombre")[0].firstChild.data
        if nombre == nombreBuscar:
            Directorio  = mapa.getElementsByTagName("directorioMapa")[0].firstChild.data
            return Directorio

def compruebaNombreMapa(nombreBuscar): #Funcion que comprueba si el mapa ya fue introducido
    doc = minidom.parse("../ArchivosXML/Mapas.xhtml")
    mapas = doc.getElementsByTagName("mapa")
    Encontrado = False
    for mapa in mapas:
        nombre = mapa.getElementsByTagName("nombre")[0].firstChild.data
        if nombre == nombreBuscar:
            Encontrado = True
    return Encontrado

def getTodosMapas(): #Funcion que añade todos los mapa a la lista [nombre,directorio,latitud,longitud]
    from VariablesGlobales.VarGlo import ListaMapas
    ListaMapas.clear()
    ListaMapas.append(["Seleccione mapa existente"])
    doc = minidom.parse("../ArchivosXML/Mapas.xhtml")
    mapas = doc.getElementsByTagName("mapa")
    for mapa in mapas:
        nombre = mapa.getElementsByTagName("nombre")[0].firstChild.data
        directorio = mapa.getElementsByTagName("directorioMapa")[0].firstChild.data
        latitud = mapa.getElementsByTagName("LatitudIni")[0].firstChild.data
        longitud = mapa.getElementsByTagName("LongitudIni")[0].firstChild.data
        ListaMapas.append([nombre,directorio,latitud,longitud])

def obtieneDirectrorio(nombreBuscar):
    doc = minidom.parse("../ArchivosXML/Mapas.xhtml")
    mapas = doc.getElementsByTagName("mapa")
    Directorio = ""
    for mapa in mapas:
        nombre = mapa.getElementsByTagName("nombre")[0].firstChild.data
        if nombre == nombreBuscar:
            Directorio = mapa.getElementsByTagName("directorioMapa")[0].firstChild.data
            return Directorio

def getLatitudLongitud(nombreBuscar):
    doc = minidom.parse("../ArchivosXML/Mapas.xhtml")
    mapas = doc.getElementsByTagName("mapa")
    ListaPuntos=[]
    for mapa in mapas:
        nombre = mapa.getElementsByTagName("nombre")[0].firstChild.data
        if nombre == nombreBuscar:
            Lat = mapa.getElementsByTagName("LatitudIni")[0].firstChild.data
            Long = mapa.getElementsByTagName("LongitudIni")[0].firstChild.data
            ListaPuntos.append([Lat,Long])
            return ListaPuntos

def eliminaMapa(nombre):
    doc = parse("../ArchivosXML/Mapas.xhtml")
    Mapas = doc.getElementsByTagName("mapa")
    for mapa in Mapas:
        nombreAux = mapa.getElementsByTagName("nombre")[0].firstChild.data

        if nombreAux == nombre:
         mapa.parentNode.removeChild(mapa)

    with open('../ArchivosXML/Mapas.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')



#FUNCIONES PARAMETOS OPTIMIZADOR
def actualizaParamOptimizador(pso,itmax,itconv,frefesco):
    doc = parse("../ArchivosXML/ParametrosAplicacion.xhtml")
    raiz = doc.documentElement

    parametros = raiz.getElementsByTagName("optimizador")

    for parametro in parametros:
        pn = parametro.parentNode

        PSO = pn.getElementsByTagName("pso")[0]
        PSO.childNodes[0].data = pso

        it = pn.getElementsByTagName("itmax")[0]
        it.childNodes[0].data = itmax

        conv = pn.getElementsByTagName("itconv")[0]
        conv.childNodes[0].data = itconv

        refresco = pn.getElementsByTagName("frefresco")[0]
        refresco.childNodes[0].data = frefesco



    with open('../ArchivosXML/ParametrosAplicacion.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

def getParametrosOptimizador():
    from VariablesGlobales.VarGlo import ListaParametrosOptimizador
    ListaParametrosOptimizador.clear()
    doc = minidom.parse("../ArchivosXML/ParametrosAplicacion.xhtml")
    mapas = doc.getElementsByTagName("optimizador")
    for mapa in mapas:
        pso = mapa.getElementsByTagName("pso")[0].firstChild.data
        itmax = mapa.getElementsByTagName("itmax")[0].firstChild.data
        itconv = mapa.getElementsByTagName("itconv")[0].firstChild.data
        frefresco = mapa.getElementsByTagName("frefresco")[0].firstChild.data
        ListaParametrosOptimizador.append([pso, itmax, itconv, frefresco])


#FUNCIONES POLIGONOS CACHE

def BuscaPoligonos():
    from VariablesGlobales.VarGlo import ListaPoligonosCache
    ListaPoligonosCache.clear()
    doc = minidom.parse("../ArchivosXML/PoligonosCache.xhtml")
    Poligonos = doc.getElementsByTagName("Poligono")
    if len(Poligonos) > 0:
        for Poligono in Poligonos:
            ListaStr = Poligono.getElementsByTagName("ListaPuntos")[0].firstChild.data
            ListaPuntos = ListaStr.split(",") # lat;lon
            ListaAux1 = []
            for Punto in ListaPuntos:
                listaAux = Punto.split(";")
                latA = listaAux[0].replace("[","")
                longA = listaAux[1].replace("]","")
                lat = latA.replace("'","")
                long = longA.replace("'","")
                tuplaAux = (float(lat),float(long))
                ListaAux1.append(tuplaAux)
            ListaPoligonosCache.append(ListaAux1)



def BuscaCirculos():
    from VariablesGlobales.VarGlo import ListaCirculosCache
    ListaCirculosCache.clear()
    doc = minidom.parse("../ArchivosXML/PoligonosCache.xhtml")
    Circulos = doc.getElementsByTagName("Circulo")
    if len(Circulos) > 0:
        for Circulo in Circulos:
            ListaStr = Circulo.getElementsByTagName("Parametros")[0].firstChild.data
            Lista1 = ListaStr.replace("[","")
            Lista2 = Lista1.replace("]","")
            Lista = Lista2.split(",")
            ListaCirculosCache.append(Lista)

def BuscaMaker():
    from VariablesGlobales.VarGlo import ListaMakerCache
    ListaMakerCache.clear()
    doc = minidom.parse("../ArchivosXML/PoligonosCache.xhtml")
    Makers = doc.getElementsByTagName("Maker")
    if len(Makers) > 0:
        for Maker in Makers:
            ListaStr = Maker.getElementsByTagName("Posicion")[0].firstChild.data
            Lista1 = ListaStr.replace("[", "")
            Lista2 = Lista1.replace("]", "")
            Lista = Lista2.split(",")
            id = Maker.getElementsByTagName("id")[0].firstChild.data
            Lista.append(id)
            ListaMakerCache.append(Lista)

def InsertaCirculoCache(Lista):
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    raiz = doc.documentElement

    nodo_circulo = doc.createElement("Circulo")

    nodo_param = doc.createElement("Parametros")
    valor_nodo_param = doc.createTextNode(Lista)
    nodo_param.appendChild(valor_nodo_param)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_circulo.appendChild(nodo_param)


    raiz.appendChild(nodo_circulo)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

def InsertaPoligonoCache(Lista):
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    raiz = doc.documentElement

    nodo_poligono = doc.createElement("Poligono")

    nodo_param = doc.createElement("ListaPuntos")
    valor_nodo_param = doc.createTextNode(Lista)
    nodo_param.appendChild(valor_nodo_param)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_poligono.appendChild(nodo_param)

    raiz.appendChild(nodo_poligono)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')

def InsertaMakerCache(Lista,id):
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    raiz = doc.documentElement

    nodo_maker = doc.createElement("Maker")

    nodo_param = doc.createElement("Posicion")
    valor_nodo_param = doc.createTextNode(Lista)
    nodo_param.appendChild(valor_nodo_param)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_maker.appendChild(nodo_param)

    nodo_id = doc.createElement("id")
    valor_nodo_id = doc.createTextNode(str(id))
    nodo_id.appendChild(valor_nodo_id)  # Cuelgue el nodo de texto en el nodo name_node
    nodo_maker.appendChild(nodo_id)

    raiz.appendChild(nodo_maker)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')


def BorrarArchivosCache():
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    Circulos = doc.getElementsByTagName("Circulo")
    Poligonos = doc.getElementsByTagName("Poligono")
    Makers =  doc.getElementsByTagName("Maker")

    for circulo in Circulos:
        circulo.parentNode.removeChild(circulo)

    for poligono in Poligonos:
        poligono.parentNode.removeChild(poligono)


    for maker in Makers:
        maker.parentNode.removeChild(maker)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')


def BorrarPoligonosCache():
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    Circulos = doc.getElementsByTagName("Circulo")
    Poligonos = doc.getElementsByTagName("Poligono")

    for circulo in Circulos:
        circulo.parentNode.removeChild(circulo)

    for poligono in Poligonos:
        poligono.parentNode.removeChild(poligono)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')


def eliminaMaher(id):
    doc = parse("../ArchivosXML/PoligonosCache.xhtml")
    Makers = doc.getElementsByTagName("Maker")
    for maker in Makers:
        idAux = maker.getElementsByTagName("id")[0].firstChild.data

        if idAux == id:
         maker.parentNode.removeChild(maker)

    with open('../ArchivosXML/PoligonosCache.xhtml', 'w') as f:
        doc.writexml(f, addindent=' ', encoding='utf-8')


def obtieneNumeroRegiones():
    lista = []
    doc = minidom.parse("../ArchivosXML/PoligonosCache.xhtml")
    Circulos = doc.getElementsByTagName("Circulo")
    Poligonos = doc.getElementsByTagName("Poligono")
    lista.append([len(Circulos), len(Poligonos)])
    return lista

def ReseteaArchivosXML():

    BorrarArchivosCache()

    actualizaParamOptimizador("-", "-", "-", "-")

    docMapas = parse("../ArchivosXML/Mapas.xhtml")
    mapas = docMapas.getElementsByTagName("mapa")

    for mapa in mapas:
        mapa.parentNode.removeChild(mapa)
    with open('../ArchivosXML/Mapas.xhtml', 'w') as f:
        docMapas.writexml(f, addindent=' ', encoding='utf-8')

    docCamaras = parse("../ArchivosXML/ModelosCamaras.xhtml")
    camaras = docMapas.getElementsByTagName("camara")
    modelos = docCamaras.getElementsByTagName("modelo")

    for camara in camaras:
        camara.parentNode.removeChild(camara)

    with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
        docMapas.writexml(f, addindent=' ', encoding='utf-8')

    for modelo in modelos:
        modelo.parentNode.removeChild(modelo)

    with open('../ArchivosXML/ModelosCamaras.xhtml', 'w') as f:
        docMapas.writexml(f, addindent=' ', encoding='utf-8')

    docArchivos = parse("../ArchivosXML/ArchivosAplicacion.xhtml")

    archivos = docArchivos.getElementsByTagName("archivo")

    for archivo in archivos:

        archivo.parentNode.removeChild(archivo)
    with open('../ArchivosXML/ArchivosAplicacion.xhtml', 'w') as f:
        docMapas.writexml(f, addindent=' ', encoding='utf-8')




def PopUpCamara(id):
    modelo = getModeloID(id)
    Posicion = []
    from ArchivosXML.FuncionesXML import leeModelosCamaras
    from VariablesGlobales.VarGlo import ListaModelosCamaras
    leeModelosCamaras()
    nombreModelo = ""
    visionAcimutal = ""
    inclinacion = ""
    radioMax = ""
    radioMin = ""
    for i in range(len(ListaModelosCamaras)):

        if ListaModelosCamaras[i][0] == modelo:

            nombreModelo = ListaModelosCamaras[i][0]
            visionAcimutal = ListaModelosCamaras[i][1]
            inclinacion = ListaModelosCamaras[i][2]
            radioMax = ListaModelosCamaras[i][3]
            radioMin = ListaModelosCamaras[i][4]
            numeroUnidades = ListaModelosCamaras[i][5]

        i = i + 1

    Posicion = getPocionCamaraID(id)

    Latitud = Posicion[0]
    Longitud = Posicion [1]


    Texto = "Latitud: " + Posicion[0] + " Longitud: " + Posicion [1] + " \n Modelo: " + nombreModelo + " Vision Acimutal: " + visionAcimutal + " \n Inclinación: " +inclinacion + " Radio Máximo: " + radioMax + " \n Radio Mínimo: " + radioMin


    return Texto






















