import os
import shutil
import subprocess
import threading
import time

import numpy as np
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QWidget, QDialog, QMainWindow, QMessageBox, QLCDNumber, QSlider, QSpinBox, QLabel, \
    QLineEdit, QPushButton
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWebEngineWidgets import *
from PySide2.QtCore import QUrl, Qt, QThread, QTimer, QThread
import folium
import Logica.FuncionesMapa
import VariablesGlobales.VarGlo
import random
import matplotlib.animation as animation

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt

import threading
import time

#import tkinter

# from tkinter import Tk, messagebox


from ArchivosXML.FuncionesXML import obtieneDirectrorio
from VariablesGlobales import *

from Views.Aplicacion import Ui_MainWindow
# from tkinter.filedialog import askopenfilename
from threading import Thread
import glob

# VARIABLES GLOBALES
latitud = 0
longitud = 0
nombre = ""
mapa = None

primeraVez = True

# VARIABLES GLOBALES PESATAÑA CAMARA
nombreModelo = ""
radioMax = 0
radioMin = 0
visionAcimutal = 0
inclinacion = 0
numeroUnidades = 0
id = 0

modeloSeleccionado = ""

# VARIABLES GLOBALES ARCHIVOS
directorioArchivoDEM = ""
directorioArchivoPuntuacion = ""
directorioArchivoShape = ""

# VARIABLES GLOBALES PESTAÑA OPTIMIZADOR
numeroParticulasPSO = 0
numeroIteracionesMax = 0
numeroIteracionesConv = 0
frecuenciaRefresco = 0

parametrosOpOK = False

demHistorico = False
shapeHistorico = False
weightHistorico = False

PuntosRestantesPoligono = 3

# VARIABLE MAPA CARGADO
MapaCargado = False

# Variable autogenerarPosiciones actuales
AutogenerarPosiciones = False

# Variable para saber en que indice del tab estamos
IndiceTab = 0


# VARIABLES GRÁFICA


class Canvas_grafica(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1,dpi= 100 ,facecolor='gray', )
        super().__init__(self.fig)
        self.fig.suptitle('Gráfica convergencia', size = 10)

        from VariablesGlobales.VarGlo import finLecturaLog, listaPuntos, puntosY, puntosX
        dataY =[0.7587608950084597, 0.7385880059715619, 0.7096615950646099, 0.7081496231052369, 0.7059811370056099, 0.683719339340631, 0.6660531406574306, 0.6645212743301712, 0.6641631757082144, 0.6640040207651224, 0.6592293724723657, 0.6495607096795329, 0.6484267307100032, 0.6376439833155273, 0.6223850031465918, 0.5937172190221642, 0.590195915906256, 0.5897383454448668, 0.5880672185424018, 0.5844265492191748, 0.5806864080565153, 0.5794529572475531, 0.5789754924182774, 0.5784582388532287]
        dataX = [2, 3, 5, 16, 19, 23, 47, 54, 61, 64, 68, 76, 80, 83, 89, 101, 129, 270, 271, 352, 358, 360, 390, 527]
        self.ax.plot(dataX, dataY)

    def grarfica_datos(self):
        minimoY = 0
        maximoY = 1
        minimoX = 0
        maximoX = 100
        self.fig.suptitle = ('Grafica convergencia')
        from VariablesGlobales.VarGlo import finLecturaLog, listaPuntos, puntosY, puntosX
        dataY = puntosY
        dataX = puntosX
        self.ax.plot(dataX, dataY)


class Reader_txt(QThread):
    def __init__(self, ruta):
        super().__init__()
        self._ruta = ruta

        def lectura(self):
            f = open(ruta + r'\ArchivosXML\LogOptimizador.txt', "r+")
            lines = f.readlines()
            ultimaLinea = lines[len(lines) - 1]
            ultimaLinea.replace("\n", "")
            print(ultimaLinea)


class TheadClass(QtCore.QThread):

    def __init__(self, parent=None):
        super(TheadClass, self).__init__(parent)
        self.is_running = True

    def run(self):
        print("Start Hilo...")
        cnt = 0
        pass

    def stop(self):
        print("Fin hilo")
        self.terminate()


class Worker(QThread):
    def __init__(self):
        super().__init__()
        self.Isrunning = False

    def run(self):

        if self.Isrunning == False:
            self.Isrunning = True


        else:
            self.isRunning = False

class HiloAlgortimo(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass




class ListAplicacion(QMainWindow, Ui_MainWindow):
    def __init__(self):  # constructror ventana principal
        super().__init__()
        self.setupUi(self)

        self.hilo = TheadClass(parent=None)
        from threading import Thread
        self.hiloOpt = Thread(target=self.workerOptimizador)

        self.Temporizador = QTimer()

        self.bt_lanzarCalculadora.clicked.connect(self.inicioAl)

        self.appPath = r'C:\Users\Carlos\Desktop\AplicacionTGF'

        Directorio = ""
        Mapa = None
        Latitud = 0
        Longitud = 0

        LatitudMapa = 0
        LongitudMapa = 0

        from ArchivosXML.FuncionesXML import BorrarArchivosCache
        #        BorrarArchivosCache()

        # CONFIGURACION INICIAL TAB
        self.tab_MAIN.setCurrentIndex(0)
        self.gb_ResumenCalculadoraMain.setVisible(False)
        self.gb_ResumenMapasMain.setVisible(False)
        self.gb_ResumenCamarasMain.setVisible(False)
        self.tab_ResOp.setVisible(False)

        self.cambioValorSP()
        # DECLARACION PIXMAP
        self.pixOk = QPixmap("../Imagenes/ok.png")
        self.pixCancel = QPixmap("../Imagenes/cancel.png")
        self.iconEXP = QIcon("../Imagenes/file_explorer.png")
        self.warning = QPixmap("../Imagenes/warning.png")

        self.dibujaIcon = QIcon("../Imagenes/mapGreen.png")
        self.borraIcon = QIcon("../Imagenes/mapRed.png")

        # Configuracion Incial Widgets
        self.bt_confirmaDEM.setEnabled(True)
        # self.bt_exp_DEM.setEnabled(False)
        self.cb_dem.setEnabled(True)
        self.lb_estadoDEM.setPixmap(self.pixCancel)

        self.bt_confirmarShape.setEnabled(True)

        self.cb_shape.setEnabled(True)
        self.lb_estadoShape.setPixmap(self.pixCancel)

        self.bt_confirmarPuntuacion.setEnabled(True)

        self.cb_puntuacion.setEnabled(True)
        self.lb_estadoPuntuacion.setPixmap(self.pixCancel)

        self.tab_Optimizador.setEnabled(False)

        self.ln_particulasPSO.setEnabled(False)
        self.ln_itereacionesMax.setEnabled(False)
        self.ln_iteracionesConvergencia.setEnabled(False)
        self.ln_frecuenciaRefresco.setEnabled(False)

        self.gb_parametroOp.setCheckable(True)
        self.gb_circulo.setEnabled(False)

        self.bt_LnId.setEnabled(False)
        self.ln_IDEX.setEnabled(False)

        self.bt_clearPunt.setEnabled(False)
        self.bt_clearShape.setEnabled(False)
        self.bt_clearDem.setEnabled(False)

        self.lb_resultSup.setText("849,2 m2")
        self.lb_resultPunt.setText("21,23%")
        self.BarraProgresoCal.setValue(0)

        # Borramos archivos cache

        # self.borrarCahe()

        # Leemos el archivo XML donde se guardan los directorios

        from ArchivosXML.FuncionesXML import leeDatosModelosDEM, leeDatosModelosSHAPE, leeDatosModelosPUNT, \
            leeModelosCamaras, eliminarCamarasImplementadas, inicializaPosiciones, reseteaNumeroUnidades
        leeDatosModelosDEM()
        leeDatosModelosSHAPE()
        leeDatosModelosPUNT()
        leeModelosCamaras()
        eliminarCamarasImplementadas()  # Colocamos todas las camaras como no implementadas
        inicializaPosiciones()  # Reseteamos las posiciones de todas las camaras "-"
        reseteaNumeroUnidades()

        # Funcion para renellar los comboBox

        self.rellenarComboDEM()
        self.rellenarComboShape()
        self.rellenarComboPuntuaciones()
        self.rellenarComboCalculador()
        self.rellenarComboOptimizador()
        self.rellenarComboMapas()

        # Configuracion inical resumen

        self.rellenarCbResumenModelo()
        self.rellenacbResumenCamara()

        # DECLARACION MSGBOX

        self.mensaje = QMessageBox()
        self.mensaje.setWindowTitle("Error valores introducidos")
        self.mensaje.setIcon(QMessageBox.Critical)

        self.mensajeOk = QMessageBox()
        self.mensajeOk.setWindowTitle("Valores introducidos correctamente")
        self.mensajeOk.setIcon(QMessageBox.Information)

        # EVENTO TAB MAIN
        self.tab_MAIN.currentChanged.connect(self.cambioIndiceTab)

        # EVENTOS TAB DEM

        self.bt_exp_DEM.clicked.connect(self.CargaDEM)  # EVENTO BT EXP
        self.cb_dem.currentIndexChanged.connect(self.seleccionComboDEM)  # EVENTO COMBO
        self.bt_confirmaDEM.clicked.connect(self.seleccionarDEM)  # EVENTO CONFIRMAR
        # self.ln_nombreDEM.textChanged.connect(self.cambioTextoDEM) #EVENTO CAMBIO DE TEXTO NOMBRE
        self.bt_confirmaDEMHistorico.clicked.connect(self.seleccionarDEMHistorico)

        # EVENTOS TAB ARCHIVOS PUNTUACIONES
        self.bt_exp_WEIGH.clicked.connect(self.cargaPuntuacion)  # EVENTO BT EXP
        self.cb_puntuacion.currentIndexChanged.connect(self.seleccionacComboPuntuaciones)  # EVENTO COMBO
        self.bt_confirmarPuntuacion.clicked.connect(self.seleccionarPuntuaciones)  # EVENTO CONFIRMAR
        # self.ln_nombrePuntuacion.textChanged.connect(self.cambioTextoPuntuaciones)  # EVENTO CAMBIO DE TEXTO NOMBRE
        self.bt_confirmarPuntuacionHistorico.clicked.connect(self.seleccionarPUNTHistorico)

        # EVENTOS TAB ARCHIVOS SHAPE
        self.bt_exp_SHAPE.clicked.connect(self.cargaShape)  # EVENTO BT EXP
        self.cb_shape.currentIndexChanged.connect(self.seleccionacComboShape)  # EVENTO COMBO
        self.bt_confirmarShape.clicked.connect(self.seleccionarShape)  # EVENTO CONFIRMAR
        # self.ln_nombreShape.textChanged.connect(self.cambioTextoShape)  # EVENTO CAMBIO DE TEXTO NOMBRE
        self.bt_confirmarShapeHistorico.clicked.connect(self.seleccionarSHAPEHistorico)

        self.bt_confirmar.clicked.connect(self.comfirmarModeloExistente)

        # EVENTOS PESTAÑA CAMARAS

        self.slider_insertcamara.valueChanged.connect(self.selectorTipoCamara)  # EVENTO SLIDE
        self.bt_confirmarDatos.clicked.connect(self.confirmarNuevoModelo)  # EVENTO BOTON CAMARA NUEVA
        self.comb_modeloscamaras_2.currentIndexChanged.connect(self.selecionarModelo)  # EVENTO COMBO
        self.ck_autogerarID.stateChanged.connect(self.seleccionID)
        self.bt_LnId.clicked.connect(self.introducirIDManual)

        # EVENTO SELECCTOR OPTIMAZDOR/CALCULADORA
        self.slider_general.valueChanged.connect(self.seleccionarTipoAplicacion)  # EVENTO SLIDER GENERAL

        # EVENTOS PESTAÑA CALCULADOR
        self.cb_selecModeloPosicionarC.currentIndexChanged.connect(self.seleccionModeloCal)
        self.bt_posionarCamaraC.clicked.connect(self.confirmarPosicionCal)

        self.bt_EliminarC_0.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_1.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_2.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_3.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_4.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_5.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_6.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_7.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_8.clicked.connect(self.eliminarCamaraC)
        self.bt_EliminarC_9.clicked.connect(self.eliminarCamaraC)

        self.bt_dibujarC_0.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_1.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_2.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_3.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_4.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_5.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_6.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_7.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_8.clicked.connect(self.dibujarCamaraC)
        self.bt_dibujarC_9.clicked.connect(self.dibujarCamaraC)

        self.bt_linea0.clicked.connect(self.seleccionarLinea)
        self.bt_linea1.clicked.connect(self.seleccionarLinea)
        self.bt_linea2.clicked.connect(self.seleccionarLinea)
        self.bt_linea3.clicked.connect(self.seleccionarLinea)
        self.bt_linea4.clicked.connect(self.seleccionarLinea)
        self.bt_linea5.clicked.connect(self.seleccionarLinea)
        self.bt_linea6.clicked.connect(self.seleccionarLinea)
        self.bt_linea7.clicked.connect(self.seleccionarLinea)
        self.bt_linea8.clicked.connect(self.seleccionarLinea)
        self.bt_linea9.clicked.connect(self.seleccionarLinea)

        # EVENTOS PESTAÑA OPTIMIZADOR
        self.cb_modeloO.currentIndexChanged.connect(self.seleccionModeloOpt)
        self.bt_agregarCamOp.clicked.connect(self.agregarModeloTabla)

        self.bt_delete0.clicked.connect(self.limpiaListaO)
        self.bt_delete1.clicked.connect(self.limpiaListaO)
        self.bt_delete2.clicked.connect(self.limpiaListaO)
        self.bt_delete3.clicked.connect(self.limpiaListaO)
        self.bt_delete4.clicked.connect(self.limpiaListaO)
        self.bt_delete5.clicked.connect(self.limpiaListaO)
        self.bt_delete6.clicked.connect(self.limpiaListaO)
        self.bt_delete7.clicked.connect(self.limpiaListaO)

        self.bt_dibujarO_0.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_1.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_2.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_3.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_4.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_5.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_6.clicked.connect(self.dibujaCamaraO)
        self.bt_dibujarO_7.clicked.connect(self.dibujaCamaraO)

        self.bt_Op_linea0.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea1.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea2.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea3.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea4.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea5.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea6.clicked.connect(self.filaSeleccionaOp)
        self.bt_Op_linea7.clicked.connect(self.filaSeleccionaOp)

        self.ck_autoGenerarPosiconesO.stateChanged.connect(self.AutogeneraPosicionesIniciales)

        #self.bt_confirmarParamOp.clicked.connect(self.confirmarParametrosOpt)

        self.gb_parametroOp.clicked.connect(self.habilitaLnOp)

        # EVENTOS CARGAR ARCHIVOS
        self.bt_addDEM.clicked.connect(self.cargarDem)
        self.bt_quitDEM.clicked.connect(self.eliminaDem)

        self.bt_addShape.clicked.connect(self.cargaGlobalShape)
        self.bt_quitShape.clicked.connect(self.eliminaShape)

        self.bt_addWeight.clicked.connect(self.cargaPunt)
        self.bt_quitWeights.clicked.connect(self.eliminaPunt)

        # EVENTOS DIBUJAR

        self.bt_guardarzona.clicked.connect(self.guardarzona)

        self.bt_seleccionarposini.clicked.connect(self.MuestraMapa)

        self.bt_confirmarCirculo.clicked.connect(self.dibujaCirculo)

        self.slider_tipoPoligono.valueChanged.connect(self.seleccionaTipoPoligono)

        self.ck_habDibujo.stateChanged.connect(self.habilitaDibujo)

        ##self.ck_dibujarMapaPoligono.stateChanged.connect(self.dibujoMapaPoligono)
        ##self.ck_dibujarMapaCirculo.stateChanged.connect(self.dibujoMapaCirculo)

        self.combo_posiciones.currentIndexChanged.connect(self.cambioItemCombo)

        self.bt_clearCirculo.clicked.connect(self.borraMapa)

        self.sp_numeroPuntos.valueChanged.connect(self.cambioValorSP)

        self.bt_confirmarPuntoPoligono.clicked.connect(self.confirmarPuntoPoligono)

        self.bt_clearPoligono.clicked.connect(self.borraMapa)

        self.bt_clearResumenModelo.clicked.connect(self.eilimiarModelo)

        # Eventos resumen
        self.bt_clearResumenMapa.clicked.connect(self.eliminaMapa)
        self.cb_resumenMapas.currentIndexChanged.connect(self.cambioItemResumenMapas)
        self.bt_refreshResumen.clicked.connect(self.actualizaResumen)

        self.cb_resumenModelo.currentIndexChanged.connect(self.cambioSeleccionModelos)

        self.cb_resumenCamaras.currentIndexChanged.connect(self.cambioSeleecionCamara)

        self.bt_clearResumenCamara.clicked.connect(self.eliminarCamaras)

        # resetarAplicacion

        self.bt_restartApp.clicked.connect(self.resetarAplicacion)

        # EVENTOS ELIMINAR ARCHIVOS

        self.bt_clearDem.clicked.connect(self.eliminarDem)

        self.bt_clearPunt.clicked.connect(self.eliminarPunt)

        self.bt_clearShape.clicked.connect(self.eliminarShape)

        self.cb_eliminarDEM.currentIndexChanged.connect(self.cambioEstadoEliminarDem)
        self.cb_eliminarShape.currentIndexChanged.connect(self.cambioEstadoEliminarShape)
        self.cb_eliminarPunt.currentIndexChanged.connect(self.cambioEstadoEliminarPunt)
        #self.datacollector = threading.Thread(target=self.actualiza())

        self.bt_LanzarOptimizador.clicked.connect(self.leeUltimaLinea)
        self.bt_detenOpt.clicked.connect(self.muestraDatos)
        self.FinLectura = False

        self.ListaPuntos = []

        self.timer_run = threading.Event()
        self.timer_run.set()
        self.hiloTxt = threading.Thread(target= self.temporizador, args=(self.timer_run,))


    def closeEvent(self, event):
        """ Override the QWindow close event.
        Close all dialogs and database connection.
        If selected via menu option exit: event == False
        If selected via window x close: event == QtGui.QCloseEvent
        """

        reply = QMessageBox.question(self, 'Cerrar aplicación', '¿Esta seguro de que desea cerrar la aplicacion?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            directorioOrigen = directorio + '\\MapasCache\\*.html'
            files = glob.glob(directorioOrigen)

            for f in files:
                try:
                    os.remove(f)

                except:
                    pass

            event.accept()
            print('Window closed')

        else:
            event.ignore()

    # ALGORITMO
    def inicioAl(self):
        from Logica.FuncionesMapa import muestraTiff
        muestraTiff()
        qurl = "../Mapas/Prueba.html"
        self.widget_mapa.load(qurl)

    def finAl(self):
        self.tab_MAIN.setEnabled(True)
        del self.worker

    def lanzaAlgoritmo(self):
       pass

    def startThread(self):
        self.hiloOpt.start()

    # self.hilo = TheadClass(parent=None)
    # self.hilo.start()
    # self.leeUltimaLinea()
    def muestraDatos(self):
        self.lb_resultadoLat_0.setText("42.3887563")
        self.lb_resultadoLong_0.setText("-7.0328372")
        self.lb_resultadoLat_1.setText("42.3909444")
        self.lb_resultadoLong_1.setText("-7.0162566")
        self.lb_resultadoLat_2.setText("42.359004")
        self.lb_resultadoLong_2.setText("-7.0145961")
        self.lb_resultadoLat_3.setText("42.3646871")
        self.lb_resultadoLong_3.setText("-7.0527981")
        self.lb_resultadoLat_4.setText("42.3686515")
        self.lb_resultadoLong_4.setText("-7.0015984")
        self.lb_resultPuntOpt.setText("42.85 %")
        self.lb_resultPuntSupCubierta.setText("1714 m2")
    def stopThread(self):
        self.hilo.stop()

    def workerOptimizador(self):

        pass

    def lanzaAlgoritmo(self):
        pass

    # FUNCIONES GRAFICA

    def leeUltimaLinea(self):
        f = open(self.appPath + r'\ArchivosXML\LogOptimizador.txt', "r+")
        lines = f.readlines()
        ultimaLinea = lines[len(lines) - 1]
        Linea = ultimaLinea.replace("\n", "")
        puntos = Linea.split(";")

        if len(puntos) > 1:
            from VariablesGlobales.VarGlo import finLecturaLog, listaPuntos, puntosY, puntosX
            print(puntos)
            puntosX.clear()
            puntosY.clear()
            puntosY = puntos[0]
            puntosX = puntos[1]
            print(puntosY)
            print(puntosX)

            self.dibujaGrafica()
            finLecturaLog = False


            self.Temporizador.start(5000)
            self.Temporizador.singleShot(5000, self.leeUltimaLinea)


        else:
            from VariablesGlobales.VarGlo import finLecturaLog
            print(puntos)
            finLecturaLog = True
            self.Temporizador.stop()

            self.dibujaGrafica(self)

    def dibujaGrafica(self):
        global  primeraVez
        if primeraVez == True:
            primeraVez = False
            self.grafica = Canvas_grafica()
            #self.LayoutGrafica.replaceWidget(self.grafica,self.grafica)
            self.LayoutGrafica.addWidget(self.grafica)

        else:
            self.grafica = Canvas_grafica()
            graficaBorar = self.LayoutGrafica.findChildren(FigureCanvas)
            self.LayoutGrafica.removeWidget(graficaBorar)
            self.LayoutGrafica.addWidget(self.grafica)


    def temporizador(self, timer_run):

        while timer_run.is_set():
            self.leeUltimaLinea()
            time.sleep(10)



    # FUNCIONES TAB MAIN

    def cambioIndiceTab(self):
        global IndiceTab

        IndiceTab = int(self.tab_MAIN.currentIndex())

        if IndiceTab == 0:
            self.gb_ResumenCalculadoraMain.setVisible(False)
            self.gb_ResumenMapasMain.setVisible(False)
            self.gb_ResumenCamarasMain.setVisible(False)
            self.gb_EliminarArchivos.setVisible(True)
            self.tab_ResOp.setVisible(False)
        if IndiceTab == 1:
            self.gb_ResumenCalculadoraMain.setVisible(False)
            self.rellenarComboMapasResumen()
            self.gb_ResumenMapasMain.setVisible(True)
            self.gb_ResumenCamarasMain.setVisible(False)
            self.gb_EliminarArchivos.setVisible(False)
            self.tab_ResOp.setVisible(False)
        if IndiceTab == 2:
            self.gb_ResumenCalculadoraMain.setVisible(False)
            self.gb_ResumenMapasMain.setVisible(False)
            self.gb_ResumenCamarasMain.setVisible(False)
            self.gb_EliminarArchivos.setVisible(True)
            self.tab_ResOp.setVisible(False)
        if IndiceTab == 3:
            self.gb_ResumenCalculadoraMain.setVisible(False)
            self.gb_ResumenMapasMain.setVisible(False)
            self.gb_ResumenCamarasMain.setVisible(True)
            self.gb_EliminarArchivos.setVisible(False)
            self.tab_ResOp.setVisible(False)
        if IndiceTab == 4:
            self.gb_ResumenCalculadoraMain.setVisible(True)
            self.gb_ResumenMapasMain.setVisible(False)
            self.gb_ResumenCamarasMain.setVisible(False)
            self.gb_EliminarArchivos.setVisible(False)
            self.tab_ResOp.setVisible(False)
        if IndiceTab == 5:
            self.gb_ResumenCalculadoraMain.setVisible(False)
            self.gb_ResumenMapasMain.setVisible(False)
            self.gb_ResumenCamarasMain.setVisible(False)
            self.gb_EliminarArchivos.setVisible(False)
            self.tab_ResOp.setVisible(True)

    # FUNCIONES CARGAR ARCHIVOS

    def cargarDem(self):
        from VariablesGlobales.VarGlo import directorioDEM
        directorioDEM = self.lb_infoDEM.text()
        self.bt_quitDEM.setEnabled(True)
        self.bt_addDEM.setEnabled(False)
        self.estado_dem.setPixmap(self.pixOk)
        self.lb_estadoDEM.setPixmap(self.pixOk)
        self.bt_confirmaDEM.setEnabled(False)
        self.bt_confirmaDEMHistorico.setEnabled(False)

        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoDEM.text(), "DEM", "Cargado")

        from fire.ArchivosConfiguracion.FuncionesXML import escribeParametroOpt
        escribeParametroOpt("rutaDem", self.lb_infoDEM.text())

    def eliminaDem(self):
        from VariablesGlobales.VarGlo import directorioDEM
        directorioDEM = ""
        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoDEM.text(), "DEM", "NoCargado")
        self.lb_infoDEM.setText("Archivo no cargado")
        self.estado_dem.setPixmap(self.pixCancel)
        self.lb_estadoDEM.setPixmap(self.pixCancel)
        self.bt_quitDEM.setEnabled(False)
        self.bt_addDEM.setEnabled(False)
        self.bt_confirmaDEM.setEnabled(True)
        self.bt_confirmaDEMHistorico.setEnabled(True)

    def cargaGlobalShape(self):
        from VariablesGlobales.VarGlo import directorioShape
        directorioShape = self.lb_infoShape.text()
        self.bt_quitShape.setEnabled(True)
        self.bt_addShape.setEnabled(False)
        self.estado_shape.setPixmap(self.pixOk)
        self.lb_estadoShape.setPixmap(self.pixOk)
        self.bt_confirmarShape.setEnabled(False)
        self.bt_confirmarShapeHistorico.setEnabled(False)
        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoShape.text(), "SHAPE", "Cargado")

        from fire.ArchivosConfiguracion.FuncionesXML import escribeParametroOpt
        escribeParametroOpt("rutaSHP",self.lb_infoShape.text())


    def eliminaShape(self):
        from VariablesGlobales.VarGlo import directorioShape
        directorioShape = ""
        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoDEM.text(), "SHAPE", "NoCargado")
        self.lb_infoShape.setText("Archivo no cargado")
        self.estado_shape.setPixmap(self.pixCancel)
        self.lb_estadoShape.setPixmap(self.pixCancel)
        self.bt_quitShape.setEnabled(False)
        self.bt_addShape.setEnabled(False)
        self.bt_confirmarShape.setEnabled(True)
        self.bt_confirmarShapeHistorico.setEnabled(True)

    def cargaPunt(self):
        from VariablesGlobales.VarGlo import directorioWeight
        directorioWeight = self.lb_infoWeigh.text()
        self.bt_quitWeights.setEnabled(True)
        self.bt_addWeight.setEnabled(False)
        self.estado_weight.setPixmap(self.pixOk)
        self.lb_estadoPuntuacion.setPixmap(self.pixOk)
        self.bt_confirmarPuntuacion.setEnabled(False)
        self.bt_confirmarPuntuacionHistorico.setEnabled(False)
        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoWeigh.text(), "PUNT", "Cargado")


        from fire.ArchivosConfiguracion.FuncionesXML import escribeParametroOpt
        escribeParametroOpt("rutaWeight",self.lb_infoWeigh.text())


    def eliminaPunt(self):
        from VariablesGlobales.VarGlo import directorioWeight
        directorioWeight = ""
        from ArchivosXML.FuncionesXML import actualizaEstado
        actualizaEstado(self.lb_infoDEM.text(), "PUNT", "NoCargado")
        self.lb_infoWeigh.setText("Archivo no cargado")
        self.estado_weight.setPixmap(self.pixCancel)
        self.lb_estadoPuntuacion.setPixmap(self.pixCancel)
        self.bt_quitWeights.setEnabled(False)
        self.bt_addWeight.setEnabled(False)
        self.bt_confirmarPuntuacion.setEnabled(True)
        self.bt_confirmarPuntuacionHistorico.setEnabled(True)

    # FUNCIONES CAMARAS

    def limpiarCombo(self):
        self.cb_dem.clear()

    # FUNCIONES MAPA

    def rellenarComboMapas(self):
        from ArchivosXML.FuncionesXML import getTodosMapas
        getTodosMapas()
        from VariablesGlobales.VarGlo import ListaMapas
        self.combo_posiciones.clear()
        for i in range(len(ListaMapas)):
            nombre = ListaMapas[i][0]
            text = nombre
            self.combo_posiciones.addItem(text)
        for i in range(len(ListaMapas)):
            if self.combo_posiciones.currentText() != "Seleccione mapa existente":
                nombre = ListaMapas[i][0]
                latitud = ListaMapas[i][2]
                longitud = ListaMapas[i][3]
                if nombre == self.combo_posiciones.currentText():
                    self.lb_lat.setText(latitud)
                    self.lb_lat_2.setText(longitud)
            else:
                self.lb_lat.setText("-")
                self.lb_lat_2.setText("-")

    def cambioItemCombo(self):
        if self.combo_posiciones.currentText() != "Seleccione mapa existente":
            Lista = []
            from ArchivosXML.FuncionesXML import getLatitudLongitud
            Lista = getLatitudLongitud(self.combo_posiciones.currentText())
            self.lb_lat.setText(Lista[0][0])
            self.lb_lat_2.setText(Lista[0][1])
        else:
            self.lb_lat.setText("-")
            self.lb_lat_2.setText("-")

    def guardarzona(self):

        valorNombre = False
        valorLatitud = False
        valorLongitud = False

        if len(self.ln_nombrezona.text()) > 0:
            global nombre
            nombre = self.ln_nombrezona.text()
            valorNombre = True
        else:
            self.mensaje.setText("Nombre es un campo obligatorio")
            self.mensaje.exec_()

        if len(self.ln_latitudini.text()):

            try:
                global latitudMapa
                latitudMapa = float(self.ln_latitudini.text())
                valorLatitud = True

            except ValueError:
                self.mensaje.setText("Latitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Latitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(self.ln_longitudini.text()) > 0:
            try:
                global longitudMapa
                longitudMapa = float(self.ln_longitudini.text())
                valorLongitud = True

            except ValueError:
                self.mensaje.setText("Longitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Longitud es un campo obligatorio")
            self.mensaje.exec_()

        if valorLongitud == True and valorNombre == True and valorLatitud == True:  # Si los tres parametros fueron introducidos correctamente guardamos mapa
            from Logica.FuncionesMapa import cargarMapa
            from ArchivosXML.FuncionesXML import compruebaNombreMapa
            existeMapa = compruebaNombreMapa(nombre)

            if not existeMapa:
                cargarMapa(str(latitudMapa), str(longitudMapa), nombre)
                self.mensaje.setText("Mapa cargado correctamente")
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setFixedWidth(100)

                self.mensaje.exec_()


            else:
                self.mensaje.setText("El nombre de mapa ya fue introducido anteriormente")
                self.mensaje.exec_()

            self.rellenarComboMapas()

    def MuestraMapa(self):
        if self.combo_posiciones.currentText() != "Seleccione mapa existente":

            cadenaTexto = self.combo_posiciones.currentText()

            listaCadenas = cadenaTexto.split(sep='[')
            nombre = listaCadenas[0]

            from ArchivosXML.FuncionesXML import obtieneDirectrorio
            directorio = obtieneDirectrorio(nombre)

            dirAjustado = directorio.replace("\\", "/")

            dirCache = dirAjustado.replace("Mapas", "MapasCache")

            existeCache = os.path.exists(dirCache)

            if existeCache:
                url = "file:///" + dirCache
                qurl = QUrl(url)
            else:
                url = "file:///" + dirAjustado
                qurl = QUrl(url)

            self.widget_mapa.load(qurl)
            global MapaCargado
            MapaCargado = True
        else:
            # LANZAR MSG BOX DE ERROR
            pass

    def dibujaCirculo(self):
        valorOKlat = False
        valorOKlong = False
        valorOKradio = False
        latitudC = 0
        longitudC = 0
        radioC = 0

        latitudTx = self.ln_lat_puntoCentral.text()
        longitudTx = self.ln_long_puntoCentral.text()
        radioTx = self.ln_radioCirculo.text()

        if len(latitudTx) > 0:
            try:
                latitudC = float(latitudTx)
                valorOKlat = True
            except ValueError:
                valorOKlat = False
                self.mensaje.setText("Latitud debe ser un número")
                self.mensaje.exec_()
        else:
            valorOKlat = False
            self.mensaje.setText("Latitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(longitudTx) > 0:
            try:
                longitudC = float(longitudTx)
                valorOKlong = True
            except ValueError:
                valorOKlong = False
                self.mensaje.setText("Longitud debe ser un número")
                self.mensaje.exec_()
        else:
            valorOKlong = False
            self.mensaje.setText("Longitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(radioTx) > 0:
            try:
                radioC = float(radioTx)
                valorOKradio = True
            except ValueError:
                valorOKlong = False
                self.mensaje.setText("El radio debe ser un número")
                self.mensaje.exec_()
        else:
            valorOKradio = False
            self.mensaje.setText("Radio es un campo obligatorio")
            self.mensaje.exec_()

        if valorOKlat and valorOKlong and valorOKradio == True:
            cadenaTexto = self.combo_posiciones.currentText()

            listaCadenas = cadenaTexto.split(sep='[')
            nombre = listaCadenas[0]
            from Logica.FuncionesMapa import dibujaCirculo
            dibujaCirculo(latitudC, longitudC, nombre, radioC)

            from ArchivosXML.FuncionesXML import obtieneDirectrorio
            directorio = obtieneDirectrorio(nombre)

            dirAjustado = directorio.replace("\\", "/")

            dirCahe = dirAjustado.replace("Mapas", "MapasCache")

            url = "file:///" + dirCahe
            qurl = QUrl(url)
            self.widget_mapa.load(qurl)

            self.ln_lat_puntoCentral.setText("")
            self.ln_long_puntoCentral.setText("")
            self.ln_radioCirculo.setText("")

    def borraMapa(self):
        from ArchivosXML.FuncionesXML import obtieneDirectrorio
        from Logica.FuncionesMapa import PintaCamaraCache
        directorio = obtieneDirectrorio(self.combo_posiciones.currentText())

        directorioCache = directorio.replace("Mapas", "MapasCache")

        existeCache = os.path.exists(directorioCache)
        if existeCache == True:
            os.remove(directorioCache)

            cadenaTexto = self.combo_posiciones.currentText()

            listaCadenas = cadenaTexto.split(sep='[')
            nombre = listaCadenas[0]
            lat = float(self.lb_lat.text())
            long = float(self.lb_lat_2.text())

            PintaCamaraCache(lat, long, nombre);

        else:
            self.mensaje.setWindowTitle("ERROR: No existen regiones")
            self.mensaje.setText("No existen regiones a eliminar")
            self.mensaje.exec_()
        from ArchivosXML.FuncionesXML import BorrarPoligonosCache
        BorrarPoligonosCache()

        self.MuestraMapa()

    def habilitaDibujo(self):
        if bool(self.ck_habDibujo.checkState()):
            self.slider_tipoPoligono.setEnabled(True)
            self.seleccionaTipoPoligono()
            self.groupBox_5.setEnabled(False)
            self.gb_infoMapa.setEnabled(False)
            self.groupBox_7.setEnabled(False)

        else:
            self.groupBox_5.setEnabled(True)
            self.gb_infoMapa.setEnabled(True)
            self.groupBox_7.setEnabled(True)
            self.slider_tipoPoligono.setEnabled(False)
            self.gb_circulo.setEnabled(False)
            self.gb_poligono.setEnabled(False)

    def seleccionaTipoPoligono(self):
        if self.slider_tipoPoligono.value() == 100:
            self.gb_poligono.setEnabled(False)
            self.gb_circulo.setEnabled(True)
        else:
            self.gb_poligono.setEnabled(True)
            self.gb_circulo.setEnabled(False)

    def dibujoMapaCirculo(self):
        if bool(self.ck_habDibujo.checkState()) == True:
            self.ln_lat_puntoCentral.setEnabled(False)
            self.ln_long_puntoCentral.setEnabled(False)
            self.ln_radioCirculo.setEnabled(False)
            self.bt_confirmarCirculo.setEnabled(False)
        else:
            self.ln_lat_puntoCentral.setEnabled(True)
            self.ln_long_puntoCentral.setEnabled(True)
            self.ln_radioCirculo.setEnabled(True)
            self.bt_confirmarCirculo.setEnabled(True)

    def dibujoMapaPoligono(self):
        if bool(self.ck_dibujarMapaPoligono.checkState()) == True:
            self.ln_latPoligono.setEnabled(False)
            self.ln_longPoligono.setEnabled(False)
            self.sp_numeroPuntos.setEnabled(False)
            self.bt_confirmarPuntoPoligono.setEnabled(False)
        else:
            self.ln_latPoligono.setEnabled(True)
            self.ln_longPoligono.setEnabled(True)
            self.sp_numeroPuntos.setEnabled(True)
            self.bt_confirmarPuntoPoligono.setEnabled(True)

    def cambioValorSP(self):
        global PuntosRestantesPoligono
        PuntosRestantesPoligono = int(self.sp_numeroPuntos.text())
        self.lb_puntosRestantesPoligono.setText(str(PuntosRestantesPoligono))

    def confirmarPuntoPoligono(self):

        global PuntosRestantesPoligono

        self.sp_numeroPuntos.setEnabled(False)

        valorOKlat = False
        valorOKlong = False
        latitudC = 0
        longitudC = 0

        latitudTx = self.ln_latPoligono.text()
        longitudTx = self.ln_longPoligono.text()

        if len(latitudTx) > 0:
            try:
                latitudC = float(latitudTx)
                valorOKlat = True
            except ValueError:
                valorOKlat = False
                self.mensaje.setText("Latitud debe ser un número")
                self.mensaje.exec_()
        else:
            valorOKlat = False
            self.mensaje.setText("Latitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(longitudTx) > 0:
            try:
                longitudC = float(longitudTx)
                valorOKlong = True
            except ValueError:
                valorOKlong = False
                self.mensaje.setText("Longitud debe ser un número")
                self.mensaje.exec_()
        else:
            valorOKlong = False
            self.mensaje.setText("Longitud es un campo obligatorio")
            self.mensaje.exec_()

        if valorOKlat and valorOKlong == True:
            PuntosRestantesPoligono = PuntosRestantesPoligono - 1
            self.lb_puntosRestantesPoligono.setText(str(PuntosRestantesPoligono))
            self.ln_latPoligono.setText("")
            self.ln_longPoligono.setText("")
            # self.sp_numeroPuntos.setValue(int(PuntosRestantesPoligono))
            from VariablesGlobales.VarGlo import ListaPuntos
            ListaPuntos.append((float(latitudTx), float(longitudTx)))
            if PuntosRestantesPoligono == 0:
                # si ya se alcanzaron los puntos...
                cadenaTexto = self.combo_posiciones.currentText()
                self.lb_puntosRestantesPoligono.setText("0")

                listaCadenas = cadenaTexto.split(sep='[')
                nombre = listaCadenas[0]
                from VariablesGlobales.VarGlo import ListaPuntos
                from Logica.FuncionesMapa import dibujaPoligono
                dibujaPoligono(ListaPuntos, float(self.lb_lat.text()), float(self.lb_lat_2.text()), nombre)

                from ArchivosXML.FuncionesXML import obtieneDirectrorio
                directorio = obtieneDirectrorio(nombre)

                dirAjustado = directorio.replace("\\", "/")

                dirCahe = dirAjustado.replace("Mapas", "MapasCache")

                url = "file:///" + dirCahe
                qurl = QUrl(url)
                self.widget_mapa.load(qurl)
                self.ln_latPoligono.setText("")
                self.ln_longPoligono.setText("")

                self.sp_numeroPuntos.setEnabled(True)

    def pruebaDibujo(self):
        cadenaTexto = self.combo_posiciones.currentText()

        listaCadenas = cadenaTexto.split(sep='[')
        nombre = listaCadenas[0]
        Lista = [(42.16944431522199, -8.681882904695248), (42.1689601113165, -8.686040272481799),
                 (42.17146912776008, -8.686901441523299)]
        from Logica.FuncionesMapa import dibujaPoligono
        dibujaPoligono(Lista, float(self.lb_lat.text()), float(self.lb_lat_2.text()), "Cuvi")

        from ArchivosXML.FuncionesXML import obtieneDirectrorio
        directorio = obtieneDirectrorio(nombre)

        dirAjustado = directorio.replace("\\", "/")

        dirCahe = dirAjustado.replace("Mapas", "MapasCache")

        url = "file:///" + dirCahe
        qurl = QUrl(url)
        self.widget_mapa.load(qurl)
        self.ln_latPoligono.setText("")
        self.ln_longPoligono.setText("")

        self.sp_numeroPuntos.setEnabled(True)

    def dibujaCamara(self):
        pass

    # FUNCIONES COMBOBOX
    def comboSeleccionado(self):
        self.ln_DEM.setEnabled(False)

    # FUNCIONES CARGAR DEM

    def CargaDEM(self):
        # Tk().withdraw()
        # filename = askopenfilename()
        self.ln_nombreDEM.setEnabled(True)
        self.ln_DEM.setEnabled(True)

        if len(self.ln_nombreDEM.text()) > 0:

            if str("filename").endswith(".TIF"):
                self.ln_DEM.setText("filename")

                self.bt_confirmaDEM.setEnabled(True)

            else:
                self.mensaje.setText("Tipo de archivo erróneo")
                self.mensaje.exec_()

        else:
            self.mensaje.setText("Debe introducir un nombre")
            self.mensaje.exec_()

    def seleccionComboDEM(self):

        if self.cb_dem.currentText() == "Seleccione archivo":
            self.bt_exp_DEM.setEnabled(True)
            self.lb_estadoDEM.setPixmap(self.pixCancel)
            self.bt_confirmaDEMHistorico.setEnabled(False)


        else:
            self.bt_exp_DEM.setEnabled(False)
            self.lb_estadoDEM.setPixmap(self.pixCancel)
            self.bt_confirmaDEMHistorico.setEnabled(True)
            from ArchivosXML.FuncionesXML import leeDatosModelosDEM
            leeDatosModelosDEM()
            from VariablesGlobales.VarGlo import ListaArchivosDem
            for i in range(len(ListaArchivosDem)):
                if ListaArchivosDem[i][0] == self.cb_dem.currentText():
                    self.lb_dirDEMhistorico.setText(ListaArchivosDem[i][1])

    def seleccionarDEM(self):
        self.lb_infoDEM.setText(self.ln_DEM.text())
        self.bt_addDEM.setEnabled(True)
        from ArchivosXML.FuncionesXML import insertaModelo
        insertaModelo(self.ln_nombreDEM.text(), self.ln_DEM.text(), "DEM", "NoCargado")
        self.rellenarComboDEM()
        self.lb_estadoDEM.setPixmap(self.warning)
        # self.lb_estadoDEM.toolTip("Debe cargar el archivo en la aplicación")
        self.bt_confirmaDEM.setEnabled(False)

    def seleccionarDEMHistorico(self):
        self.lb_infoDEM.setText(self.lb_dirDEMhistorico.text())
        self.bt_addDEM.setEnabled(True)
        self.rellenarComboDEM()
        self.lb_estadoDEM.setPixmap(self.warning)

    def rellenarComboDEM(self):

        from ArchivosXML.FuncionesXML import leeDatosModelosDEM
        leeDatosModelosDEM()
        from VariablesGlobales.VarGlo import ListaArchivosDem
        self.cb_dem.clear()
        self.cb_eliminarDEM.clear()

        j = 0
        for j in range(len(ListaArchivosDem)):
            self.cb_dem.addItem(ListaArchivosDem[j][0])
            self.cb_eliminarDEM.addItem(ListaArchivosDem[j][0])
            j = j + 1

    # FUNCIONES PUNTUACION ZONAS

    def cargaPuntuacion(self):
        # Tk().withdraw()
        # filename = askopenfilename()
        self.ln_nombrePuntuacion.setEnabled(True)
        self.ln_puntuacion.setEnabled(True)

        if len(self.ln_nombrePuntuacion.text()) > 0:

            if str("filename").endswith(".TIF"):
                self.ln_puntuacion.setText("filename")

                self.bt_confirmarPuntuacion.setEnabled(True)

            else:
                self.mensaje.setText("Tipo de archivo erróneo")
                self.mensaje.exec_()

        else:
            self.mensaje.setText("Debe introducir un nombre")
            self.mensaje.exec_()

    def seleccionacComboPuntuaciones(self):

        if self.cb_puntuacion.currentText() == "Seleccione archivo":
            self.bt_exp_WEIGH.setEnabled(True)
            self.lb_estadoPuntuacion.setPixmap(self.pixCancel)
            self.bt_confirmarPuntuacionHistorico.setEnabled(False)


        else:
            self.bt_exp_WEIGH.setEnabled(False)
            self.lb_estadoPuntuacion.setPixmap(self.pixCancel)
            self.bt_confirmarPuntuacionHistorico.setEnabled(True)
            from ArchivosXML.FuncionesXML import leeDatosModelosPUNT
            leeDatosModelosPUNT()
            from VariablesGlobales.VarGlo import ListaArchivosPuntuaciones
            for i in range(len(ListaArchivosPuntuaciones)):
                if ListaArchivosPuntuaciones[i][0] == self.cb_puntuacion.currentText():
                    # self.ln_nombreDEM.setText(ListaArchivosDem[i][0])
                    self.lb_directorioWeightHist.setText(ListaArchivosPuntuaciones[i][1])

    def seleccionarPuntuaciones(self):
        self.lb_infoWeigh.setText(self.ln_puntuacion.text())
        self.bt_addWeight.setEnabled(True)
        from ArchivosXML.FuncionesXML import insertaModelo
        insertaModelo(self.ln_nombrePuntuacion.text(), self.ln_puntuacion.text(), "PUNT", "NoCargado")
        self.rellenarComboPuntuaciones()
        self.lb_estadoPuntuacion.setPixmap(self.warning)
        # self.lb_estadoPuntuacion.toolTip("Debe cargar el archivo en la aplicación")

    def rellenarComboPuntuaciones(self):
        from ArchivosXML.FuncionesXML import leeDatosModelosPUNT
        leeDatosModelosPUNT()

        from VariablesGlobales.VarGlo import ListaArchivosPuntuaciones
        self.cb_puntuacion.clear()
        self.cb_eliminarPunt.clear()

        j = 0
        for j in range(len(ListaArchivosPuntuaciones)):
            self.cb_puntuacion.addItem(ListaArchivosPuntuaciones[j][0])
            self.cb_eliminarPunt.addItem(ListaArchivosPuntuaciones[j][0])
            j = j + 1

    def seleccionarPUNTHistorico(self):
        self.lb_infoWeigh.setText(self.lb_directorioWeightHist.text())
        self.bt_addWeight.setEnabled(True)
        self.rellenarComboPuntuaciones()
        self.lb_estadoPuntuacion.setPixmap(self.warning)

    # FUNCIONES CARGAR SHAPE

    def cargaShape(self):
        # Tk().withdraw()
        # filename = askopenfilename()
        self.ln_nombreShape.setEnabled(True)
        self.ln_shape.setEnabled(True)

        if len(self.ln_nombreShape.text()) > 0:

            if str("filename").endswith(".shp"):
                self.ln_shape.setText("filename")

                self.bt_confirmarShape.setEnabled(True)

            else:
                self.mensaje.setText("Tipo de archivo erróneo")
                self.mensaje.exec_()

        else:
            self.mensaje.setText("Debe introducir un nombre")
            self.mensaje.exec_()

    def seleccionacComboShape(self):
        global shapeHistorico
        if self.cb_shape.currentText() == "Seleccione archivo":
            self.bt_exp_SHAPE.setEnabled(True)
            self.lb_estadoShape.setPixmap(self.pixCancel)
            self.bt_confirmarShapeHistorico.setEnabled(False)
        else:

            self.bt_exp_SHAPE.setEnabled(False)
            self.lb_estadoShape.setPixmap(self.pixCancel)
            self.bt_confirmarShapeHistorico.setEnabled(True)
            from ArchivosXML.FuncionesXML import leeDatosModelosSHAPE
            leeDatosModelosSHAPE()
            from VariablesGlobales.VarGlo import ListaArchivosShape
            for i in range(len(ListaArchivosShape)):
                if ListaArchivosShape[i][0] == self.cb_shape.currentText():
                    # self.ln_nombreDEM.setText(ListaArchivosDem[i][0])
                    self.lb_directorioShapeHist.setText(ListaArchivosShape[i][1])

    def seleccionarShape(self):
        self.lb_infoShape.setText(self.ln_shape.text())
        self.bt_addShape.setEnabled(True)
        from ArchivosXML.FuncionesXML import insertaModelo
        insertaModelo(self.ln_nombreShape.text(), self.ln_shape.text(), "SHAPE", "NoCargado")
        self.rellenarComboShape()
        self.lb_estadoShape.setPixmap(self.warning)
        # self.lb_estadoShape.toolTip("Debe cargar el archivo en la aplicación")

    def rellenarComboShape(self):
        from ArchivosXML.FuncionesXML import leeDatosModelosSHAPE
        leeDatosModelosSHAPE()

        from VariablesGlobales.VarGlo import ListaArchivosShape
        self.cb_shape.clear()
        self.cb_eliminarShape.clear()

        j = 0
        for j in range(len(ListaArchivosShape)):
            self.cb_shape.addItem(ListaArchivosShape[j][0])
            self.cb_eliminarShape.addItem(ListaArchivosShape[j][0])
            j = j + 1

    def seleccionarSHAPEHistorico(self):
        self.lb_infoShape.setText(self.lb_directorioShapeHist.text())
        self.bt_addShape.setEnabled(True)
        self.rellenarComboShape()
        self.lb_estadoShape.setPixmap(self.warning)

    # FUNCIONES CAMARAS
    def rellenarComboCamaras(self):
        from ArchivosXML.FuncionesXML import leeModelosCamaras
        leeModelosCamaras()
        from VariablesGlobales.VarGlo import ListaModelosCamaras
        self.comb_modeloscamaras_2.clear()
        j = 0
        for j in range(len(ListaModelosCamaras)):
            self.comb_modeloscamaras_2.addItem(ListaModelosCamaras[j][0])
            j = j + 1

    # FUNCIONES PESTAÑA CAMARAS

    def selectorTipoCamara(self):
        self.limpiarInputsCamaras()
        self.seleccionID()
        self.actualizaVariablesCamaras()
        if self.slider_insertcamara.value() == 0:
            self.ln_modeloCamara.setEnabled(True)
            self.ln_acimutal.setEnabled(True)
            self.ln_inclinacion.setEnabled(True)
            self.ln_radioMax.setEnabled(True)
            self.ln_radioMin.setEnabled(True)
            self.bt_confirmarDatos.setEnabled(True)
            self.ln_ID.setEnabled(True)

            self.comb_modeloscamaras_2.setEnabled(False)
            self.sp_numeroCamaras.setEnabled(False)
            self.bt_confirmar.setEnabled(False)
            self.ln_IDEX.setEnabled(False)
        else:

            self.ln_modeloCamara.setEnabled(False)
            self.ln_acimutal.setEnabled(False)
            self.ln_inclinacion.setEnabled(False)
            self.ln_radioMax.setEnabled(False)
            self.ln_radioMin.setEnabled(False)
            self.bt_confirmarDatos.setEnabled(False)
            self.ln_ID.setEnabled(False)

            self.comb_modeloscamaras_2.setEnabled(True)
            self.sp_numeroCamaras.setEnabled(True)
            self.bt_confirmar.setEnabled(True)
            self.ln_IDEX.setEnabled(True)
            self.rellenarComboCamaras()

    def confirmarNuevoModelo(self):
        # Comprobamos Line nombre modelo
        modeloOK = False
        radioMaxOK = False
        radioMinOK = False
        acimutalOk = False
        inclinacionOK = False
        idOk = False
        global numeroUnidades
        numeroUnidades = 0

        if len(self.ln_modeloCamara.text()) > 0:
            global nombreModelo
            nombreModelo = self.ln_modeloCamara.text()
            modeloOK = True
        else:
            self.mensaje.setText("Debe introducir el nombre del modelo")
            self.mensaje.exec_()
            modeloOK = False
        # Comprobamos Line radio max
        if len(self.ln_radioMax.text()) > 0:
            try:
                float(self.ln_radioMax.text())

                global radioMax

                radioMax = self.ln_radioMax.text()
                radioMaxOK = True

                # Colocar otro if para comprobar valor numerico introducido

            except ValueError:
                radioMaxOK = False
                self.mensaje.setText("Radio máximo debe ser un valor numérico")
                self.mensaje.exec_()
        else:
            radioMaxOK = False
            self.mensaje.setText("Debe introducir el radio máximo")
            self.mensaje.exec_()
        # Comprobamos Line radio min
        if len(self.ln_radioMin.text()) > 0:
            try:
                float(self.ln_radioMin.text())

                global radioMin

                radioMin = self.ln_radioMin.text()
                radioMinOK = True
                # Colocar otro if para comprobar valor numerico introducido

            except ValueError:
                radioMinOK = False
                self.mensaje.setText("Radio mínimo debe ser un valor numérico")
                self.mensaje.exec_()
        else:
            radioMinOK = False
            self.mensaje.setText("Debe introducir el radio mínimo")
            self.mensaje.exec_()

        # Comprobamos Line vision acimutal
        if len(self.ln_acimutal.text()) > 0:
            try:
                float(self.ln_acimutal.text())

                global visionAcimutal

                visionAcimutal = self.ln_acimutal.text()
                acimutalOk = True
                # Colocar otro if para comprobar valor numerico introducido

            except ValueError:
                acimutalOk = False
                self.mensaje.setText("Vision acimutal debe ser un valor numérico")
                self.mensaje.exec_()
        else:
            acimutalOk = False
            self.mensaje.setText("Debe introducir la vision acimutal")
            self.mensaje.exec_()

        # Comprobamos Line inclinacion
        if len(self.ln_inclinacion.text()) > 0:
            try:
                float(self.ln_inclinacion.text())

                global inclinacion
                inclinacionOK = True
                inclinacion = self.ln_inclinacion.text()

                # Colocar otro if para comprobar valor numerico introducido

            except ValueError:
                inclinacionOK = False
                self.mensaje.setText("Inclinación debe ser un valor numérico")
                self.mensaje.exec_()
        else:
            inclinacionOK = False
            self.mensaje.setText("Debe introducir la inclinación")
            self.mensaje.exec_()

        # Comprobamos Line ID
        global id
        if len(self.ln_ID.text()) > 0:
            from ArchivosXML.FuncionesXML import compruebaId
            if compruebaId(self.ln_ID.text()):
                self.mensaje.setText("ID ya introducido, introduzca otro valor")
                self.mensaje.exec_()
            else:

                idOk = True
                id = self.ln_inclinacion.text()

        else:
            if bool(self.ck_autogerarID.checkState()) == True:
                from ArchivosXML.FuncionesXML import compruebaId

                id = random.randint(0, 1000)
                if compruebaId(id):
                    id = random.randint(0, 1000)
                    self.ln_ID.setText(str(id))
                    idOk = True
                else:
                    self.ln_ID.setText(str(id))
                    idOk = True


            else:
                idOk = False
                self.mensaje.setText("Debe introducir un id, o marcar la opcion de generarlo automaticamente")
                self.mensaje.exec_()

        if inclinacionOK == True and acimutalOk == True and radioMinOK == True and radioMaxOK == True and modeloOK == True and idOk == True:
            # Tk().withdraw()
            #  confirmacion = messagebox.askokcancel(message="Valores introducidos correctamente ¿Añadir el nuevo modelo?",
            # title="Agregar nuevo modelo de camara")
            confirmacion = True
            if confirmacion == True:
                from ArchivosXML.FuncionesXML import insertaModeloCamara, insertaNuevaCamara
                insertaModeloCamara(nombreModelo, visionAcimutal, inclinacion, radioMax, radioMin)
                insertaNuevaCamara(str(id), nombreModelo, "-", "-")
                self.limpiarInputsCamaras()
                self.rellenarResumenCamara()
                self.rellenarComboCamaras()
                self.rellenarResumenCamara()
                self.rellenarCbResumenModelo()

    def rellenarResumenCamara(self):
        global nombreModelo
        global visionAcimutal
        global inclinacion
        global radioMax
        global radioMin
        global numeroUnidades

        self.lb_infomodelo.setText(nombreModelo)
        self.lb_infoacimutal.setText(str(visionAcimutal))
        self.lb_infoinclinacion.setText(str(inclinacion))
        self.lb_inforadiomax.setText(str(radioMax))
        self.lb_inforadiomin.setText(str(radioMin))
        self.lb_infonumerounidades.setText(str(numeroUnidades))

    def limpiarInputsCamaras(self):
        self.ln_modeloCamara.setText("")
        self.ln_acimutal.setText("")
        self.ln_inclinacion.setText("")
        self.ln_radioMax.setText("")
        self.ln_radioMin.setText("")

    def limpiarResumenCamaras(self):

        self.lb_infomodelo.setText("")
        self.lb_infoacimutal.setText("")
        self.lb_infoinclinacion.setText("")
        self.lb_inforadiomax.setText("")
        self.lb_inforadiomin.setText("")
        self.lb_infonumerounidades.setText("")

    def selecionarModelo(self):
        if self.comb_modeloscamaras_2.currentText() == "Seleccione camara existente":
            self.sp_numeroCamaras.setEnabled(False)
            self.limpiarResumenCamaras()
        else:
            self.sp_numeroCamaras.setEnabled(True)
            global modeloSeleccionado
            modeloSeleccionado = self.comb_modeloscamaras_2.currentText()
            self.actualizaVariablesCamaras()
            self.rellenarResumenCamara()

    def comfirmarModeloExistente(self):
        global numeroModelos
        global modeloSeleccionado

        from ArchivosXML.FuncionesXML import getNumeroUnidades, actualizaNumeroModelos, insertaNuevaCamara, compruebaId
        numeroAnterior = int(getNumeroUnidades(modeloSeleccionado))
        numeroModelos = int(self.sp_numeroCamaras.text()) + numeroAnterior

        # Tk().withdraw()
        # confirmacion = messagebox.askokcancel(
        # message="Desea añadir " + self.sp_numeroCamaras.text() + " unidades del modelo de camara: " + modeloSeleccionado,
        # title="Insertar cámara existente")
        confirmacion = True
        if confirmacion == True:
            actualizaNumeroModelos(modeloSeleccionado, str(numeroModelos))

            self.actualizaVariablesCamaras()
            self.sp_numeroCamaras.setEnabled(False)
            self.comb_modeloscamaras_2.setEnabled(False)
            self.ModeloSeleccionado = self.comb_modeloscamaras_2.currentText()
            self.NumeroIdRestantes = int(self.sp_numeroCamaras.text())

            # SECCION INSERTAR CAMARAS
            for i in range(int(self.sp_numeroCamaras.text())):
                if bool(self.ck_autogerarID.checkState()):
                    id = random.randint(0, 1000)
                    if compruebaId(str(id)):
                        id = random.randint(0, 1000)
                        insertaNuevaCamara(str(id), modeloSeleccionado, "-", "-")
                    else:
                        insertaNuevaCamara(str(id), modeloSeleccionado, "-", "-")
                    self.sp_numeroCamaras.setEnabled(True)

                else:
                    self.lb_idRestante.setText(self.sp_numeroCamaras.text())
                    self.bt_LnId.setEnabled(True)
                    self.bt_confirmar.setEnabled(True)
                    self.sp_numeroCamaras.setEnabled(True)
                    self.mensaje.setText("Debe introducir los Id manualmente o marcar la opcion de autogenerarlos")
                    # self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec_()

            self.comb_modeloscamaras_2.setEnabled(True)

            self.rellenarResumenCamara()

    def introducirIDManual(self):
        if len(self.ln_IDEX.text()) > 0:
            from ArchivosXML.FuncionesXML import insertaNuevaCamara, compruebaId
            if bool(compruebaId(self.ln_IDEX.text())) == False:
                insertaNuevaCamara(self.ln_IDEX.text(), self.comb_modeloscamaras_2.currentText(), "-", "-")
                numeroRestantes = int(self.lb_idRestante.text())
                numeroRestantes = numeroRestantes - 1
                self.lb_idRestante.setText(str(numeroRestantes))
                self.ln_IDEX.setText("")
                if numeroRestantes == 0:
                    self.mensaje.setText("Todos los id han sido introducidos correctamente")
                    self.mensaje.setIcon(QMessageBox.Information)
                    self.mensaje.exec_()
                    self.bt_confirmar.setEnabled(True)
                    self.bt_LnId.setEnabled(False)
            else:
                self.mensaje.setText("Id ya introducido anteriormente")
                self.mensaje.exec_()

        else:
            self.mensaje.setText("Debe introducir un ID")
            self.mensaje.exec_()

    def actualizaVariablesCamaras(self):
        from ArchivosXML.FuncionesXML import leeModelosCamaras
        from VariablesGlobales.VarGlo import ListaModelosCamaras
        leeModelosCamaras()
        for i in range(len(ListaModelosCamaras)):
            if ListaModelosCamaras[i][0] == modeloSeleccionado and modeloSeleccionado != "Seleccione modelo existente":
                global nombreModelo
                nombreModelo = ListaModelosCamaras[i][0]
                global visionAcimutal
                visionAcimutal = ListaModelosCamaras[i][1]
                global inclinacion
                inclinacion = ListaModelosCamaras[i][2]
                global radioMax
                radioMax = ListaModelosCamaras[i][3]
                global radioMin
                radioMin = ListaModelosCamaras[i][4]
                global numeroUnidades
                numeroUnidades = ListaModelosCamaras[i][5]
            i = i + 1

    def rellenarComboCamaras(self):
        from ArchivosXML.FuncionesXML import leeModelosCamaras
        leeModelosCamaras()
        from VariablesGlobales.VarGlo import ListaModelosCamaras
        self.comb_modeloscamaras_2.clear()
        j = 0
        for j in range(len(ListaModelosCamaras)):
            self.comb_modeloscamaras_2.addItem(ListaModelosCamaras[j][0])
            j = j + 1

    def seleccionID(self):
        if bool(self.ck_autogerarID.checkState()) == True:
            if self.slider_insertcamara.value() == 0:
                self.ln_ID.setEnabled(False)
            else:
                self.ln_IDEX.setVisible(False)
                self.label_44.setVisible(False)
                self.label_22.setVisible(False)
                self.lb_idRestante.setVisible(False)
                self.bt_LnId.setVisible(False)
        else:
            if self.slider_insertcamara.value() == 0:
                self.ln_ID.setEnabled(True)
            else:
                self.ln_IDEX.setVisible(True)
                self.label_44.setVisible(True)
                self.label_22.setVisible(True)
                self.lb_idRestante.setVisible(True)
                self.bt_LnId.setVisible(True)

    # FUNCION SELECTOR OPTIMIZADOR/CALCULADORA

    def seleccionarTipoAplicacion(self):
        if self.slider_general.value() == 100:
            self.tab_Optimizador.setEnabled(True)
            self.tab_Calculadora.setEnabled(False)
            self.tab_MAIN.setCurrentIndex(5)
            self.rellenarComboOptimizador()

        else:
            self.tab_Optimizador.setEnabled(False)
            self.tab_Calculadora.setEnabled(True)
            self.tab_MAIN.setCurrentIndex(4)
            self.rellenarComboCalculador()

    # FUNCIONES PESTAÑA CALCULADOR

    def rellenarComboCalculador(self):
        from ArchivosXML.FuncionesXML import leeModelosCamaras
        leeModelosCamaras()
        from VariablesGlobales.VarGlo import ListaModelosCamaras
        self.cb_selecModeloPosicionarC.clear()
        j = 0
        for j in range(len(ListaModelosCamaras)):
            self.cb_selecModeloPosicionarC.addItem(ListaModelosCamaras[j][0])
            j = j + 1

    def seleccionModeloCal(self):
        if self.cb_selecModeloPosicionarC.currentText() == "Seleccione modelo existente":
            self.ln_longitudCamaraC.setEnabled(False)
            self.ln_latitudCamaraC.setEnabled(False)
            self.lb_modeloseleccionadoC.setText("-")
            # self.bt_camaraMapaC.setEnabled(False)
        else:
            self.ln_longitudCamaraC.setEnabled(True)
            self.ln_latitudCamaraC.setEnabled(True)
            self.lb_modeloseleccionadoC.setText(self.cb_selecModeloPosicionarC.currentText())
            from ArchivosXML.FuncionesXML import getNumeroUnidades
            numeroUnidades = getNumeroUnidades(self.cb_selecModeloPosicionarC.currentText())
            self.lb_numeroUnidadesC.setText(numeroUnidades)

    def confirmarPosicionCal(self):
        LatOk = False
        LongOk = False
        if len(self.ln_latitudCamaraC.text()):

            try:
                global latitudCamaraC
                latitudCamaraC = float(self.ln_latitudCamaraC.text())
                LatOk = True
            except ValueError:
                self.mensaje.setText("Latitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Latitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(self.ln_longitudCamaraC.text()) > 0:
            try:
                global longitudCamaraC
                longitudCamaraC = float(self.ln_longitudCamaraC.text())
                LongOk = True
            except ValueError:
                self.mensaje.setText("Longitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Longitud es un campo obligatorio")
            self.mensaje.exec_()

        if self.cb_selecModeloPosicionarC.currentText() != "Seleccione modelo existente":

            if LongOk == True and LatOk == True:
                # Tk().withdraw()
                # confirmacion = messagebox.askokcancel(
                #  message="Desea posicionar el modelo de camara: " + self.lb_modeloseleccionadoC.text() + " ?",
                #  title="PosicionarCamara")

                confirmacion = True
                if confirmacion == True:
                    self.cargaModeloLista()
                    self.ln_latitudCamaraC.setText("")
                    self.ln_longitudCamaraC.setText("")
                    from ArchivosXML.FuncionesXML import eliminaunaunidad, getNumeroUnidades
                    eliminaunaunidad(self.lb_modeloseleccionadoC.text())
                    unidades = getNumeroUnidades(self.lb_modeloseleccionadoC.text())
                    self.lb_numeroUnidadesC.setText(str(unidades))



        else:
            self.mensaje.setText("Debe seleccionar un modelo de camra")
            self.mensaje.exec_()

    def getFilaLibreC(self):  # Conseguimos la fila libre que este mas alta
        NumeroMin = 1000
        for Label in self.gb_listaCamarasC.findChildren(QLabel):
            NombreEtiqueta = Label.objectName()
            TextoEtiqueta = Label.text()

            if NombreEtiqueta.startswith("lb_modelo") and TextoEtiqueta == "-":
                NumeroEtiquetaModelo = NombreEtiqueta[-1]
                if int(NumeroEtiquetaModelo) <= int(NumeroMin):
                    NumeroMin = NumeroEtiquetaModelo

        return NumeroMin

    def cargaModeloLista(self):  # Actualizamos los campos de la lisata
        NumeroLibre = self.getFilaLibreC()
        if int(self.lb_numeroUnidadesC.text()) > 0:
            Id = ""
            Lat = self.ln_latitudCamaraC.text()
            Long = self.ln_longitudCamaraC.text()

            for Label in self.gb_listaCamarasC.findChildren(QLabel):
                NombreEtiqueta = Label.objectName()
                TextoEtiqueta = Label.text()

                if NombreEtiqueta == "lb_modelo" + str(NumeroLibre):  # Cargamos nombre modelo en la lista
                    Label.setText(self.lb_modeloseleccionadoC.text())

                if NombreEtiqueta == "lb_prueba" + str(NumeroLibre):  # Cargamos posicion en la lista
                    texto = "[" + self.ln_latitudCamaraC.text() + "," + self.ln_longitudCamaraC.text() + "]"
                    Label.setText(texto)

                if NombreEtiqueta == "lb_id" + str(NumeroLibre):  # Cargamos id en la lista
                    from ArchivosXML.FuncionesXML import seleccionaUnaCamara
                    id = seleccionaUnaCamara(self.cb_selecModeloPosicionarC.currentText())
                    Id = id
                    Label.setText(id)

                # Colocar un if para que una vez inserte todos los parametros salga de la funcion
            for Boton in self.gb_listaCamarasC.findChildren(QPushButton):
                NombreBoton = Boton.objectName()
                if NombreBoton == "bt_dibujarC_" + str(NumeroLibre) or NombreBoton == "bt_EliminarC_" + str(
                        NumeroLibre):
                    Boton.setEnabled(True)
            from ArchivosXML.FuncionesXML import actualizaEstadoCamara
            actualizaEstadoCamara(id, True)
            from ArchivosXML.FuncionesXML import actualizaPosicionCamara
            actualizaPosicionCamara(id, Lat, Long)
        else:
            self.mensaje.setText("Numero de unidades insuficientes,seleccione otro modelo o agregue mas unidades")
            self.mensaje.exec_()

    def dibujarCamaraC(self):
        boton = self.sender().objectName()
        NumeroBoton = boton[-1]
        global MapaCargado

        if MapaCargado:
            for Label in self.gb_listaCamarasC.findChildren(QLabel):
                NombreEtiqueta = Label.objectName()
                NumeroEtiqueta = NombreEtiqueta[-1]

                if NombreEtiqueta == "lb_id" + str(NumeroBoton):
                    idSeleccionado = Label.text()

            for Label in self.gb_listaCamarasC.findChildren(QLabel):
                NombreEtiqueta = Label.objectName()
                NumeroEtiqueta = NombreEtiqueta[-1]

                if NombreEtiqueta == "lb_prueba" + str(NumeroBoton):
                    self.lb_lat.text()
                    textoEtiqueta = Label.text()
                    cadena1 = textoEtiqueta.replace("[", "")
                    cadena2 = cadena1.replace("]", "")
                    ListaCadenas = cadena2.split(sep=',')
                    Latitud = float(ListaCadenas[0])
                    Longitud = float(ListaCadenas[1])
                    nombre = self.combo_posiciones.currentText()

                    from Logica.FuncionesMapa import PintaCamara
                    PintaCamara(Latitud, Longitud, nombre,
                                idSeleccionado)  # A ESTA FUNCION PASERLE EL ID DE LA CAMARA PARA PODER BORRARLA

                    from ArchivosXML.FuncionesXML import obtieneDirectrorio
                    directorio = obtieneDirectrorio(nombre)

                    dirAjustado = directorio.replace("\\", "/")

                    dirCahe = dirAjustado.replace("Mapas", "MapasCache")

                    url = "file:///" + dirCahe
                    qurl = QUrl(url)
                    self.widget_mapa.load(qurl)
                    # self.cambiaPixBt(NumeroBoton)
        else:
            self.mensaje.setText("Debe cargar un mapa")
            self.mensaje.exec_()

    def eliminarCamaraC(self):
        boton = self.sender().objectName()
        NumeroBoton = boton[-1]

        for Label in self.gb_listaCamarasC.findChildren(QLabel):
            NombreEtiqueta = Label.objectName()
            NumeroEtiquetaBorrar = NombreEtiqueta[-1]

            etiquetaLista = NombreEtiqueta.startswith("lb_id")
            modeloLista = NombreEtiqueta.startswith("lb_modelo")
            posicionLista = NombreEtiqueta.startswith("lb_prueba")
            superficieLista = NombreEtiqueta.startswith("lb_superficie")
            puntuacionLista = NombreEtiqueta.startswith("lb_puntuacion")

            if NombreEtiqueta == "lb_id" + str(NumeroBoton):
                id = Label.text()

                for Label in self.gb_listaCamarasC.findChildren(QLabel):
                    NombreEtiqueta = Label.objectName()
                    NumeroEtiqueta = NombreEtiqueta[-1]

                    if NombreEtiqueta == "lb_prueba" + str(NumeroBoton):
                        self.lb_lat.text()
                        textoEtiqueta = Label.text()
                        cadena1 = textoEtiqueta.replace("[", "")
                        cadena2 = cadena1.replace("]", "")
                        ListaCadenas = cadena2.split(sep=',')
                        Latitud = float(ListaCadenas[0])
                        Longitud = float(ListaCadenas[1])
                        nombre = self.combo_posiciones.currentText()

                        from Logica.FuncionesMapa import eliminaCamara
                        eliminaCamara(Latitud, Longitud, nombre,
                                      id)  # A ESTA FUNCION PASERLE EL ID DE LA CAMARA PARA PODER BORRARLA

                        from ArchivosXML.FuncionesXML import obtieneDirectrorio, añadeunaunidad, getModeloID
                        modelo = getModeloID(id)
                        añadeunaunidad(modelo)
                        directorio = obtieneDirectrorio(nombre)

                        dirAjustado = directorio.replace("\\", "/")

                        dirCahe = dirAjustado.replace("Mapas", "MapasCache")

                        url = "file:///" + dirCahe
                        qurl = QUrl(url)
                        self.widget_mapa.load(qurl)
                        break
                        # self.cambiaPixBt(NumeroBoton)
                from ArchivosXML.FuncionesXML import actualizaEstadoCamara, actualizaPosicionCamara
                actualizaEstadoCamara(id, False)
                actualizaPosicionCamara(id, "-", "-")
                Label.setText("-")

            if modeloLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    # Sumar un numero a unidades libres ModeloSeleciconado
                    Label.setText('-')
            if posicionLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    Label.setText('-')
            if superficieLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    Label.setText('-')
            if puntuacionLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    Label.setText('-')

        for Boton in self.gb_listaCamarasC.findChildren(QPushButton):
            NombreBoton = Boton.objectName()
            if NombreBoton == "bt_dibujarC_" + str(NumeroBoton) or NombreBoton == "bt_EliminarC_" + str(NumeroBoton):
                Boton.setEnabled(False)

    def seleccionarLinea(self):
        boton = self.sender().objectName()
        NumeroBoton = boton[-1]

        for Label in self.gb_listaCamarasC.findChildren(QLabel):
            NombreEtiqueta = Label.objectName()
            NumeroEtiqueta = NombreEtiqueta[-1]

            if NumeroEtiqueta == NumeroBoton:
                Label.setAutoFillBackground(True)

                if NombreEtiqueta.startswith("lb_id"):
                    self.lb_idModificarPos.setText(Label.text())

            else:
                Label.setAutoFillBackground(False)

    # FUNCIONES PESTAÑA OPTIMIZADOR

    def rellenarComboOptimizador(self):
        from ArchivosXML.FuncionesXML import leeModelosCamaras
        leeModelosCamaras()
        from VariablesGlobales.VarGlo import ListaModelosCamaras
        self.cb_modeloO.clear()
        j = 0
        for j in range(len(ListaModelosCamaras)):
            self.cb_modeloO.addItem(ListaModelosCamaras[j][0])
            j = j + 1

    def seleccionModeloOpt(self):
        if self.cb_modeloO.currentText() == "Seleccione modelo existente":
            self.ln_latitudCamaraO.setEnabled(False)
            self.ln_longitudCamaraO.setEnabled(False)
            self.lb_modeloseleccionadoO.setText("")

            self.bt_agregarCamOp.setEnabled(False)
            # ETIQUETA NUMERO DE UNIDADAES
        else:
            self.ln_latitudCamaraO.setEnabled(True)
            self.ln_longitudCamaraO.setEnabled(True)
            self.lb_infomodeloOp.setText(self.cb_modeloO.currentText())

            self.bt_agregarCamOp.setEnabled(True)
            from ArchivosXML.FuncionesXML import getNumeroUnidades
            numeroUnidades = getNumeroUnidades(self.cb_modeloO.currentText())
            self.lb_unidadesOp.setText(numeroUnidades)

    def confirmarPosicionOpt(self):
        LatOk = False
        LongOk = False
        if len(self.ln_latitudCamaraO.text()) > 0:

            try:
                global latitudCamaraC
                latitudCamaraC = float(self.ln_latitudCamaraO.text())
                LatOk = True
            except ValueError:
                self.mensaje.setText("Latitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Latitud es un campo obligatorio")
            self.mensaje.exec_()

        if len(self.ln_longitudCamaraO.text()) > 0:
            try:
                global longitudCamaraC
                longitudCamaraC = float(self.lb_modeloseleccionadoO.text())
                LongOk = True
            except ValueError:
                self.mensaje.setText("Longitud debe ser un número")
                self.mensaje.exec_()
        else:
            self.mensaje.setText("Longitud es un campo obligatorio")
            self.mensaje.exec_()

        if LongOk == True and LatOk == True:
            # Tk().withdraw()
            # confirmacion = messagebox.askokcancel(
            # message="Desea insertar el modelo de camara: " + self.lb_modeloseleccionadoC.text() + " ?",
            # title="Insertar Camara")
            confirmacion = True
            if confirmacion == True:
                return True
                # Lanzar funcion rellenaTabla

    def agregarModeloTabla(self):

        self.cargaModeloListaOpt()

        if self.cb_modeloO.currentText() != "Seleccione modelo existente":
            from ArchivosXML.FuncionesXML import getParametroCam
            from fire.ArchivosConfiguracion.FuncionesXML import escribeParametroOpt

            radioMin = getParametroCam(self.cb_modeloO.currentText(),"radioMin")
            escribeParametroOpt("radioMin", radioMin)

            radioMax = getParametroCam(self.cb_modeloO.currentText(), "radioMax")
            escribeParametroOpt("radioMax", radioMax)

            inclina = getParametroCam(self.cb_modeloO.currentText(), "inclinacion")
            escribeParametroOpt("inclinacion", inclina)

            azi = getParametroCam(self.cb_modeloO.currentText(), "visionAcimutal")
            escribeParametroOpt("azimutal", azi)

    def getFilaLibreO(self):  # Conseguimos la fila libre que este mas alta
        NumeroMin = 1000
        for Label in self.gb_listaCamarasO.findChildren(
                QLabel):  # =============Cambiar el nombre de este group box ===============
            NombreEtiqueta = Label.objectName()
            TextoEtiqueta = Label.text()

            if NombreEtiqueta.startswith("lb_modeloOp") and TextoEtiqueta == "-":
                NumeroEtiquetaModelo = NombreEtiqueta[-1]

                if int(NumeroEtiquetaModelo) <= int(NumeroMin):
                    NumeroMin = NumeroEtiquetaModelo

                    return NumeroMin

    def cargaModeloListaOpt(self):  # Actualizamos los campos de la lisata
        NumeroLibre = self.getFilaLibreO()
        global AutogenerarPosiciones
        if self.cb_modeloO.currentText() != "Seleccione modelo existente":

            if bool(self.ck_autoGenerarPosiconesO.checkState()) == False:
                # Comprobamos lat y long si ck esta a false
                LatOk = False
                LongOk = False
                if len(self.ln_latitudCamaraO.text()) > 0:

                    try:
                        global latitudCamaraC
                        latitudCamaraC = float(self.ln_latitudCamaraO.text())
                        LatOk = True
                        self.ln_latitudCamaraO.setText("")
                    except ValueError:
                        self.mensaje.setText("Latitud debe ser un número")
                        self.mensaje.exec_()
                else:
                    self.mensaje.setText("Latitud es un campo obligatorio")
                    self.mensaje.exec_()

                if len(self.ln_longitudCamaraO.text()) > 0:
                    try:
                        global longitudCamaraC
                        longitudCamaraC = float(self.ln_longitudCamaraO.text())
                        LongOk = True
                        self.ln_longitudCamaraO.setText("")
                    except ValueError:
                        self.mensaje.setText("Longitud debe ser un número")
                        self.mensaje.exec_()
                else:
                    self.mensaje.setText("Longitud es un campo obligatorio")
                    self.mensaje.exec_()

                if LongOk == True and LatOk == True:
                    # Tk().withdraw()
                    #  confirmacion = messagebox.askokcancel(
                    #   message="Desea insertar el modelo de camara: " + self.lb_infomodeloOp.text() + " ?",
                    #  title="Insertar Camara")
                    confirmacion = True
                    if confirmacion == True:
                        # La misma funcion que en el else pero modificando posicion camara
                        if int(self.lb_unidadesOp.text()) > 0:
                            from ArchivosXML.FuncionesXML import seleccionaUnaCamara, actualizaNumeroModelos
                            actualizaNumeroModelos(self.cb_modeloO.currentText(), self.lb_unidadesOp.text())
                            id = seleccionaUnaCamara(self.cb_modeloO.currentText())
                            for Label in self.gb_listaCamarasO.findChildren(QLabel):
                                NombreEtiqueta = Label.objectName()
                                TextoEtiqueta = Label.text()

                                if NombreEtiqueta == "lb_modeloOp" + str(
                                        NumeroLibre):  # Cargamos nombre modelo en la lista
                                    Label.setText(self.cb_modeloO.currentText())

                                if NombreEtiqueta == "lb_idOp" + str(NumeroLibre):  # Cargamos posicion en la lista
                                    texto = str(id)
                                    Label.setText(texto)
                                # Colocar un if para que una vez inserte todos los parametros salga de la funcion
                            for Boton in self.gb_listaCamarasO.findChildren(QPushButton):
                                NombreBoton = Boton.objectName()
                                if NombreBoton == "bt_dibujarO_" + str(NumeroLibre):
                                    if AutogenerarPosiciones == False:
                                        Boton.setEnabled(True)

                            numeroAnterior = int(self.lb_unidadesOp.text())
                            numeroSiguiente = numeroAnterior - 1
                            self.lb_unidadesOp.setText(str(numeroSiguiente))

                            from ArchivosXML.FuncionesXML import actualizaPosicionCamara, actualizaEstadoCamara
                            actualizaPosicionCamara(id, latitudCamaraC, longitudCamaraC)

                        else:
                            # Mensaje camaras insufcientes
                            pass



            else:
                if int(self.lb_unidadesOp.text()) > 0:
                    from ArchivosXML.FuncionesXML import seleccionaUnaCamara, actualizaEstadoCamara, \
                        actualizaNumeroModelos, eliminaunaunidad
                    id = seleccionaUnaCamara(self.cb_modeloO.currentText())
                    actualizaEstadoCamara(id, True)
                    actualizaNumeroModelos(self.cb_modeloO.currentText(), self.lb_unidadesOp.text())
                    eliminaunaunidad(self.cb_modeloO.currentText())
                    for Label in self.gb_listaCamarasO.findChildren(QLabel):
                        NombreEtiqueta = Label.objectName()
                        TextoEtiqueta = Label.text()

                        if NombreEtiqueta == "lb_modeloOp" + str(NumeroLibre):  # Cargamos nombre modelo en la lista
                            Label.setText(self.cb_modeloO.currentText())

                        if NombreEtiqueta == "lb_idOp" + str(NumeroLibre):  # Cargamos posicion en la lista
                            texto = str(id)
                            Label.setText(texto)
                        # Colocar un if para que una vez inserte todos los parametros salga de la funcion
                    for Boton in self.gb_listaCamarasO.findChildren(QPushButton):
                        NombreBoton = Boton.objectName()
                        if NombreBoton == "bt_dibujarO_" + str(NumeroLibre):
                            if AutogenerarPosiciones == False:
                                Boton.setEnabled(True)

                    numeroAnterior = int(self.lb_unidadesOp.text())
                    numeroSiguiente = numeroAnterior - 1
                    self.lb_unidadesOp.setText(str(numeroSiguiente))

                else:
                    self.mensaje.setText(
                        "Numero de unidades insuficientes,seleccione otro modelo o agregue mas unidades")
                    self.mensaje.exec_()
        else:
            self.mensaje.setText("Seleccione un modelo")
            self.mensaje.exec_()

    def limpiaListaO(self):
        boton = self.sender().objectName()
        NumeroBoton = boton[-1]
        global AutogenerarPosiciones

        for Label in self.gb_listaCamarasO.findChildren(QLabel):
            NombreEtiqueta = Label.objectName()
            NumeroEtiquetaBorrar = NombreEtiqueta[-1]

            etiquetaLista = NombreEtiqueta.startswith("lb_idOp")
            modeloLista = NombreEtiqueta.startswith("lb_modeloOp")

            if etiquetaLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    id = Label.text()
                    from ArchivosXML.FuncionesXML import actualizaEstadoCamara, eliminaunaunidad, getModeloID, \
                        getPocionCamaraID, obtieneDirectrorio, actualizaPosicionCamara
                    modelo = getModeloID(id)
                    eliminaunaunidad(modelo)
                    actualizaEstadoCamara(id, False)
                    if bool(self.ck_autoGenerarPosiconesO.checkState()) == False:
                        ListaPosiciones = getPocionCamaraID(id)
                        if len(ListaPosiciones) > 0:
                            Latitud = ListaPosiciones[0]
                            Longitud = ListaPosiciones[1]
                            nombre = self.combo_posiciones.currentText()
                            from Logica.FuncionesMapa import eliminaCamara
                            eliminaCamara(Latitud, Longitud, nombre, id)
                            actualizaPosicionCamara(id, "-", "-")
                            actualizaEstadoCamara(id, False)

                            directorio = obtieneDirectrorio(nombre)

                            dirAjustado = directorio.replace("\\", "/")

                            dirCahe = dirAjustado.replace("Mapas", "MapasCache")

                            url = "file:///" + dirCahe
                            qurl = QUrl(url)
                            self.widget_mapa.load(qurl)
                    else:
                        actualizaEstadoCamara(id, False)

                    Label.setText('-')
            if modeloLista:
                if int(NumeroEtiquetaBorrar) == int(NumeroBoton):
                    # Sumar un numero a unidades libres ModeloSeleciconado,Num
                    from ArchivosXML.FuncionesXML import añadeunaunidad, getNumeroUnidades
                    modelo = Label.text()
                    añadeunaunidad(modelo)
                    numeroSiguiente = getNumeroUnidades(modelo)

                    self.lb_unidadesOp.setText(str(numeroSiguiente))
                    Label.setText('-')
        for Boton in self.gb_listaCamarasO.findChildren(QPushButton):
            NombreBoton = Boton.objectName()
            if NombreBoton == "bt_dibujarO_" + str(NumeroBoton) and AutogenerarPosiciones == False:
                Boton.setEnabled(False)


    def habilitaLnOp(self):

        for ln in self.gb_parametroOp.findChildren(QLineEdit):
            ln.setEnabled(True)

    def dibujaCamaraO(self):
        boton = self.sender().objectName()
        NumeroBoton = boton[-1]
        global MapaCargado
        self.bt_addDEM.setChecked(True)

        if MapaCargado:
            for Label in self.gb_listaCamarasO.findChildren(QLabel):
                NombreEtiqueta = Label.objectName()
                NumeroEtiqueta = NombreEtiqueta[-1]

                if NombreEtiqueta == "lb_idOp" + str(NumeroBoton):
                    id = Label.text()
                    from ArchivosXML.FuncionesXML import getPocionCamaraID
                    ListaCoord = getPocionCamaraID(id)

                    Latitud = float(ListaCoord[0])
                    Longitud = float(ListaCoord[1])
                    nombre = self.combo_posiciones.currentText()

                    from Logica.FuncionesMapa import PintaCamara
                    PintaCamara(Latitud, Longitud, nombre, id)

                    from ArchivosXML.FuncionesXML import obtieneDirectrorio
                    directorio = obtieneDirectrorio(nombre)

                    dirAjustado = directorio.replace("\\", "/")

                    dirCahe = dirAjustado.replace("Mapas", "MapasCache")

                    url = "file:///" + dirCahe
                    qurl = QUrl(url)
                    self.widget_mapa.load(qurl)
        else:
            self.mensaje.setText("Debe cargar un mapa")
            self.mensaje.exec_()

    def filaSeleccionaOp(self):

        boton = self.sender().objectName()
        NumeroBoton = boton[-1]

        for Label in self.gb_listaCamarasO.findChildren(QLabel):
            NombreEtiqueta = Label.objectName()
            NumeroEtiqueta = NombreEtiqueta[-1]

            if NumeroEtiqueta == NumeroBoton:
                Label.setAutoFillBackground(True)

                if NombreEtiqueta.startswith("lb_id"):
                    id = Label.text()

                    if id != "-":
                        from ArchivosXML.FuncionesXML import getPocionCamaraID, getModeloID, getNumeroUnidades

                        ListaCoord = getPocionCamaraID(id)

                        lat = ListaCoord[0]
                        long = ListaCoord[1]
                        modelo = getModeloID(id)
                        Unidades = getNumeroUnidades(modelo)

                        self.lb_infoLatOpt.setText(lat)
                        self.lb_infoLongOp.setText(long)

                        self.lb_infomodeloOp.setText(modelo)
                        self.lb_unidadesOp.setText(Unidades)



            else:
                Label.setAutoFillBackground(False)

    def AutogeneraPosicionesIniciales(self):
        global AutogenerarPosiciones

        if bool(self.ck_autoGenerarPosiconesO.checkState()) == True:
            AutogenerarPosiciones = True
            self.ln_latitudCamaraO.setEnabled(False)
            self.ln_longitudCamaraO.setEnabled(False)
        else:
            AutogenerarPosiciones = False
            self.ln_latitudCamaraO.setEnabled(True)
            self.ln_longitudCamaraO.setEnabled(True)

    # Borrar archivos cache al lanzar aplicacion

    def borrarCahe(self):
        directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        directorioBorrar = directorio + "\\MapasCahe\\*.html"

        dirAjustado = directorioBorrar.replace("\\", "/")

        os.remove(dirAjustado)

    # FUNCIONES AUXILIARES

    def cambiaPixBt(self, numero):

        for boton in self.gb_listaCamarasC.findChildren(QPushButton):
            NombreBoton = boton.objectName()
            Icono = boton.icon()
            self.bt_seleccionarposini.icon.name()
            if NombreBoton == "bt_dibujarC_" + str(numero):
                if Icono == self.dibujaIcon:
                    boton.setIcon(self.borraIcon)

                else:
                    boton.setIcon(self.dibujaIcon)

    # FUNCIONES RESUMEN

    def eliminaMapa(self):
        from ArchivosXML.FuncionesXML import eliminaMapa

        if self.cb_resumenMapas.currentText() != "Seleccione mapa existente":
            self.lb_resumenNombreMapa.setText(self.cb_resumenMapas.currentText())

            confirmacion = True
            if confirmacion == True:
                eliminaMapa(self.cb_resumenMapas.currentText())

                self.mensaje.setText("Mapa eliminado")

                self.mensaje.exec_()

                self.cb_resumenMapas.setCurrentIndex(0)

                self.rellenarComboMapas()

        else:
            self.mensaje.setText("Debe seleccionar un mapa")
            self.mensaje.exec_()

        self.rellenarComboMapasResumen()
        pass

    def rellenarComboMapasResumen(self):
        from ArchivosXML.FuncionesXML import getTodosMapas
        getTodosMapas()
        from VariablesGlobales.VarGlo import ListaMapas
        self.cb_resumenMapas.clear()
        for i in range(len(ListaMapas)):
            nombre = ListaMapas[i][0]
            text = nombre
            self.cb_resumenMapas.addItem(text)

    def cambioItemResumenMapas(self):
        if self.cb_resumenMapas.currentText() != "Seleccione mapa existente":

            texto = self.cb_resumenMapas.currentText()

            self.lb_resumenNombreMapa.setText(texto)
        else:
            self.lb_resumenNombreMapa.setText("-")

    def actualizaResumen(self):
        from ArchivosXML.FuncionesXML import obtieneNumeroRegiones

        listas = obtieneNumeroRegiones()
        for lista in listas:
            numeroCirculos = lista[0]
            numeroPoligono = lista[1]
            numeroTotal = numeroCirculos + numeroPoligono

        self.lb_numeroPoligonosResumen.setText(str(numeroPoligono))
        self.lb_numeroCirculosResumen.setText(str(numeroCirculos))
        self.lb_numeroRegionesResumen.setText(str(numeroTotal))

    def rellenarCbResumenModelo(self):
        from ArchivosXML.FuncionesXML import getTodosModelos

        ListaAux = getTodosModelos()

        for i in range(len(ListaAux)):
            self.cb_resumenModelo.addItem(ListaAux[i])

    def cambioSeleccionModelos(self):
        from ArchivosXML.FuncionesXML import getNumeroUnidades

        if self.cb_resumenModelo.currentText() != "Seleccione modelo existente":
            numeroUni = getNumeroUnidades(self.cb_resumenModelo.currentText())
            self.lb_resumenNumeroModelo.setText(str(numeroUni))
            self.lb_resumenNombreModelo.setText(self.cb_resumenModelo.currentText())

        else:
            self.lb_resumenNombreModelo.setText("-")
            self.lb_resumenNumeroModelo.setText("-")

    def eilimiarModelo(self):

        from ArchivosXML.FuncionesXML import eliminaModeloCamara
        confirmacion = True

        if confirmacion == True:
            eliminaModeloCamara(self.cb_resumenModelo.currentText())

            self.mensaje.setText("Modelo " + self.cb_resumenModelo.currentText() + " fue eliminado")
            self.mensaje.exec_()

            self.cb_resumenModelo.setCurrentIndex(0)
            self.lb_resumenNombreModelo.setText("-")
            self.lb_resumenNumeroModelo.setText("-")
            self.rellenarResumenCamara()
            self.rellenarComboCamaras()
            self.rellenarComboCalculador()
            self.rellenarComboOptimizador()
            self.rellenacbResumenCamara()

    def rellenacbResumenCamara(self):
        from ArchivosXML.FuncionesXML import getTodosModelos

        ListaAux = getTodosModelos()

        for i in range(len(ListaAux)):
            self.cb_resumenCamaras.addItem(ListaAux[i])

    def cambioSeleecionCamara(self):
        from ArchivosXML.FuncionesXML import getNumeroUnidades, getUnidadesImplemntadas, getNumeroTotalUnidades

        if self.cb_resumenCamaras.currentText() != "Seleccione modelo existente":
            self.bt_clearResumenCamara.setEnabled(True)
            numeroTotal = getNumeroTotalUnidades(self.cb_resumenCamaras.currentText())
            self.lb_resumenNumeroCamarasTotal.setText(str(numeroTotal))
            numeroImplementadas = getUnidadesImplemntadas(self.cb_resumenCamaras.currentText())
            self.lb_resumenNumeroCamarasImplementadas.setText(str(numeroImplementadas))


        else:
            self.bt_clearResumenCamara.setEnabled(False)
            self.lb_resumenNumeroCamarasTotal.setText("-")
            self.lb_resumenNumeroCamarasImplementadas.setText("-")

    def eliminarCamaras(self):
        from ArchivosXML.FuncionesXML import eliminarCamaras, eliminaunaunidad
        if self.cb_resumenCamaras.currentText() != "Seleccione modelo existente":
            numeroTot = int(self.lb_resumenNumeroCamarasTotal.text())
            numeroImp = int(self.lb_resumenNumeroCamarasImplementadas.text())
            numeroBorrar = int(self.sp_unidadesEliminar.text())
            numeroMaxBorrar = numeroTot - numeroImp

            confirmacion = True

            if confirmacion == True:

                if numeroBorrar > numeroMaxBorrar:
                    self.mensaje.setText("Solo se eliminaran " + str(
                        numeroMaxBorrar) + " unidades del modelo " + self.cb_resumenCamaras.currentText() + " ya que el resto estan implementadas")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec_()
                    # lanzar funcion borrar camara con numeroMaxBorrar
                    eliminarCamaras(self.cb_resumenCamaras.currentText(), numeroMaxBorrar)
                    # actualizar unidades

                    for i in range(numeroMaxBorrar - 1):
                        eliminaunaunidad(self.cb_resumenCamaras.currentText())
                else:
                    # lanzar funcion borrar con numeroBorrar
                    eliminarCamaras(self.cb_resumenCamaras.currentText(), numeroBorrar)
                    # actualizar numero de unidades
                    for i in range(numeroBorrar - 1):
                        eliminaunaunidad(self.cb_resumenCamaras.currentText())
            self.cb_resumenCamaras.setCurrentIndex(0)
            self.mensaje.setText("Unidades eliminadas correctamente")

        else:
            self.mensaje.setText("Debe seleccionar un modelo de camara")
            self.mensaje.exec_()

    def resetarAplicacion(self):
        confirmacion = True

        if confirmacion == True:
            self.mensaje.setText("Se reiniciara la aplicación")
            self.mensaje.exec_()

            from ArchivosXML.FuncionesXML import ReseteaArchivosXML
            ReseteaArchivosXML()

            self.close()

    # FUNIONES ELIMINAR ARCHIVOS

    def eliminarDem(self):
        from ArchivosXML.FuncionesXML import getEstadoArchivo, EliminarArchivos

        nombreArchivo = self.cb_eliminarDEM.currentText()

        estado = getEstadoArchivo(nombreArchivo)

        if estado == "NoCargado":
            confirmacion = True
            if confirmacion == True:
                EliminarArchivos(nombreArchivo)
                self.mensaje.setWindowTitle("Archivo eliminado correctamente")
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El archivo fue eliminado")
                self.mensaje.exec_()

            self.rellenarComboDEM()



        else:
            self.mensaje.setWindowTitle("Error eliminando archivos")
            self.mensaje.setText("El archivo se encuentra cargado, no se puede eliminar")
            self.mensaje.exec_()

    def eliminarShape(self):
        from ArchivosXML.FuncionesXML import getEstadoArchivo, EliminarArchivos

        nombreArchivo = self.cb_eliminarShape.currentText()

        estado = getEstadoArchivo(nombreArchivo)

        if estado == "NoCargado":
            confirmacion = True
            if confirmacion == True:
                EliminarArchivos(nombreArchivo)
                self.mensaje.setWindowTitle("Archivo eliminado correctamente")
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El archivo fue eliminado")
                self.mensaje.exec_()

                self.rellenarComboShape()



        else:
            self.mensaje.setWindowTitle("Error eliminando archivos")
            self.mensaje.setText("El archivo se encuentra cargado, no se puede eliminar")
            self.mensaje.exec_()

    def eliminarPunt(self):
        from ArchivosXML.FuncionesXML import getEstadoArchivo, EliminarArchivos

        nombreArchivo = self.cb_eliminarPunt.currentText()

        estado = getEstadoArchivo(nombreArchivo)

        if estado == "NoCargado":
            confirmacion = True
            if confirmacion == True:
                EliminarArchivos(nombreArchivo)
                self.mensaje.setWindowTitle("Archivo eliminado correctamente")
                self.mensaje.setIcon(QMessageBox.Information)
                self.mensaje.setText("El archivo fue eliminado")
                self.mensaje.exec_()

                self.rellenarComboPuntuaciones()





        else:
            self.mensaje.setWindowTitle("Error eliminando archivos")
            self.mensaje.setText("El archivo se encuentra cargado, no se puede eliminar")
            self.mensaje.exec_()

    def cambioEstadoEliminarDem(self):

        if self.cb_eliminarDEM.currentText() == "Seleccione archivo":
            self.bt_clearDem.setEnabled(False)

        else:
            self.bt_clearDem.setEnabled(True)

    def cambioEstadoEliminarShape(self):

        if self.cb_eliminarShape.currentText() == "Seleccione archivo":
            self.bt_clearShape.setEnabled(False)

        else:
            self.bt_clearShape.setEnabled(True)

    def cambioEstadoEliminarPunt(self):

        if self.cb_eliminarPunt.currentText() == "Seleccione archivo":
            self.bt_clearPunt.setEnabled(False)

        else:
            self.bt_clearPunt.setEnabled(True)

    #Funcion lanzar OPT

    def lanzarOpt(self):
        huboError = False
        from ArchivosXML.FuncionesXML import totalUnidadesImplementadas
        unidadesImplementadas = totalUnidadesImplementadas()
        from fire.ArchivosConfiguracion.FuncionesXML import escribeParametroOpt, getUnParametro,listaNombres
        escribeParametroOpt("cantidad", str(unidadesImplementadas))

        for nombreParam in listaNombres:
            valor = getUnParametro(nombreParam)

            if valor == "0" and nombreParam != "radioMin" :
                self.mensaje.setWindowTitle("Error en el parametro de configuracio" + nombreParam)
                self.mensaje.setText("El parámetro:" + nombreParam + " es obligatorio")
                self.mensaje.exec_()

                huboError = True


        if huboError == False:
           self.hiloTxt.start()

