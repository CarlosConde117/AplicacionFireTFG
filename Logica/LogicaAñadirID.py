from PySide2.QtWidgets import QDialog, QMessageBox
from Views.PopUp_InsertarID import Ui_PopUp_InsertarID
from Logica.VentanaPrincipal import ListAplicacion
class ListPopInsertarID(QDialog, Ui_PopUp_InsertarID):
    def __init__(self,parent = None):                                              #constructror ventana principal
        super().__init__(parent)
        self.setupUi(self)


        Ids = ListAplicacion.NumeroIdRestantes

        Modelo = ListAplicacion.ModeloSeleccionado

        self.lb_modeloSeleccionado.setText(Modelo)
        self.lb_idRestantes.setText(str(Ids))




        # DECLARACION MSGBOX

        self.mensaje = QMessageBox()
        self.mensaje.setWindowTitle("Error valores introducidos")
        self.mensaje.setIcon(QMessageBox.Critical)


    #EVENTOS
        self.bt_confirmar.clicked.connect(self.confirmaID)


    #FUNCIONES

    def confirmaID(self):

        if len(self.ln_id.text()) > 0:
            from ArchivosXML.FuncionesXML import insertaNuevaCamara
            insertaNuevaCamara(self.ln_id.text(),self.lb_modeloSeleccionado.text(), "0", "0")
            self.close()
        else:
            self.mensaje.setText("Debe introducir un ID")
            self.mensaje.exec_()




