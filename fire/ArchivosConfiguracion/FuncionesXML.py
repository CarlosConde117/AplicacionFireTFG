from xml.dom import minidom

from xml.dom.minidom import parse

#VARIABLES OPTIMIZADOR
Cantidad = 0
Altura = 0
RadioMaximo = 0
RadioMinimo = 0
azimutal = 0
inclinacion = 0
y0 = 0
y1 = 0
x0 = 0
x1 = 0
rutaDEM = ""
rutaWeight = ""
rutaSHP = ""
frecuenciaOPT = 0
numeroPSO = 0
LimiteConvergencia = 0
iteracionesMax = 0

listaNombres = ["cantidad", "altura","radioMax","radioMin","azimutal","inclinacion","y0","y1","x0","y1","rutaDem","rutaWeight","rutaSHP","frecuencia","numeroPSO","limiteConv","iteracionesMax"]

projectPath1 =  r'C:/Users/Carlos/Desktop/AplicacionTGF/fire'
def generacionConfigOpt():
    ruta = projectPath1 + '/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml'
    doc = minidom.parse(ruta)

    parametrosOPT = doc.getElementsByTagName("optimizador")

    for parametro in parametrosOPT:
        global Cantidad
        Cantidad = int(parametro.getElementsByTagName("cantidad")[0].firstChild.data)

        global Altura
        Altura = float(parametro.getElementsByTagName("altura")[0].firstChild.data)

        global RadioMinimo
        RadioMinimo = float(parametro.getElementsByTagName("radioMin")[0].firstChild.data)

        global RadioMaximo
        RadioMaximo = float(parametro.getElementsByTagName("radioMax")[0].firstChild.data)

        global azimutal
        azimutal = float(parametro.getElementsByTagName("azimutal")[0].firstChild.data)

        global inclinacion
        inclinacion = float(parametro.getElementsByTagName("inclinacion")[0].firstChild.data)

        global y0
        y0 = float(parametro.getElementsByTagName("y0")[0].firstChild.data)

        global y1
        y1 = float(parametro.getElementsByTagName("y1")[0].firstChild.data)

        global x0
        x0 = float(parametro.getElementsByTagName("x0")[0].firstChild.data)

        global x1
        x1 = float(parametro.getElementsByTagName("x1")[0].firstChild.data)

        global rutaDEM
        rutaDEM = parametro.getElementsByTagName("rutaDem")[0].firstChild.data

        global rutaWeight
        rutaWeight = parametro.getElementsByTagName("rutaWeight")[0].firstChild.data

        global rutaSHP
        rutaSHP = parametro.getElementsByTagName("rutaSHP")[0].firstChild.data

        global frecuenciaOPT
        frecuenciaOPT = int(parametro.getElementsByTagName("frecuencia")[0].firstChild.data)

        global numeroPSO
        numeroPSO = int(parametro.getElementsByTagName("numeroPSO")[0].firstChild.data)

        global LimiteConvergencia
        LimiteConvergencia = int(parametro.getElementsByTagName("limiteConv")[0].firstChild.data)

        global iteracionesMax
        iteracionesMax = int(parametro.getElementsByTagName("iteracionesMax")[0].firstChild.data)



def escribeParametroOpt(nombre,valor):
    doc = parse("../fire/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml")
    raiz = doc.documentElement

    parametros = raiz.getElementsByTagName("optimizador")

    for parametro in parametros:
       # rutaDEM = parametro.getElementsByTagName("rutaDem")[0].firstChild.data

        pn = parametro.parentNode

        paramam = pn.getElementsByTagName(nombre)[0]
        paramam.childNodes[0].data = valor

        with open('../fire/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml', 'w') as f:
            doc.writexml(f, addindent=' ', encoding='utf-8')
        break

def getUnParametro(nombre):
    ruta = projectPath1 + '/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml'
    doc = minidom.parse(ruta)

    parametrosOPT = doc.getElementsByTagName("optimizador")

    for parametro in parametrosOPT:
        Result = parametro.getElementsByTagName(nombre)[0].firstChild.data
        break

    return Result

def eliminaParametrosConfig():
    ruta = projectPath1 + '/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml'
    doc = minidom.parse(ruta)

    parametrosOPT = doc.getElementsByTagName("optimizador")
    ValorReset = 0
    for parametro in parametrosOPT:
        for nombre in listaNombres:
            if nombre != "y0" or nombre != "y1" or nombre != "x0" or nombre != "x1":
                pn = parametro.parentNode

                paramam = pn.getElementsByTagName(nombre)[0]
                paramam.childNodes[0].data = ValorReset

                with open('../fire/ArchivosConfiguracion/ConfiguracionAlgoritmo.xhtml', 'w') as f:
                    doc.writexml(f, addindent=' ', encoding='utf-8')
                break










