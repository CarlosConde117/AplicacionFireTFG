import os

from PySide2.QtWidgets import QApplication, QMessageBox
from Logica.VentanaPrincipal import ListAplicacion
from threading import Thread
from multiprocessing import Process
def LanzaApp():
    Aplicacion = QApplication()
    Ventana = ListAplicacion()
    Ventana.show()
    Aplicacion.exec_()


hiloPpal = Thread(target= LanzaApp)

def arrancaApp():
    Aplicacion = QApplication()
    Ventana = ListAplicacion()
    Ventana.show()
    Aplicacion.exec_()



if __name__ == "__main__":
   #hiloPpal.start()
   #Aplicacion = QApplication()
   #Ventana = ListAplicacion()
   #Ventana.show()
   #Aplicacion.exec_()

   proc = Process(target= arrancaApp)
   proc.start()

