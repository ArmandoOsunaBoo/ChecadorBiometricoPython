 # Aqui vamos a definir la estructura de aplicacion
from distutils.dir_util import copy_tree
import os
import datetime
import importlib
from tkinter import messagebox as mbox 
import face_recognition 
from tkinter import *
from tkinter import ttk
import argparse 
import imutils
from cv2 import cv2
import PIL
from imutils.video import FPS, VideoStream
from PIL import Image, ImageTk
import pickle
import codificacion_rostro
from base_de_datos import BaseDeDatos
from scanner_dedo import ScanerHuella
import shutil
from tkcalendar import * 
import tempfile
from pyfingerprint.pyfingerprint import PyFingerprint
from time import time
from time import sleep
from controlador_nfc import *
checador_ip = "0.0.0.0"
servidor_ip = "0.0.0.0"
numero_empleado = ""
scale_percent = 70
nombreChecador= "Checador Recepcion A"
width, height = 400, 240
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# la ruta para la usb es "/media/pi/NORMAN" por lo que la USB obligatoriamente debe llamarse NORMAN


def quit_ventana_reportes_vtn():
    app.ventana_reportes_vtn.destroy()
                      
def quit_aviso():
    app.aviso.destroy()

def quit_result_vtn():
    app.result_vtn.destroy()
    app.ventana_checadaX.destroy()

def quit_ventana_checadaX(): 
    app.ventana_checadaX.destroy()

def quit_config_vtn():
    app.config_vtn.destroy()

def quit_registro_vtn():
    app.registro_vtn.destroy()

def quit_ventana_descarga_usb():
        app.descargar_usb_vtn.destroy()

def quit_ventana_carga_usb():
        app.cargar_usb_vtn.destroy()
        
def quit_numempleado_vtn():
        app.numempleado_vtn.destroy()
        
def quit_ventana_huella():
        app.ventana_huella.destroy()

def quit_entrada_vtn():
    app.entrada_vtn.destroy()

def quit_cambio_empleado_vtn():
    app.cambio_empleado_vtn.destroy()

class ChecadorAPP(Frame):

        def __init__(self, master=None):
                super().__init__(master, width=800, height=480)
                self.master = master
                #self.master.overrideredirect(True)
                self.vartxt = StringVar()
                self.contador = 0
                self.numero_empleado=""
                #self.bd = BaseDeDatos("192.168.108.21","root","normanmx2020","checador_db",3306)
                self.pack()
                self.crear_controles()

        

        def enviar_registro(self,hora,numeroempleado,evento,nombreChecador):
                print("conexion a base de datos..")
                bd = BaseDeDatos("127.0.0.1","root","normanmx2020","checador_db",3306)
                hora_actual2 = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
                h = datetime.datetime.now().strftime('%H:%M')
                fecha = datetime.datetime.now().strftime('%Y/%m/%d')
                
                bd.insertRegistro(hora_actual2,numeroempleado,evento,nombreChecador,fecha,h)
                print(hora_actual2)
                quit_result_vtn()

        def ventana_resultadoChecador(self,numeroempleado,hora,evento):
                self.result_vtn = Toplevel(self) 
                self.result_vtn.geometry("+{}+{}".format(0, 0))
                self.result_vtn.overrideredirect(True)
                self.result_vtn.title("Registro de Empleado")
                self.result_vtn.canvas = Canvas(
                    self.result_vtn, bg="black", width=800, height=480)
                self.result_vtn.canvas.pack()
                self.result_vtn.bind('<Escape>', lambda e: root.quit())
                self.result_vtn.portada = Image.open("imagenes/fondo_negro.png")
                self.result_vtn.portada2 = self.result_vtn.portada.resize((800, 480), Image.ANTIALIAS)
                self.result_vtn.fondo_config = ImageTk.PhotoImage(self.result_vtn.portada2)
                self.result_vtn.canvas.create_image(400, 100, image=self.result_vtn.fondo_config)
                rutaImagen =  os.getcwd()
                """rutaImagen = rutaImagen+"/fotos_empleados/"+numeroempleado
                img = cv2.imread(rutaImagen) """
                #
                self.result_vtn.portada3 = Image.open(rutaImagen+"/fotos_empleados/"+numeroempleado+".png")
                self.result_vtn.portada4 = self.result_vtn.portada3.resize((210, 280), Image.ANTIALIAS)
                self.result_vtn.fondo_config2 = ImageTk.PhotoImage(self.result_vtn.portada4)
                self.result_vtn.canvas.create_image(210, 280, image=self.result_vtn.fondo_config2)
                self.result_vtn.label1 = Label(
                    self.result_vtn, text=evento+" \n "+numeroempleado+"\n "+hora, font="Verdana 16 bold", fg="white", bg="black")
                self.result_vtn.label1.place(x=210, y=10)
                #
                self.result_vtn.img2 = Image.open("imagenes/correctobtn.png")
                self.result_vtn.img2 = self.result_vtn.img2.resize(
                    (180, 55), Image.ANTIALIAS)
                self.result_vtn.img2 = ImageTk.PhotoImage(self.result_vtn.img2)
                self.result_vtn.tomarfotobtn = Button(
                    self.result_vtn, width=180, height=55, image=self.result_vtn.img2, command=lambda: self.enviar_registro(hora,numeroempleado,evento,nombreChecador), borderwidth=0)
                self.result_vtn.tomarfotobtn.place(x=550, y=150)
                #5
                self.result_vtn.img4 = Image.open("imagenes/nobtn.png")
                self.result_vtn.img4 = self.result_vtn.img4.resize(
                    (180, 55), Image.ANTIALIAS)
                self.result_vtn.img4 = ImageTk.PhotoImage(self.result_vtn.img4)
                self.result_vtn.tomarfotobtn = Button( self.result_vtn, width=180, height=55, image=self.result_vtn.img4, command=quit_result_vtn, borderwidth=0)
                self.result_vtn.tomarfotobtn.place(x=550, y=220)


        def descarga_de_archivos(self):
                #bd.obtenerChecadas(self,fecha_inicio,fecha_final )
                try:
                    newPath = shutil.copy('/media/pi/NORMAN/DataResult.xlsx', os.path.abspath(os.getcwd()))
                    self.cargar_usb_vtn.progress['value'] = 20
                    self.cargar_usb_vtn.progress.update_idletasks()
                    self.cargar_usb_vtn.T.see(END)
                    self.cargar_usb_vtn.T.insert(END, "Excel con checadas cargado con exito! \n")
                except Exception as e:
                    print('Operacion Fallida!')
                    print('Mensage de Error: ' + str(e))
                    self.cargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
                try:
                    newPath = shutil.copy('/media/pi/NORMAN/codificaciones.pickle', os.path.abspath(os.getcwd()))
                    self.cargar_usb_vtn.progress['value'] = 40
                    self.cargar_usb_vtn.T.insert(END, "Codificaciones cargadas con exito! \n")
                    self.cargar_usb_vtn.progress.update_idletasks()
                    self.cargar_usb_vtn.T.see(END)
                except Exception as e:
                    print('Operacion Fallida!')
                    print('Mensage de Error: ' + str(e))
                    self.cargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
                try:
                    newPath = copy_tree('/media/pi/NORMAN/dataset_huella', os.path.abspath(os.getcwd()+"/dataset_huella"))
                    self.cargar_usb_vtn.progress['value'] = 60
                    self.cargar_usb_vtn.T.insert(END, "Dataset de Huellas cargadas con exito! \n")
                    self.cargar_usb_vtn.progress.update_idletasks()
                    self.cargar_usb_vtn.T.see(END)
                except Exception as e:
                    print('Operacion Fallida!')
                    print('Mensage de Error: ' + str(e))
                    self.cargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
                try:
                    newPath = copy_tree('/media/pi/NORMAN/dataset', os.path.abspath(os.getcwd()+"/dataset"))
                    self.cargar_usb_vtn.progress['value'] = 80
                    self.cargar_usb_vtn.T.insert(END, "Dataset cargado con exito! \n")
                    self.cargar_usb_vtn.progress.update_idletasks()
                    self.cargar_usb_vtn.T.see(END)
                except Exception as e:
                    print('Operacion Fallida!')
                    print('Mensage de Error: ' + str(e))
                    self.cargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
                try:
                    newPath = copy_tree('/media/pi/NORMAN/fotos_empleados', os.path.abspath(os.getcwd()+"/fotos_empleados"))
                    self.cargar_usb_vtn.progress['value'] = 100
                    self.cargar_usb_vtn.T.insert(END, "Fotos de empleados cargadas con exito! \n")
                    self.cargar_usb_vtn.progress.update_idletasks()
                    self.cargar_usb_vtn.T.see(END)
                except Exception as e:
                    print('Operacion Fallida!')
                    print('Mensage de Error: ' + str(e))
                    self.cargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
                self.cargar_usb_vtn.progress['value'] = 100
                self.cargar_usb_vtn.progress.update_idletasks()

        def ventana_carga_usb(self,a):
            self.cargar_usb_vtn = Toplevel(self) 
            self.cargar_usb_vtn.geometry("+{}+{}".format(0, 0))
            self.cargar_usb_vtn.overrideredirect(True)
            self.cargar_usb_vtn.title("Subir datos a la USB")
            self.cargar_usb_vtn.bind('<Escape>', lambda e: root.quit())
            self.cargar_usb_vtn.canvas = Canvas(self.cargar_usb_vtn, bg="black", width=500, height=400)
            self.cargar_usb_vtn.canvas.pack()
            self.cargar_usb_vtn.portada3 = Image.open("imagenes/fondo_negro.png")
            self.cargar_usb_vtn.portada4 = self.cargar_usb_vtn.portada3.resize((1200, 800), Image.ANTIALIAS)
            self.cargar_usb_vtn.fondo_config2 = ImageTk.PhotoImage(self.cargar_usb_vtn.portada4)
            self.cargar_usb_vtn.canvas.create_image(0, 0, image=self.cargar_usb_vtn.fondo_config2) 
            #
            self.cargar_usb_vtn.T = Text(self.cargar_usb_vtn, height=7, width=60)
            self.cargar_usb_vtn.T.place(x=5,y=80)
            self.cargar_usb_vtn.T.insert(END, "Carga de datos a USB... \n")
            self.cargar_usb_vtn.progress = ttk.Progressbar(self.cargar_usb_vtn, orient = HORIZONTAL,  length = 500, mode = 'determinate') 
            self.cargar_usb_vtn.progress.place(x=0,y=200) 
            self.cargar_usb_vtn.avisobtn = Button( self.cargar_usb_vtn, width=5, height=1, text="Descargar",command=lambda:self.descarga_de_archivos(), borderwidth=1)
            self.cargar_usb_vtn.avisobtn.place(x=200,y=250)
                
            #
            self.cargar_usb_vtn.ggg = Image.open("imagenes/regresarbtn.png")
            self.cargar_usb_vtn.ggg = self.cargar_usb_vtn.ggg.resize((50, 50), Image.ANTIALIAS)
            self.cargar_usb_vtn.ggg = ImageTk.PhotoImage(self.cargar_usb_vtn.ggg)
            self.cargar_usb_vtn.ggg_btn  = Button(self.cargar_usb_vtn, width=50, height=50, image=self.cargar_usb_vtn.ggg, command=lambda:self.cargar_usb_vtn.destroy(), borderwidth=0)
            self.cargar_usb_vtn.ggg_btn.place(x=400, y=300)
            '''
                self.cargar_usb_vtn = Toplevel(self) 
                self.cargar_usb_vtn.geometry("500x200+{}+{}".format(0, 0))
                self.cargar_usb_vtn.title("Subir datos al sistema")
                self.cargar_usb_vtn.bind('<Escape>', lambda e: root.quit())
                
                self.cargar_usb_vtn.T = Text(self.cargar_usb_vtn, height=7, width=50)
                self.cargar_usb_vtn.T.pack()
                self.cargar_usb_vtn.T.insert(END, "Iniciando carga al sistema... \n")
                self.cargar_usb_vtn.progress = ttk.Progressbar(self.cargar_usb_vtn, orient = HORIZONTAL,  length = 500, mode = 'determinate') 
                self.cargar_usb_vtn.progress.pack() 
                
                self.cargar_usb_vtn.avisobtn = Button( self.cargar_usb_vtn, width=5, height=1, text="Descargar", command=lambda:self.descarga_de_archivos(), borderwidth=1)
                self.cargar_usb_vtn.avisobtn.place(x=100,y=160)
                
                self.cargar_usb_vtn.cancelarbtn = Button( self.cargar_usb_vtn, width=5, height=1, text="Cancelar", command=lambda:quit_ventana_carga_usb(), borderwidth=1)
                self.cargar_usb_vtn.cancelarbtn.place(x=300,y=160) 
                '''


        def carga_de_archivos(self):
            try:
                #bd.obtenerChecadas(self,fecha_inicio,fecha_final )
                newPath = shutil.copy('DataResult.xlsx', '/media/pi/NORMAN')
                self.descargar_usb_vtn.progress['value'] = 20
                self.descargar_usb_vtn.progress.update_idletasks()
                self.descargar_usb_vtn.T.see(END)
                self.descargar_usb_vtn.T.insert(END, "Excel con checadas cargado con exito! \n")
            except Exception as e:
                print('Operacion Fallida!')
                print('Mensage de Error: ' + str(e))
                self.descargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
            try:
                newPath = shutil.copy('codificaciones.pickle', '/media/pi/NORMAN')
                self.descargar_usb_vtn.progress['value'] = 40
                self.descargar_usb_vtn.T.insert(END, "Codificaciones cargadas con exito! \n")
                self.descargar_usb_vtn.progress.update_idletasks()
                self.descargar_usb_vtn.T.see(END)
            except Exception as e:
                print('Operacion Fallida!')
                print('Mensage de Error: ' + str(e))
                self.descargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
            try:
                os.mkdir("/media/pi/NORMAN/fotos_empleados")
                newPath = copy_tree('fotos_empleados', '/media/pi/NORMAN/fotos_empleados')
                self.descargar_usb_vtn.progress['value'] = 60
                self.descargar_usb_vtn.T.insert(END, "Fotos de empleados cargadas con exito! \n")
                self.descargar_usb_vtn.progress.update_idletasks()
                self.descargar_usb_vtn.T.see(END)
            except Exception as e:
                print('Operacion Fallida!')
                print('Mensage de Error: ' + str(e))
                self.descargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
            try:
                os.mkdir("/media/pi/NORMAN/dataset")
                newPath = copy_tree('dataset', '/media/pi/NORMAN/dataset')
                self.descargar_usb_vtn.progress['value'] = 80
                self.descargar_usb_vtn.T.insert(END, "Fotos cargadas con exito! \n")
                self.descargar_usb_vtn.T.see(END)
            except Exception as e:
                print('Operacion Fallida!')
                print('Mensage de Error: ' + str(e))
                self.descargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
            try:
                os.mkdir("/media/pi/NORMAN/dataset_huella")
                self.descargar_usb_vtn.progress.update_idletasks()
                newPath = copy_tree('dataset_huella', '/media/pi/NORMAN/dataset_huella')
                self.descargar_usb_vtn.progress['value'] = 100
                self.descargar_usb_vtn.T.insert(END, "Huellas cargadas con exito! \n")
                self.descargar_usb_vtn.T.see(END)
                self.descargar_usb_vtn.progress.update_idletasks()
            except Exception as e:
                print('Operacion Fallida!')
                print('Mensage de Error: ' + str(e))
                self.descargar_usb_vtn.T.insert(END, "Error: "+str(e)+"\n")
            self.descargar_usb_vtn.progress['value'] = 100
            self.descargar_usb_vtn.progress.update_idletasks()

        def ventana_descarga_usb(self,a):
            self.descargar_usb_vtn = Toplevel(self) 
            self.descargar_usb_vtn.geometry("+{}+{}".format(0, 0))
            self.descargar_usb_vtn.overrideredirect(True)
            self.descargar_usb_vtn.title("Subir datos a la USB")
            self.descargar_usb_vtn.bind('<Escape>', lambda e: root.quit())
            self.descargar_usb_vtn.canvas = Canvas(self.descargar_usb_vtn, bg="black", width=500, height=400)
            self.descargar_usb_vtn.canvas.pack()
            self.descargar_usb_vtn.portada3 = Image.open("imagenes/fondo_negro.png")
            self.descargar_usb_vtn.portada4 = self.descargar_usb_vtn.portada3.resize((1200, 800), Image.ANTIALIAS)
            self.descargar_usb_vtn.fondo_config2 = ImageTk.PhotoImage(self.descargar_usb_vtn.portada4)
            self.descargar_usb_vtn.canvas.create_image(0, 0, image=self.descargar_usb_vtn.fondo_config2) 
            #
            self.descargar_usb_vtn.T = Text(self.descargar_usb_vtn, height=7, width=60)
            self.descargar_usb_vtn.T.place(x=5,y=80)
            self.descargar_usb_vtn.T.insert(END, "Descarga de datos a USB... \n")
            self.descargar_usb_vtn.progress = ttk.Progressbar(self.descargar_usb_vtn, orient = HORIZONTAL,  length = 500, mode = 'determinate') 
            self.descargar_usb_vtn.progress.place(x=0,y=200) 
            self.descargar_usb_vtn.avisobtn = Button( self.descargar_usb_vtn, width=5, height=1, text="Descargar", command=lambda:self.carga_de_archivos(), borderwidth=1)
            self.descargar_usb_vtn.avisobtn.place(x=200,y=250)
                
            #
            self.descargar_usb_vtn.ggg = Image.open("imagenes/regresarbtn.png")
            self.descargar_usb_vtn.ggg = self.descargar_usb_vtn.ggg.resize((50, 50), Image.ANTIALIAS)
            self.descargar_usb_vtn.ggg = ImageTk.PhotoImage(self.descargar_usb_vtn.ggg)
            self.descargar_usb_vtn.ggg_btn  = Button(self.descargar_usb_vtn, width=50, height=50, image=self.descargar_usb_vtn.ggg, command=lambda:self.descargar_usb_vtn.destroy(), borderwidth=0)
            self.descargar_usb_vtn.ggg_btn.place(x=400, y=300)
            '''
              
                 
                
                
                '''


        def ventana_tarjeta(self,evento):

            hora_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
            if float(hora_actual[0:2])<=12:
                extension="a.m."
            else:
                extension="p.m."

            nfc = Controlador_NFC()
            numempleado = nfc.leer_tarjeta()
            if numempleado ==-1:
                self.crear_cuadro_error("Ingrese un numero de empleado valido")
            else:
                self.ventana_resultadoChecador(numempleado,hora_actual+" "+extension,evento)


        def ventana_huellax(self,evento):
                self.ventana_huella = Toplevel(self) 
                self.ventana_huella.geometry("+{}+{}".format(0, 0))
                self.ventana_huella.overrideredirect(True)
                self.ventana_huella.title("Checada con huella")
                self.ventana_huella.bind('<Escape>', lambda e: root.quit())
                self.ventana_huella.canvas = Canvas(self.ventana_huella, bg="black", width=800, height=480)
                self.ventana_huella.canvas.pack()
                self.ventana_huella.portada3 = Image.open("imagenes/fondo_negro.png")
                self.ventana_huella.portada4 = self.ventana_huella.portada3.resize((800, 480), Image.ANTIALIAS)
                self.ventana_huella.fondo_config2 = ImageTk.PhotoImage(self.ventana_huella.portada4)
                self.ventana_huella.canvas.create_image(400, 240, image=self.ventana_huella.fondo_config2) 
                ##Label
                self.ventana_huella.label = Label( self.ventana_huella, text = "Ingrese un número de empleado", bg="black", fg="white", font="Verdana 26 bold") 
                self.ventana_huella.label.place(x=100,y=20) 
                ##Entry
                self.ventana_huella.numempleado = Entry(self.ventana_huella, width=10, font="Verdana 14 bold")
                self.ventana_huella.numempleado.place(x=200, y=100)
                # 
                ##Boton de esperar Huella
                self.ventana_huella.imgy = Image.open("imagenes/revisarhuella.png")
                self.ventana_huella.imgy = self.ventana_huella.imgy.resize((180, 55), Image.ANTIALIAS)
                self.ventana_huella.imgy = ImageTk.PhotoImage(self.ventana_huella.imgy)
                self.ventana_huella.tomar_huellabtn = Button(self.ventana_huella, width=180, height=55, image=self.ventana_huella.imgy, command=lambda:self.huella_checada(evento,self.ventana_huella.numempleado.get()), borderwidth=0)
                self.ventana_huella.tomar_huellabtn.place(x=500, y=200)
                #boton regresar
                self.ventana_huella.ggg = Image.open("imagenes/regresarbtn.png")
                self.ventana_huella.ggg = self.ventana_huella.ggg.resize(
                            (50, 50), Image.ANTIALIAS)
                self.ventana_huella.ggg = ImageTk.PhotoImage(self.ventana_huella.ggg)
                self.ventana_huella.ggg_btn  = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.ggg, command=quit_ventana_huella, borderwidth=0)
                self.ventana_huella.ggg_btn.place(x=100, y=100)
                #SECCION PARA LOS BOTONES DE PONER LOS NUMEROS
                #
                self.ventana_huella.im1 = Image.open("imagenes/0.png")
                self.ventana_huella.im1 = self.ventana_huella.im1.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im1 = ImageTk.PhotoImage(self.ventana_huella.im1)
                self.ventana_huella.btn1 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im1, command=lambda:self.ingresar_caracter("0"), borderwidth=0)
                self.ventana_huella.btn1.place(x=100, y=200)
                #
                self.ventana_huella.im2 = Image.open("imagenes/1.png")
                self.ventana_huella.im2 = self.ventana_huella.im2.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im2 = ImageTk.PhotoImage(self.ventana_huella.im2)
                self.ventana_huella.btn2 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im2, command=lambda:self.ingresar_caracter("1"), borderwidth=0)
                self.ventana_huella.btn2.place(x=200, y=200)
                #
                self.ventana_huella.im3 = Image.open("imagenes/2.png")
                self.ventana_huella.im3 = self.ventana_huella.im3.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im3 = ImageTk.PhotoImage(self.ventana_huella.im3)
                self.ventana_huella.btn3 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im3, command=lambda:self.ingresar_caracter("2"), borderwidth=0)
                self.ventana_huella.btn3.place(x=300, y=200)
                #
                self.ventana_huella.im4 = Image.open("imagenes/3.png")
                self.ventana_huella.im4 = self.ventana_huella.im4.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im4 = ImageTk.PhotoImage(self.ventana_huella.im4)
                self.ventana_huella.btn4 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im4, command=lambda:self.ingresar_caracter("3"), borderwidth=0)
                self.ventana_huella.btn4.place(x=400, y=200)
                #
                self.ventana_huella.im5 = Image.open("imagenes/4.png")
                self.ventana_huella.im5 = self.ventana_huella.im5.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im5 = ImageTk.PhotoImage(self.ventana_huella.im5)
                self.ventana_huella.btn5 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im5, command=lambda:self.ingresar_caracter("4"), borderwidth=0)
                self.ventana_huella.btn5.place(x=100, y=300)
                #
                self.ventana_huella.im6 = Image.open("imagenes/5.png")
                self.ventana_huella.im6 = self.ventana_huella.im6.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im6 = ImageTk.PhotoImage(self.ventana_huella.im6)
                self.ventana_huella.btn6 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im6, command=lambda:self.ingresar_caracter("5"), borderwidth=0)
                self.ventana_huella.btn6.place(x=200, y=300)
                #
                self.ventana_huella.im7 = Image.open("imagenes/6.png")
                self.ventana_huella.im7 = self.ventana_huella.im7.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im7 = ImageTk.PhotoImage(self.ventana_huella.im7)
                self.ventana_huella.btn7 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im7,command=lambda:self.ingresar_caracter("6"), borderwidth=0)
                self.ventana_huella.btn7.place(x=300, y=300)
                #
                self.ventana_huella.im8 = Image.open("imagenes/7.png")
                self.ventana_huella.im8 = self.ventana_huella.im8.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im8 = ImageTk.PhotoImage(self.ventana_huella.im8)
                self.ventana_huella.btn8 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im8, command=lambda:self.ingresar_caracter("7"), borderwidth=0)
                self.ventana_huella.btn8.place(x=400, y=300)
                #
                self.ventana_huella.im9 = Image.open("imagenes/8.png")
                self.ventana_huella.im9 = self.ventana_huella.im9.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im9 = ImageTk.PhotoImage(self.ventana_huella.im9)
                self.ventana_huella.btn9 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im9, command=lambda:self.ingresar_caracter("8"), borderwidth=0)
                self.ventana_huella.btn9.place(x=100, y=400)
                #
                self.ventana_huella.im10 = Image.open("imagenes/9.png")
                self.ventana_huella.im10 = self.ventana_huella.im10.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.im10 = ImageTk.PhotoImage(self.ventana_huella.im10)
                self.ventana_huella.btn10 = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.im10, command=lambda:self.ingresar_caracter("9"), borderwidth=0)
                self.ventana_huella.btn10.place(x=200, y=400)
                #
                self.ventana_huella.sprbtn = Image.open("imagenes/supr.png")
                self.ventana_huella.sprbtn = self.ventana_huella.sprbtn.resize((50, 50), Image.ANTIALIAS)
                self.ventana_huella.sprbtn = ImageTk.PhotoImage(self.ventana_huella.sprbtn)
                self.ventana_huella.spr_btn = Button(self.ventana_huella, width=50, height=50, image=self.ventana_huella.sprbtn, command=lambda:self.ingresar_caracter("x"), borderwidth=0)
                self.ventana_huella.spr_btn.place(x=300, y=400)

                self.ventana_huella.T = Text(self.ventana_huella, height=4, width=35)
                self.ventana_huella.T.place(x=400,y=100)
                self.ventana_huella.T.insert(END, "Esperando numero de empleado\n")

        def ingresar_caracterregistro(self,char):
            text=""
            if(len(self.numempleado_vtn.numempleado.get())<5 or char == "x"):
                if(char == "x" and len(self.numempleado_vtn.numempleado.get())>0 ):
                    text = self.numempleado_vtn.numempleado.get()
                    text = text[:-1]
                    
                else:
                    if(str(char)!="x"):
                        text = self.numempleado_vtn.numempleado.get()
                        text= text+str(char) 
                        if(len(self.numempleado_vtn.numempleado.get())==5):
                            self.numempleado_vtn.T.insert(END, "Presione \"Analizar huella\"\n")

                self.numempleado_vtn.numempleado.delete(0,END)
                self.numempleado_vtn.numempleado.insert(0,text)
            else:
                self.numempleado_vtn.T.insert(END, "Solo 5 digitos\n")
                self.numempleado_vtn.T.see(END)

        
        def ingresar_caracterentrada(self,char):
            text=""
            if(len(self.entrada_vtn.numempleado.get())<9 or char == "x"):
                if(char == "x" and len(self.entrada_vtn.numempleado.get())>0 ):
                    text = self.entrada_vtn.numempleado.get()
                    text = text[:-1] 

                else:
                    if(str(char)!="x"):
                        text = self.entrada_vtn.numempleado.get()
                        text= text+str(char)
                        if(len(self.entrada_vtn.numempleado.get())==9):
                            print("Presione \"Analizar huella\"\n")

                self.entrada_vtn.numempleado.delete(0,END)
                self.entrada_vtn.numempleado.insert(0,text)
                
            else:
                print("Presione \"Analizar huella\"\n")



        def ingresar_caracter(self,char):
            text=""
            if(len(self.ventana_huella.numempleado.get())<5 or char == "x"):
                if(char == "x" and len(self.ventana_huella.numempleado.get())>0 ):
                    text = self.ventana_huella.numempleado.get()
                    text = text[:-1]
                    self.ventana_huella.T.delete(0, 'end')

                else:
                    if(str(char)!="x"):
                        text = self.ventana_huella.numempleado.get()
                        text= text+str(char)
                        if(len(self.ventana_huella.numempleado.get())==5):
                            self.ventana_huella.T.insert(END, "Presione \"Analizar huella\"\n")

                self.ventana_huella.numempleado.delete(0,END)
                self.ventana_huella.numempleado.insert(0,text)
                
            else:
                self.ventana_huella.T.insert(END, "Solo 5 digitos\n")
                self.ventana_huella.T.see(END)


  
        def huella_checada(self,evento,numempleado):
                print(evento)
                print("Numero Empleado: "+str(numempleado))
                
                if(numempleado=="" or len(numempleado)<5):
                    #mbox.showerror("Error 3", "Ingrese un numero de empleado valido",parent=self.ventana_huella)
                    self.crear_cuadro_error("Ingrese un numero de empleado valido")
                else:
                    if os.path.isfile(str(os.getcwd())+"/dataset_huella/"+"0_"+str(numempleado)+".bmp"):
                        #Si existe un archivo asi significa quee si esta registrado con huella
                        self.revisar_hora(0)
                        #Vamos a evaluar que empleado es en base al numero de empleado
                        ###Primero se obtiene la huella actual del empleado
                        try:
                                
                                print("Intentando conectar al scanner")
                                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                                if ( f.verifyPassword() == False ):
                                        raise ValueError('La contraseña del sensor no es correcta!')
                                print("Conexion lograda")
                                print('Templates usados: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
                                try:
                                        start_time = time()
                                        print('***Esperando Huella...***')
                                        ###
                                        
                                        ###
                                        while ( f.readImage() == False ):
                                                pass
                                        
                                        
                                        try:
                                            time.sleep(0.5)
                                        except Exception as e: 
                                            print('shhh') 
                                        
                                        print('Descargando imagen (Esto puede tomar tiempo)...')
                                        imageDestination =  os.getcwd() + '/huella_prueba.bmp'
                                        f.downloadImage(imageDestination)
                                        print('Fin del analisis!')  
                                        #im = cv2.imread(imageDestination)
                                        #im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                                        #th, im_gray_th_otsu = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY)
                                        #cv2.imwrite(imageDestination, im_gray_th_otsu)
                                        
                                        
                                        matches=""
                                        ###
                                        try:
                                                for x in range(0,3):
                                                        print("Intento: "+str(x))
                                                        fingerprint_database_image = cv2.imread(str(os.getcwd())+"/dataset_huella/"+str(x)+"_"+str(numempleado)+".bmp")
                                                        print(str(os.getcwd())+"/dataset_huella/"+str(x)+"_"+str(numempleado)+".bmp")
                                                        #cv2.imshow("--imgDatabase"+str(x), fingerprint_database_image)
                                                        #Esto es solo por si se necesita binarizar la imagen dependiendo del caso  
                                                        ###print("Escribiendo con filtro"+str(th))
                                                        
                                                        sift = cv2.xfeatures2d.SIFT_create() 
                                                        img2= cv2.imread(imageDestination)
                                                        #cv2.imshow(str(x)+str(imageDestination), img2)
                                                        
                                                        keypoints_1, descriptors_1 = sift.detectAndCompute(img2, None)
                                                        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)
                                                        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=7), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                                                        match_points = []
                        
                                                        for p, q in matches:
                                                                #print("aaaaaaaayudaaaaaa")
                                                                if p.distance < 0.60*q.distance:
                                                                        match_points.append(p)
                                                        print("Coincidencias: "+str(len(match_points)))
                                                        keypoints = 0
                                                        if len(keypoints_1) <= len(keypoints_2):
                                                                keypoints = len(keypoints_1)            
                                                        else:
                                                                keypoints = len(keypoints_2)
                                                        result = cv2.drawMatches(img2, keypoints_1, fingerprint_database_image, keypoints_2, match_points, None) 
                                                        
                                                        
                                                        #Si todo sale bien pues decimos que si es el empleado
                                                        hora_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
                                                        if float(hora_actual[0:2])<=12:
                                                                extension="a.m."
                                                        else:
                                                                extension="p.m."
                                                        print("% Comparativa: ", len(match_points) / keypoints * 100)
                                                        print("match_points"+str(len(match_points))+"/"+str(keypoints)+" * "+"100")
                                                        
                                                        result = cv2.resize(result, None, fx=2.0, fy=2.0)
                                                        #cv2.imshow("result: "+str(x), result) 
                                                        elapsed_time = time() - start_time
                                                        print("Tiempo transcurrido: %0.10f seconds." % elapsed_time)
                                                        if  (len(match_points) / keypoints * 100)>1.1:
                                                                self.ventana_resultadoChecador(numempleado,hora_actual+" "+extension,evento)
                                                                break
                                                        elif (x==2):
                                                                #mbox.showwarning("Error 4", "No se identifico la huella, si el problema persiste contacte con el administrador.",parent=self.ventana_huella)
                                                                self.crear_cuadro_error("No se identifico la huella, vuelva intentar")
                                                                break
                                        
                                        except Exception as e:
                                                print('Calculo fallido!')
                                                print('Mensage de Error: ' + str(e))
                                        

                                except Exception as e:
                                        print('Operacion Fallida!')
                                        print('Mensage de Error: ' + str(e))
                                                        
                                                
                        except Exception as e:
                                print('El sensor no pudo inicializarse!')
                                print('Mensage de Error: ' + str(e))
                        
                    else:
                        #mbox.showwarning("Error 5", "El empleado no esta registrado.",parent=self.ventana_huella)
                        self.crear_cuadro_error("El empleado no esta registrado")
                                                                
                                
                
                

        def foto_checada(self,evento):
            self.revisar_hora(0)
            #Obtendremos argumentos para poder trabajar
            ap = argparse.ArgumentParser()
            var1= 'haarcascade_frontalface_default.xml'
            var2='codificaciones.pickle'
            # Cargamos las caras conocidas y los datos embebidos
            print("[INFO] Cargando rostros...")
            data = pickle.loads(open(var2, "rb").read())

            detector = cv2.CascadeClassifier(var1)
            # Iniciamos el stream de video dedicado a obtener la imagen
            print("[INFO] starting video stream...")
            frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
            ########vs = VideoStream(src=0).start()
            # vs = VideoStream(usePiCamera=True).start()
            ###time.sleep(2.0)
            # Iniciamos el contador FPS
            ####fps = FPS().start()
            # Tomamos 1 frame de video de la camara y reducimos el tamaño
            # a 500px (para agilizar el proceso)
            ###frame = vs.read()
            frame = imutils.resize(frame, width=500)
            
            # convertimos el frame en escala de grises para poder realizar la detección de rostros
            # y otro frame lo pasamos a RGB para realizar el reconocimiento de rostros
            grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # detectamos el rostro en escala de grises
            rects = detector.detectMultiScale(grises, scaleFactor=1.1, 
                minNeighbors=5, minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

            # OpenCV retorna las cordenadas de la caja en el orden (x,y,w,h) 
            #  pero nosotros lo ocupamos en el orden (arriba,derecha,abajo,izquierda)
            # por lo que tenemos que re-ordenar
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            # computamos cada rostros por cada caja
            encodings =  face_recognition.face_encodings(rgb, boxes)
            names = []
            # realizamos el recorrido sobre las cod faciales
            for encoding in encodings:
                # se intenta realizar un match con cada codificacion que tenemos ya guardada
                # con la imagen actual, se pone
                coincidencias = face_recognition.compare_faces(data["Codificaciones"],
                    encoding)
                nombre = "Desconocido"

                #checamos para ver si conseguimos una coincidencia
                if True in coincidencias:
                    # Encontramos los  indices de todas las coincidencias de rostros
                    # y comparamos con nuestro diccionario para contar el total de veces
                    # que han habido coincidencias con un dataset en especifico
                    coincidenciasIdxs = [i for (i, b) in enumerate(coincidencias) if b]
                    contador = {}
                    #iteramos cada indice y mantenemos la cuenta para cada reconocimiento rostro-rostro
                    for i in coincidenciasIdxs:
                        nombre = data["Nombres"][i]
                        contador[nombre] = contador.get(nombre, 0) + 1

                    # Determina el rostro reconocido por el mayor numero de coincidencias encontradas
                    # en caso de empate se seleccionará la primera coincidencia (heredado de python)
                    nombre = max(contador, key=contador.get)
                    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
                    if float(hora_actual[0:2])<=12:
                        extension="a.m."
                    else:
                        extension="p.m."
                    self.ventana_resultadoChecador(nombre,hora_actual+" "+extension,evento)
                    print("El empleado es: "+nombre)
                
                # actualizamos la lista de nombres
                #nombre.append(nombre)        



        def actualizar_frame(self):
                self.image2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
                width = int(self.image2.shape[1] * scale_percent / 100)
                height = int(self.image2.shape[0] * scale_percent / 100)
                dsize = (self.image2.shape[1], self.image2.shape[0])
                self.image2 = cv2.resize(self.image2, dsize)
                cv2.rectangle(self.image2, (125, 5), (275, 235), (0, 255, 0), 4)
                self.image2 = Image.fromarray(self.image2)
                self.image2 = ImageTk.PhotoImage(self.image2)
                self.ventana_checadaX.canvascv.create_image( 0, 0, anchor=NW, image=self.image2)
                self.ventana_checadaX.after(20, self.actualizar_frame)

        def revisar_hora(self,encendido):
                hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
                if float(hora_actual[0:2])<=12:
                    extension="a.m."
                else:
                    extension="p.m."
                self.vartxt.set(hora_actual+" "+extension)
                
                if (encendido==1):
                    """ print(self.vartxt.get()) """
                    self.ventana_checadaX.label2.update_idletasks()
                    self.ventana_checadaX.after(1000, lambda:self.revisar_hora(1))

        def ventana_checada(self,evento):
                self.ventana_checadaX = Toplevel(self) 
                self.ventana_checadaX.geometry("+{}+{}".format(0, 0))
                self.ventana_checadaX.overrideredirect(True)
                self.ventana_checadaX.title("AAAAAAA")

                self.ventana_checadaX.canvas = Canvas(self.ventana_checadaX, bg="black", width=800, height=480)
                self.ventana_checadaX.canvas.pack()
                self.ventana_checadaX.bind('<Escape>', lambda e: root.quit())
                self.portada3 = Image.open("imagenes/fondo_negro.png")
                self.portada4 = self.portada3.resize((800, 480), Image.ANTIALIAS)
                self.fondo_config2 = ImageTk.PhotoImage(self.portada4)
                self.ventana_checadaX.canvas.create_image(400, 240, image=self.fondo_config2)
                #Sección para pintar la camara
                self.cap = cap
                self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.interval = 20
                self.ventana_checadaX.canvascv = Canvas(self.ventana_checadaX, width=400, height=240)
                self.ventana_checadaX.canvascv.place(x=115, y=125)
                self.actualizar_frame()

                #seccion de labels
                self.ventana_checadaX.label = Label( self.ventana_checadaX, text = evento, bg="black", fg="white", font="Verdana 26 bold")
                self.ventana_checadaX.label2 = Label( self.ventana_checadaX, textvariable =self.vartxt, bg="black", fg="white", font="Verdana 26 bold")
                self.ventana_checadaX.label.place(x=250,y=20)
                self.ventana_checadaX.label2.place(x=250,y=60)
                # Sección para poner botones
                self.ventana_checadaX.img2 = Image.open("imagenes/tomar_fotobtn.png")
                self.ventana_checadaX.img2 = self.ventana_checadaX.img2.resize((180, 55), Image.ANTIALIAS)
                self.ventana_checadaX.img2 = ImageTk.PhotoImage(self.ventana_checadaX.img2)
                self.ventana_checadaX.tomarfotobtn = Button( self.ventana_checadaX, width=180, height=55, image=self.ventana_checadaX.img2, command=lambda:self.foto_checada(evento), borderwidth=0)
                self.ventana_checadaX.tomarfotobtn.place(x=550, y=125)
                #
                self.ventana_checadaX.imgx = Image.open("imagenes/revisarhuella.png")
                self.ventana_checadaX.imgx = self.ventana_checadaX.imgx.resize((180, 55), Image.ANTIALIAS)
                self.ventana_checadaX.imgx = ImageTk.PhotoImage(self.ventana_checadaX.imgx)
                self.ventana_checadaX.tomarhuellabtn = Button( self.ventana_checadaX, width=180, height=55, image=self.ventana_checadaX.imgx, command=lambda:self.ventana_huellax(evento), borderwidth=0)
                self.ventana_checadaX.tomarhuellabtn.place(x=550, y=190)
                #
                self.ventana_checadaX.imgxx = Image.open("imagenes/lectortarjeta.png")
                self.ventana_checadaX.imgxx = self.ventana_checadaX.imgxx.resize((180, 55), Image.ANTIALIAS)
                self.ventana_checadaX.imgxx = ImageTk.PhotoImage(self.ventana_checadaX.imgxx)
                self.ventana_checadaX.lectorbtn = Button( self.ventana_checadaX, width=180, height=55, image=self.ventana_checadaX.imgxx, command=lambda:self.ventana_tarjeta(evento), borderwidth=0)
                self.ventana_checadaX.lectorbtn.place(x=550, y=250)
                #
                self.ventana_checadaX.img5 = Image.open("imagenes/regresarbtn.png")
                self.ventana_checadaX.img5 = self.ventana_checadaX.img5.resize(
                            (50, 50), Image.ANTIALIAS)
                self.ventana_checadaX.img5 = ImageTk.PhotoImage(self.ventana_checadaX.img5)
                self.ventana_checadaX.regreso_btn = Button( self.ventana_checadaX, width=50, height=50, image=self.ventana_checadaX.img5, command=quit_ventana_checadaX, borderwidth=0)
                self.ventana_checadaX.regreso_btn.place(x=700, y=400)
                #
                self.revisar_hora(1)
        
        def procesado_dataset(self):
                self.aviso.avisobtn2.config(state='disabled')
                self.aviso.avisobtn.config(state='disabled')
                codapp = codificacion_rostro.CodificadorImagenes()
                codapp.iniciar_codificación(self.aviso.T,self.aviso.progress,self.aviso.avisobtn)
        
        def carga_huella(self):
                numero_empleado= self.numempleado_vtn.numempleado.get()
                #self.numempleado_vtn.destroy() <-- no se destruye porque imprimeros en pantalla lo que tiene que hacer
                if(numero_empleado==""  or len(numero_empleado)!=5):
                        #mbox.showerror("Error 6", "No ingreso un numero de empleado correcto 5 digitos",parent=self.numempleado_vtn)
                        self.crear_cuadro_error("No ingreso un numero de empleado correcto")
                else:
                        for x in range(0,3):
                                try:
                                        print("Intentando conectar al scanner")
                                        self.numempleado_vtn.T.insert(END, "Iniciando carga... \n")
                                        self.numempleado_vtn.T.see(END)
                                        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                                        
                                        if ( f.verifyPassword() == False ):
                                                raise ValueError('La contraseña del sensor no es correcta!')
                                                self.numempleado_vtn.T.insert(END, "Error: la contraseña del scanner no es correcta \n")
                                                self.numempleado_vtn.T.see(END)
                                                self.numempleado_vtn.T.update_idletasks()
                                        print("Conexion lograda")
                                        self.numempleado_vtn.T.insert(END, "*Conexion lograda*\n")
                                        self.numempleado_vtn.T.see(END)
                                        print('Templates usados: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
                                        try:
                                                print('***Esperando Huella...***')
                                                self.numempleado_vtn.T.insert(END, "***Esperando Huella...***\n")
                                                self.numempleado_vtn.T.see(END)
                                                self.numempleado_vtn.T.update_idletasks()
                                                while ( f.readImage() == False ):
                                                        pass
                                                ret, frame = cap.read()
                                                cv2.imwrite( os.getcwd()+"/fotos_empleados/"+str(numero_empleado)+".png", frame[0:250, 95:300])
                                                print('Descargando imagen (Esto puede tomar tiempo)...')
                                                self.numempleado_vtn.T.insert(END, "Descargando imagen (Esto puede tomar tiempo)...\n")
                                                self.numempleado_vtn.T.see(END)
                                                self.numempleado_vtn.T.update_idletasks()

                                                imageDestination =  os.getcwd() + '/dataset_huella/'+str(x)+'_'+str(numero_empleado)+'.bmp'
                                                f.downloadImage(imageDestination)
                                                #Esto es solo por si se necesita binarizar la imagen dependiendo del caso
                                                print('The image was saved to "' + imageDestination + '".')
                                                #im = cv2.imread(imageDestination)
                                                #im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                                                #th, im_gray_th_otsu = cv2.threshold(im_gray,  110, 255, cv2.THRESH_BINARY)
                                                #print("th"+str(th)) 
                                                #cv2.imwrite(imageDestination, im_gray_th_otsu)

                                        except Exception as e:
                                                print('Operacion Fallida!')
                                                print('Mensage de Error: ' + str(e))
                                                self.numempleado_vtn.T.insert(END, "Error:"+str(e)+"\n")
                                                self.numempleado_vtn.T.see(END)
                                                self.numempleado_vtn.T.update_idletasks()
                                        
                                except Exception as e:
                                        print('El sensor no pudo inicializarse!')
                                        print('Mensage de Error: ' + str(e))
                                        self.numempleado_vtn.T.insert(END, "Error:"+str(e)+"\n")
                                        self.numempleado_vtn.T.see(END)
                                        self.numempleado_vtn.T.update_idletasks()
                        print('Fin del registro!') 
                        self.numempleado_vtn.T.insert(END, 'Fin del registro!'+"\n")
                        self.numempleado_vtn.T.see(END)
                                        
        def carga_nfc(self):
                numero_empleado= self.numempleado_vtn.numempleado.get()
                #self.numempleado_vtn.destroy() <-- no se destruye porque imprimeros en pantalla lo que tiene que hacer
                if(numero_empleado==""  or len(numero_empleado)!=5):
                        #mbox.showerror("Error 7", "No ingreso un numero de empleado correcto 5 digitos",parent=self.numempleado_vtn)
                        self.crear_cuadro_error("No ingreso un numero de empleado correcto")
                else:
                    self.numempleado_vtn.T.insert(END, "Inicio registro NFC \n")
                    self.numempleado_vtn.T.see(END)
                    nfc=Controlador_NFC()
                    ret, frame = cap.read()
                    err = nfc.escribir_tarjeta(numero_empleado,frame)
                    if err ==1:
                        self.numempleado_vtn.T.insert(END, "HUBO UN ERROR EN EL PROCESO... \n")
                    self.numempleado_vtn.T.insert(END, "Fin del proceso... \n")
                    self.numempleado_vtn.T.see(END)

                               
                                
                        
                
        def carga_de_dataset(self):
                self.contador = 0
                #self.registro_vtn.numempleado.config(state='normal')
                self.aviso = Tk()
                # self.aviso = Toplevel(self)
                self.aviso.geometry("500x400")
                self.aviso.attributes("-topmost", True)
                self.aviso.title("IMPORTANTE")
                self.aviso.label = Label(self.aviso, text="¿Quieres realizar el procesado de fotos?", padx=50, pady=50)
                self.aviso.label.pack()
                self.aviso.avisobtn2 = Button( self.aviso, width=10, height=5, text="Aceptar", command=self.procesado_dataset, borderwidth=1)
                """ self.aviso.avisobtn2.place(x=10, y=80) """
                self.aviso.avisobtn2.place(x=130,y=290)
                self.aviso.avisobtn = Button( self.aviso, width=10, height=5, text="Cancelar", command=quit_aviso, borderwidth=1)
                self.aviso.avisobtn.place(x=280,y=290)
                """ self.aviso.avisobtn.place(x=100, y=80) """
                
                self.aviso.T = Text(self.aviso, height=7, width=50)
                self.aviso.T.pack()
                self.aviso.T.insert(END, "Iniciando carga... \n")
                self.aviso.progress = ttk.Progressbar(self.aviso, orient = HORIZONTAL,  length = 500, mode = 'determinate') 
                self.aviso.progress.pack()

        def borrar_foto(self):
                if(self.numero_empleado!=""):
                        direccion = os.getcwd()
                        direccion = direccion+"/dataset/"+self.numero_empleado
                        if os.path.exists(direccion) and os.listdir(direccion)!=0 and self.contador>0:
                            self.contador= self.contador-1
                            os.remove(direccion+"/"+str(self.contador)+".png")
                            self.vartxt.set("Fotos "+str(self.contador)+" /8")
                            print("BORRANDO: "+str(self.contador))

        def tomar_foto(self,numero_empleado):
                # obtener numero de empleado
                self.numero_empleado = numero_empleado
                print("aaaaaaaa "+self.numero_empleado)
                if self.numero_empleado == "":
                    self.crear_cuadro_error("No se ha ingresado un numero de empleado")
                else:
                    #self.registro_vtn.numempleado.config(state='disabled')
                    ret, frame = cap.read()
                    # primero crear carpeta si ya existe borrarla y volverla a hacer
                    direccion = os.getcwd()
                    uniqueid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    direccion = direccion+"/dataset/"+self.numero_empleado
                    if self.contador != 8:
                        if os.path.exists(direccion) and os.listdir(direccion)!=0:
                            for x in os.listdir(direccion):
                                print(x)
                        else:
                            os.mkdir(direccion)
                        if self.contador==1:
                            direccion2 = os.getcwd()
                            """ (125, 5), (275, 235) """
                            cv2.imwrite(direccion2+"/fotos_empleados/"+str(self.numero_empleado)+".png", frame[0:400, 100:400])
                        cv2.imwrite(direccion+"/"+str(self.contador)+".png", frame)
                        print("Foto tomada"+str(self.contador)+".png")
                        self.contador = self.contador+1
                        self.vartxt.set("Fotos "+str(self.contador)+" /8")
                        print(self.vartxt.get())
                    else:
                        self.crear_cuadro_error("Ya se han tomado todas las fotos")

        def ventana_registro(self):
                numero_empleado= self.numempleado_vtn.numempleado.get()
                #self.numempleado_vtn.destroy()
                if(numero_empleado=="" or len(numero_empleado)!=5 ):
                        #mbox.showerror("Error 8", "Numero de empleado no valido, ingrese 5 digitos",parent=self.numempleado_vtn) 
                        self.crear_cuadro_error("NUmero de empleado no valido")
                else:
                        self.numempleado_vtn.destroy()
                        print(numero_empleado)
                        self.registro_vtn = Toplevel(self)
                        self.registro_vtn.geometry("+{}+{}".format(0, 0))
                        self.registro_vtn.overrideredirect(True)
                        self.registro_vtn.title("Registro de Empleado")
                        self.registro_vtn.canvas = Canvas(self.registro_vtn, bg="red", width=800, height=480)
                        self.registro_vtn.canvas.pack()
                        self.registro_vtn.bind('<Escape>', lambda e: root.quit())
                        self.registro_vtn.portada = Image.open("imagenes/fondo_negro.png")
                        self.registro_vtn.portada2 = self.registro_vtn.portada.resize((800, 480), Image.ANTIALIAS)
                        self.registro_vtn.fondo_config = ImageTk.PhotoImage(self.registro_vtn.portada2)
                        self.registro_vtn.canvas.create_image(400, 240, image=self.registro_vtn.fondo_config)
                        # Estado de la ventana
                        '''self.registro_vtn.numempleado = Entry(self.registro_vtn, width=50)
                        self.registro_vtn.numempleado.place(x=200, y=100)
                        self.registro_vtn.label1 = Label(
                            self.registro_vtn, text="Ingrese el número de empleado", font="Verdana 18 bold", fg="white", bg="black")
                        self.registro_vtn.label1.place(x=190, y=50)'''

                        self.registro_vtn.img = Image.open("imagenes/finalizarbtn.png")
                        self.registro_vtn.img = self.registro_vtn.img.resize((180, 50), Image.ANTIALIAS)
                        self.registro_vtn.img = ImageTk.PhotoImage(self.registro_vtn.img)
                        self.registro_vtn.siguientebtn = Button(self.registro_vtn, width=180, height=55, image=self.registro_vtn.img, command=self.carga_de_dataset, borderwidth=0)
                        self.registro_vtn.siguientebtn.place(x=550, y=290)
                        
                        # Sección para poner botones
                        self.registro_vtn.img2 = Image.open("imagenes/tomar_fotobtn.png")
                        self.registro_vtn.img2 = self.registro_vtn.img2.resize(
                            (180, 55), Image.ANTIALIAS)
                        self.registro_vtn.img2 = ImageTk.PhotoImage(self.registro_vtn.img2)
                        self.registro_vtn.tomarfotobtn = Button(
                            self.registro_vtn, width=180, height=55, image=self.registro_vtn.img2, command= lambda: self.tomar_foto(numero_empleado), borderwidth=0)
                        self.registro_vtn.tomarfotobtn.place(x=550, y=150)
                        #
                        self.registro_vtn.img4 = Image.open("imagenes/borrat_anteriorbtn.png")
                        self.registro_vtn.img4 = self.registro_vtn.img4.resize(
                            (180, 55), Image.ANTIALIAS)
                        self.registro_vtn.img4 = ImageTk.PhotoImage(self.registro_vtn.img4)
                        self.registro_vtn.tomarfotobtn = Button(
                            self.registro_vtn, width=180, height=55, image=self.registro_vtn.img4, command=self.borrar_foto, borderwidth=0)
                        self.registro_vtn.tomarfotobtn.place(x=550, y=220)
                        #LABEL
                        self.registro_vtn.contador = 0
                        self.registro_vtn.label2 = Label( self.registro_vtn, textvariable = self.numero_empleado, bg="black", fg="white", font="Verdana 14 bold")
                        self.registro_vtn.label = Label( self.registro_vtn, textvariable = self.vartxt, bg="black", fg="white", font="Verdana 14 bold")
                        self.vartxt.set("Tome 8 fotos")
                        self.registro_vtn.label.place(x=15, y=300)
                        #boton regresar
                        self.registro_vtn.img5 = Image.open("imagenes/regresarbtn.png")
                        self.registro_vtn.img5 = self.registro_vtn.img5.resize(
                            (50, 50), Image.ANTIALIAS)
                        self.registro_vtn.img5 = ImageTk.PhotoImage(self.registro_vtn.img5)
                        self.registro_vtn.regreso_btn = Button(
                            self.registro_vtn, width=50, height=50, image=self.registro_vtn.img5, command=quit_registro_vtn, borderwidth=0)
                        self.registro_vtn.regreso_btn.place(x=700, y=400)

                        # CAMARA OPENCV
                        self.cap = cap
                        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                        self.interval = 20

                        self.registro_vtn.canvascv = Canvas(self.registro_vtn, width=400, height=240)
                        self.registro_vtn.canvascv.place(x=15, y=100)
                        self.actualizar_imagen()

        def actualizar_imagenhuella(self):
                self.numempleado_vtn.image2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
                width = int(self.numempleado_vtn.image2.shape[1] * scale_percent / 100)
                height = int(self.numempleado_vtn.image2.shape[0] * scale_percent / 100)
                dsize = (200, 120)
                self.numempleado_vtn.image2 = cv2.resize(self.numempleado_vtn.image2, dsize)
                cv2.rectangle(self.numempleado_vtn.image2, (50, 5), (135, 116), (0, 255, 0), 4)
                self.numempleado_vtn.image2 = Image.fromarray(self.numempleado_vtn.image2)
                self.numempleado_vtn.image2 = ImageTk.PhotoImage(self.numempleado_vtn.image2)
                self.numempleado_vtn.canvascv.create_image( 0, 0, anchor=NW, image=self.numempleado_vtn.image2)
                self.numempleado_vtn.after(20, self.actualizar_imagenhuella)

        def actualizar_imagen(self):
                self.image2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
                width = int(self.image2.shape[1] * scale_percent / 100)
                height = int(self.image2.shape[0] * scale_percent / 100)
                dsize = (400, 240)
                self.image2 = cv2.resize(self.image2, dsize)
                cv2.rectangle(self.image2, (125, 5), (275, 235), (0, 255, 0), 4)
                self.image2 = Image.fromarray(self.image2)
                self.image2 = ImageTk.PhotoImage(self.image2)
                self.registro_vtn.canvascv.create_image( 0, 0, anchor=NW, image=self.image2)
                self.registro_vtn.after(20, self.actualizar_imagen)
        
        
        def ventana_entrar(self):
                self.entrada_vtn = Toplevel(self)
                self.entrada_vtn.geometry("+{}+{}".format(0, 0)) 
                self.entrada_vtn.overrideredirect(True)
                self.entrada_vtn.title("Registro de Empleado")
                self.entrada_vtn.canvas = Canvas(
                    self.entrada_vtn, bg="red", width=800, height=480)
                self.entrada_vtn.canvas.pack() 
                self.entrada_vtn.bind('<Escape>', lambda e: root.quit())
                self.entrada_vtn.portada = Image.open("imagenes/fondo_negro.png")
                self.entrada_vtn.portada2 = self.entrada_vtn.portada.resize((800, 480), Image.ANTIALIAS)
                self.entrada_vtn.fondo_config = ImageTk.PhotoImage(self.entrada_vtn.portada2)
                self.entrada_vtn.canvas.create_image(400, 240, image=self.entrada_vtn.fondo_config)
                self.entrada_vtn.numempleado = Entry(self.entrada_vtn, show="*", width=50)
                self.entrada_vtn.numempleado.place(x=100, y=100)
                self.entrada_vtn.label1 = Label(
                    self.entrada_vtn, text="Ingrese código de acceso", font="Verdana 18 bold", fg="white", bg="black")
                self.entrada_vtn.label1.place(x=100, y=50)
                
                self.entrada_vtn.imgrostro = Image.open("imagenes/ingresarclave.png")
                self.entrada_vtn.imgrostro = self.entrada_vtn.imgrostro.resize((180, 50), Image.ANTIALIAS)
                self.entrada_vtn.imgrostro = ImageTk.PhotoImage(self.entrada_vtn.imgrostro)
                self.entrada_vtn.rostrobtn = Button(self.entrada_vtn, width=180, height=55, image=self.entrada_vtn.imgrostro, command=self.ventana_Configuracion, borderwidth=0)
                self.entrada_vtn.rostrobtn.place(x=550, y=90) 
                
                self.entrada_vtn.img5 = Image.open("imagenes/regresarbtn.png")
                self.entrada_vtn.img5 = self.entrada_vtn.img5.resize(
                            (50, 50), Image.ANTIALIAS)
                self.entrada_vtn.img5 = ImageTk.PhotoImage(self.entrada_vtn.img5)
                self.entrada_vtn.regreso_btn = Button(
                            self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.img5, command=quit_entrada_vtn, borderwidth=0)
                self.entrada_vtn.regreso_btn.place(x=700, y=400)
                #botones
                self.entrada_vtn.im1 = Image.open("imagenes/0.png")
                self.entrada_vtn.im1 = self.entrada_vtn.im1.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im1 = ImageTk.PhotoImage(self.entrada_vtn.im1)
                self.entrada_vtn.btn1 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im1, command=lambda:self.ingresar_caracterentrada("0"), borderwidth=0)
                self.entrada_vtn.btn1.place(x=100, y=280)
                #
                self.entrada_vtn.im2 = Image.open("imagenes/1.png")
                self.entrada_vtn.im2 = self.entrada_vtn.im2.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im2 = ImageTk.PhotoImage(self.entrada_vtn.im2)
                self.entrada_vtn.btn2 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im2, command=lambda:self.ingresar_caracterentrada("1"), borderwidth=0)
                self.entrada_vtn.btn2.place(x=200, y=280)
                #
                self.entrada_vtn.im3 = Image.open("imagenes/2.png")
                self.entrada_vtn.im3 = self.entrada_vtn.im3.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im3 = ImageTk.PhotoImage(self.entrada_vtn.im3)
                self.entrada_vtn.btn3 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im3, command=lambda:self.ingresar_caracterentrada("2"), borderwidth=0)
                self.entrada_vtn.btn3.place(x=300, y=280)
                #
                self.entrada_vtn.im4 = Image.open("imagenes/3.png")
                self.entrada_vtn.im4 = self.entrada_vtn.im4.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im4 = ImageTk.PhotoImage(self.entrada_vtn.im4)
                self.entrada_vtn.btn4 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im4, command=lambda:self.ingresar_caracterentrada("3"), borderwidth=0)
                self.entrada_vtn.btn4.place(x=400, y=280)
                #
                self.entrada_vtn.im5 = Image.open("imagenes/4.png")
                self.entrada_vtn.im5 = self.entrada_vtn.im5.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im5 = ImageTk.PhotoImage(self.entrada_vtn.im5)
                self.entrada_vtn.btn5 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im5, command=lambda:self.ingresar_caracterentrada("4"), borderwidth=0)
                self.entrada_vtn.btn5.place(x=100, y=340)
                #
                self.entrada_vtn.im6 = Image.open("imagenes/5.png")
                self.entrada_vtn.im6 = self.entrada_vtn.im6.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im6 = ImageTk.PhotoImage(self.entrada_vtn.im6)
                self.entrada_vtn.btn6 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im6, command=lambda:self.ingresar_caracterentrada("5"), borderwidth=0)
                self.entrada_vtn.btn6.place(x=200, y=340)
                #
                self.entrada_vtn.im7 = Image.open("imagenes/6.png")
                self.entrada_vtn.im7 = self.entrada_vtn.im7.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im7 = ImageTk.PhotoImage(self.entrada_vtn.im7)
                self.entrada_vtn.btn7 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im7,command=lambda:self.ingresar_caracterentrada("6"), borderwidth=0)
                self.entrada_vtn.btn7.place(x=300, y=340)
                #
                self.entrada_vtn.im8 = Image.open("imagenes/7.png")
                self.entrada_vtn.im8 = self.entrada_vtn.im8.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im8 = ImageTk.PhotoImage(self.entrada_vtn.im8)
                self.entrada_vtn.btn8 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im8, command=lambda:self.ingresar_caracterentrada("7"), borderwidth=0)
                self.entrada_vtn.btn8.place(x=400, y=340)
                #
                self.entrada_vtn.im9 = Image.open("imagenes/8.png")
                self.entrada_vtn.im9 = self.entrada_vtn.im9.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im9 = ImageTk.PhotoImage(self.entrada_vtn.im9)
                self.entrada_vtn.btn9 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im9, command=lambda:self.ingresar_caracterentrada("8"), borderwidth=0)
                self.entrada_vtn.btn9.place(x=100, y=400)
                #
                self.entrada_vtn.im10 = Image.open("imagenes/9.png")
                self.entrada_vtn.im10 = self.entrada_vtn.im10.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.im10 = ImageTk.PhotoImage(self.entrada_vtn.im10)
                self.entrada_vtn.btn10 = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.im10, command=lambda:self.ingresar_caracterentrada("9"), borderwidth=0)
                self.entrada_vtn.btn10.place(x=200, y=400)
                #
                self.entrada_vtn.sprbtn = Image.open("imagenes/supr.png")
                self.entrada_vtn.sprbtn = self.entrada_vtn.sprbtn.resize((50, 50), Image.ANTIALIAS)
                self.entrada_vtn.sprbtn = ImageTk.PhotoImage(self.entrada_vtn.sprbtn)
                self.entrada_vtn.spr_btn = Button(self.entrada_vtn, width=50, height=50, image=self.entrada_vtn.sprbtn, command=lambda:self.ingresar_caracterentrada("x"), borderwidth=0)
                self.entrada_vtn.spr_btn.place(x=300, y=400)
                

        
        def ventana_numempleado(self,opc):
                self.numempleado_vtn = Toplevel(self)
                self.numempleado_vtn.geometry("+{}+{}".format(0, 0)) 
                self.numempleado_vtn.overrideredirect(True)
                self.numempleado_vtn.title("Registro de Empleado")
                self.numempleado_vtn.canvas = Canvas(
                    self.numempleado_vtn, bg="red", width=800, height=480)
                self.numempleado_vtn.canvas.pack()
                self.numempleado_vtn.T = Text(self.numempleado_vtn, height=7, width=50)
                self.numempleado_vtn.T.place(x=100,y=130)
                self.numempleado_vtn.T.insert(END, "Iniciando carga... \n")
                self.numempleado_vtn.T.see(END)
                self.numempleado_vtn.bind('<Escape>', lambda e: root.quit())
                self.numempleado_vtn.portada = Image.open("imagenes/fondo_negro.png")
                self.numempleado_vtn.portada2 = self.numempleado_vtn.portada.resize((800, 480), Image.ANTIALIAS)
                self.numempleado_vtn.fondo_config = ImageTk.PhotoImage(self.numempleado_vtn.portada2)
                self.numempleado_vtn.canvas.create_image(400, 240, image=self.numempleado_vtn.fondo_config)
                self.numempleado_vtn.numempleado = Entry(self.numempleado_vtn, width=50)
                self.numempleado_vtn.numempleado.place(x=100, y=100)
                self.numempleado_vtn.label1 = Label(
                    self.numempleado_vtn, text="Ingrese el número de empleado", font="Verdana 18 bold", fg="white", bg="black")
                self.numempleado_vtn.label1.place(x=150, y=50)
                
                self.numempleado_vtn.imgrostro = Image.open("imagenes/registrorostror.png")
                self.numempleado_vtn.imgrostro = self.numempleado_vtn.imgrostro.resize((180, 50), Image.ANTIALIAS)
                self.numempleado_vtn.imgrostro = ImageTk.PhotoImage(self.numempleado_vtn.imgrostro)
                self.numempleado_vtn.rostrobtn = Button(self.numempleado_vtn, width=180, height=55, image=self.numempleado_vtn.imgrostro, command=self.ventana_registro, borderwidth=0)
                self.numempleado_vtn.rostrobtn.place(x=550, y=90)
                
                self.numempleado_vtn.imghuella = Image.open("imagenes/registrohuella.png")
                self.numempleado_vtn.imghuella = self.numempleado_vtn.imghuella.resize((180, 50), Image.ANTIALIAS)
                self.numempleado_vtn.imghuella = ImageTk.PhotoImage(self.numempleado_vtn.imghuella)
                self.numempleado_vtn.huellabtn = Button(self.numempleado_vtn, width=180, height=55, image=self.numempleado_vtn.imghuella, command=self.carga_huella, borderwidth=0)
                self.numempleado_vtn.huellabtn.place(x=550, y=160)

                self.numempleado_vtn.nfcbtn = Image.open("imagenes/lectortarjeta.png")
                self.numempleado_vtn.nfcbtn = self.numempleado_vtn.nfcbtn.resize((180, 50), Image.ANTIALIAS)
                self.numempleado_vtn.nfcbtn = ImageTk.PhotoImage(self.numempleado_vtn.nfcbtn)
                self.numempleado_vtn.nfcb = Button(self.numempleado_vtn, width=180, height=55, image=self.numempleado_vtn.nfcbtn, command=self.carga_nfc, borderwidth=0)
                self.numempleado_vtn.nfcb.place(x=550, y=230)
                
                self.numempleado_vtn.img5 = Image.open("imagenes/regresarbtn.png")
                self.numempleado_vtn.img5 = self.numempleado_vtn.img5.resize(
                            (50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.img5 = ImageTk.PhotoImage(self.numempleado_vtn.img5)
                self.numempleado_vtn.regreso_btn = Button(
                            self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.img5, command=quit_numempleado_vtn, borderwidth=0)
                self.numempleado_vtn.regreso_btn.place(x=700, y=400)
                #botones
                self.numempleado_vtn.im1 = Image.open("imagenes/0.png")
                self.numempleado_vtn.im1 = self.numempleado_vtn.im1.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im1 = ImageTk.PhotoImage(self.numempleado_vtn.im1)
                self.numempleado_vtn.btn1 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im1, command=lambda:self.ingresar_caracterregistro("0"), borderwidth=0)
                self.numempleado_vtn.btn1.place(x=100, y=280)
                #
                self.numempleado_vtn.im2 = Image.open("imagenes/1.png")
                self.numempleado_vtn.im2 = self.numempleado_vtn.im2.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im2 = ImageTk.PhotoImage(self.numempleado_vtn.im2)
                self.numempleado_vtn.btn2 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im2, command=lambda:self.ingresar_caracterregistro("1"), borderwidth=0)
                self.numempleado_vtn.btn2.place(x=200, y=280)
                #
                self.numempleado_vtn.im3 = Image.open("imagenes/2.png")
                self.numempleado_vtn.im3 = self.numempleado_vtn.im3.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im3 = ImageTk.PhotoImage(self.numempleado_vtn.im3)
                self.numempleado_vtn.btn3 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im3, command=lambda:self.ingresar_caracterregistro("2"), borderwidth=0)
                self.numempleado_vtn.btn3.place(x=300, y=280)
                #
                self.numempleado_vtn.im4 = Image.open("imagenes/3.png")
                self.numempleado_vtn.im4 = self.numempleado_vtn.im4.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im4 = ImageTk.PhotoImage(self.numempleado_vtn.im4)
                self.numempleado_vtn.btn4 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im4, command=lambda:self.ingresar_caracterregistro("3"), borderwidth=0)
                self.numempleado_vtn.btn4.place(x=400, y=280)
                #
                self.numempleado_vtn.im5 = Image.open("imagenes/4.png")
                self.numempleado_vtn.im5 = self.numempleado_vtn.im5.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im5 = ImageTk.PhotoImage(self.numempleado_vtn.im5)
                self.numempleado_vtn.btn5 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im5, command=lambda:self.ingresar_caracterregistro("4"), borderwidth=0)
                self.numempleado_vtn.btn5.place(x=100, y=340)
                #
                self.numempleado_vtn.im6 = Image.open("imagenes/5.png")
                self.numempleado_vtn.im6 = self.numempleado_vtn.im6.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im6 = ImageTk.PhotoImage(self.numempleado_vtn.im6)
                self.numempleado_vtn.btn6 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im6, command=lambda:self.ingresar_caracterregistro("5"), borderwidth=0)
                self.numempleado_vtn.btn6.place(x=200, y=340)
                #
                self.numempleado_vtn.im7 = Image.open("imagenes/6.png")
                self.numempleado_vtn.im7 = self.numempleado_vtn.im7.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im7 = ImageTk.PhotoImage(self.numempleado_vtn.im7)
                self.numempleado_vtn.btn7 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im7,command=lambda:self.ingresar_caracterregistro("6"), borderwidth=0)
                self.numempleado_vtn.btn7.place(x=300, y=340)
                #
                self.numempleado_vtn.im8 = Image.open("imagenes/7.png")
                self.numempleado_vtn.im8 = self.numempleado_vtn.im8.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im8 = ImageTk.PhotoImage(self.numempleado_vtn.im8)
                self.numempleado_vtn.btn8 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im8, command=lambda:self.ingresar_caracterregistro("7"), borderwidth=0)
                self.numempleado_vtn.btn8.place(x=400, y=340)
                #
                self.numempleado_vtn.im9 = Image.open("imagenes/8.png")
                self.numempleado_vtn.im9 = self.numempleado_vtn.im9.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im9 = ImageTk.PhotoImage(self.numempleado_vtn.im9)
                self.numempleado_vtn.btn9 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im9, command=lambda:self.ingresar_caracterregistro("8"), borderwidth=0)
                self.numempleado_vtn.btn9.place(x=100, y=400)
                #
                self.numempleado_vtn.im10 = Image.open("imagenes/9.png")
                self.numempleado_vtn.im10 = self.numempleado_vtn.im10.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.im10 = ImageTk.PhotoImage(self.numempleado_vtn.im10)
                self.numempleado_vtn.btn10 = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.im10, command=lambda:self.ingresar_caracterregistro("9"), borderwidth=0)
                self.numempleado_vtn.btn10.place(x=200, y=400)
                #
                self.numempleado_vtn.sprbtn = Image.open("imagenes/supr.png")
                self.numempleado_vtn.sprbtn = self.numempleado_vtn.sprbtn.resize((50, 50), Image.ANTIALIAS)
                self.numempleado_vtn.sprbtn = ImageTk.PhotoImage(self.numempleado_vtn.sprbtn)
                self.numempleado_vtn.spr_btn = Button(self.numempleado_vtn, width=50, height=50, image=self.numempleado_vtn.sprbtn, command=lambda:self.ingresar_caracterregistro("x"), borderwidth=0)
                self.numempleado_vtn.spr_btn.place(x=300, y=400)
                #
                self.numempleado_vtn.canvascv = Canvas(self.numempleado_vtn, width=200, height=120)
                self.numempleado_vtn.canvascv.place(x=480, y=350)
                self.actualizar_imagenhuella()
                
        def generar_reportes(self,fecha1,fecha2):
            print("Generando reporte... de "+fecha1+" a "+fecha2)
            bd = BaseDeDatos("127.0.0.1","root","normanmx2020","checador_db",3306)
            x, e = bd.obtenerChecadas(fecha1,fecha2)
            if x == -1:
                self.ventana_reportes_vtn.T.insert(END, "Hubo un error no se pudieron descargar las checadas\n")
                self.ventana_reportes_vtn.T.insert(END, "Error:"+e+"\n")
                self.ventana_reportes_vtn.T.see(END)
            else:
                self.ventana_reportes_vtn.T.insert(END, "Operación exitosa...\n")
                self.ventana_reportes_vtn.T.see(END)

            

        def ventana_reportes(self):
            self.ventana_reportes_vtn = Toplevel(self)
            self.ventana_reportes_vtn.geometry("+{}+{}".format(0, 0)) 
            self.ventana_reportes_vtn.overrideredirect(True)
            self.ventana_reportes_vtn.title("Registro de Empleado")
            self.ventana_reportes_vtn.canvas = Canvas(
                    self.ventana_reportes_vtn, bg="red", width=800, height=480)
            self.ventana_reportes_vtn.canvas.pack()
            self.ventana_reportes_vtn.bind('<Escape>', lambda e: root.quit())
            self.ventana_reportes_vtn.portada = Image.open("imagenes/fondo_negro.png")
            self.ventana_reportes_vtn.portada2 = self.ventana_reportes_vtn.portada.resize((800, 480), Image.ANTIALIAS)
            self.ventana_reportes_vtn.fondo_config = ImageTk.PhotoImage(self.ventana_reportes_vtn.portada2)
            self.ventana_reportes_vtn.canvas.create_image(400, 240, image=self.ventana_reportes_vtn.fondo_config)
            #Calendario obtener fecha
            x = datetime.datetime.now()
            self.ventana_reportes_vtn.fecha1 = Calendar(self.ventana_reportes_vtn, selectmode="day",year=x.year, month=x.month,day=x.day)
            self.ventana_reportes_vtn.fecha1.place(x=100, y=100)

            self.ventana_reportes_vtn.label1 = Label(
                    self.ventana_reportes_vtn, text="Seleccione el rango de fechas para obtener las checadas", font="Verdana 18 bold", fg="white", bg="black")
            self.ventana_reportes_vtn.label1.place(x=150, y=50)
            #
            self.ventana_reportes_vtn.fecha2 = Calendar(self.ventana_reportes_vtn, selectmode="day",year=x.year, month=x.month,day=x.day)
            self.ventana_reportes_vtn.fecha2.place(x=400, y=100)
            #
            self.ventana_reportes_vtn.T = Text(self.ventana_reportes_vtn, height=7, width=60)
            self.ventana_reportes_vtn.T.place(x=100,y=350)
            self.ventana_reportes_vtn.T.insert(END, "Esperando las fechas para obtener las checadas...\n")
            self.ventana_reportes_vtn.T.see(END)
            #
            self.ventana_reportes_vtn.img5x = Image.open("imagenes/obtenerreporte2.png")
            self.ventana_reportes_vtn.img5x = self.ventana_reportes_vtn.img5x.resize( 
                            (200, 60), Image.ANTIALIAS)
            self.ventana_reportes_vtn.img5x = ImageTk.PhotoImage(self.ventana_reportes_vtn.img5x)
            self.ventana_reportes_vtn.regreso_btn = Button(
                            self.ventana_reportes_vtn, width=200, height=60, image=self.ventana_reportes_vtn.img5x, command=lambda: self.generar_reportes(str(self.ventana_reportes_vtn.fecha1.selection_get()),str(self.ventana_reportes_vtn.fecha2.selection_get())), borderwidth=0)
            self.ventana_reportes_vtn.regreso_btn.place(x=585, y=300)

            self.ventana_reportes_vtn.img5 = Image.open("imagenes/regresarbtn.png")
            self.ventana_reportes_vtn.img5 = self.ventana_reportes_vtn.img5.resize( 
                            (50, 50), Image.ANTIALIAS)
            self.ventana_reportes_vtn.img5 = ImageTk.PhotoImage(self.ventana_reportes_vtn.img5)
            self.ventana_reportes_vtn.regreso_btn = Button(
                            self.ventana_reportes_vtn, width=50, height=50, image=self.ventana_reportes_vtn.img5, command=quit_ventana_reportes_vtn, borderwidth=0)
            self.ventana_reportes_vtn.regreso_btn.place(x=700, y=400)


        def ventana_cambio_numero(self):
            self.cambio_empleado_vtn = Toplevel(self)
            self.cambio_empleado_vtn.geometry("+{}+{}".format(0, 0)) 
            self.cambio_empleado_vtn.overrideredirect(True)
            self.cambio_empleado_vtn.title("Registro de Empleado")
            self.cambio_empleado_vtn.canvas = Canvas(
                    self.cambio_empleado_vtn, bg="red", width=800, height=480)
            self.cambio_empleado_vtn.canvas.pack()
            self.cambio_empleado_vtn.bind('<Escape>', lambda e: root.quit())
            self.cambio_empleado_vtn.portada = Image.open("imagenes/fondo_negro.png")
            self.cambio_empleado_vtn.portada2 = self.cambio_empleado_vtn.portada.resize((800, 480), Image.ANTIALIAS)
            self.cambio_empleado_vtn.fondo_config = ImageTk.PhotoImage(self.cambio_empleado_vtn.portada2)
            self.cambio_empleado_vtn.canvas.create_image(400, 240, image=self.cambio_empleado_vtn.fondo_config)
            self.cambio_empleado_vtn.numempleado = Entry(self.cambio_empleado_vtn, width=30)
            self.cambio_empleado_vtn.numempleado.place(x=100, y=100)
            self.cambio_empleado_vtn.label1 = Label(
                    self.cambio_empleado_vtn, text="Cambio de numero de empleado", font="Verdana 18 bold", fg="white", bg="black")
            self.cambio_empleado_vtn.label1.place(x=150, y=50)
            #
            self.cambio_empleado_vtn.numempleado2 = Entry(self.cambio_empleado_vtn, width=30)
            self.cambio_empleado_vtn.numempleado2.place(x=400, y=100)
            #
            self.cambio_empleado_vtn.T = Text(self.cambio_empleado_vtn, height=7, width=60)
            self.cambio_empleado_vtn.T.place(x=100,y=150)
            self.cambio_empleado_vtn.T.insert(END, "Ingrese el antiguo y despues el nuevo numero de empleado\n")
            self.cambio_empleado_vtn.T.see(END)
            #
            self.cambio_empleado_vtn.img5x = Image.open("imagenes/cambiarempleado.png")
            self.cambio_empleado_vtn.img5x = self.cambio_empleado_vtn.img5x.resize( 
                            (200, 60), Image.ANTIALIAS)
            self.cambio_empleado_vtn.img5x = ImageTk.PhotoImage(self.cambio_empleado_vtn.img5x)
            self.cambio_empleado_vtn.regreso_btn = Button(
                            self.cambio_empleado_vtn, width=200, height=60, image=self.cambio_empleado_vtn.img5x, command=self.cambio_de_numero, borderwidth=0)
            self.cambio_empleado_vtn.regreso_btn.place(x=600, y=250)

            self.cambio_empleado_vtn.img5 = Image.open("imagenes/regresarbtn.png")
            self.cambio_empleado_vtn.img5 = self.cambio_empleado_vtn.img5.resize( 
                            (50, 50), Image.ANTIALIAS)
            self.cambio_empleado_vtn.img5 = ImageTk.PhotoImage(self.cambio_empleado_vtn.img5)
            self.cambio_empleado_vtn.regreso_btn = Button(
                            self.cambio_empleado_vtn, width=50, height=50, image=self.cambio_empleado_vtn.img5, command=quit_cambio_empleado_vtn, borderwidth=0)
            self.cambio_empleado_vtn.regreso_btn.place(x=700, y=400)


        def cambio_de_numero(self):
            numN = self.cambio_empleado_vtn.numempleado2.get()
            numA = self.cambio_empleado_vtn.numempleado.get()
            if numA == "" or  numN == "":
                #mbox.showerror("Error 9", "Ingrese un numero de empleado antiguo y nuevo",parent=self.cambio_empleado_vtn)
                self.crear_cuadro_error("Ingrese 2 numeros de empleados")
            else:
                #CARPETA DE DATASET DE ROSTROS
                try:
                    if os.path.exists(os.getcwd()+"/dataset/"+numA):
                        #src = path.realpath("guru99.txt")
                        os.rename(os.getcwd()+"/dataset/"+numA,os.getcwd()+"/dataset/"+numN)
                        self.cambio_empleado_vtn.T.insert(END, "Cambiado "+os.getcwd()+"/dataset/"+numA+"\n")
                        self.cambio_empleado_vtn.T.insert(END, "por "+os.getcwd()+"/dataset/"+numN+"\n")
                        self.cambio_empleado_vtn.T.see(END)
                    else:
                        print("No se encontro la carpeta")
                        print(os.getcwd()+"/dataset/"+numA)
                        self.cambio_empleado_vtn.T.insert(END, "No se encontro la carpeta\n")
                        self.cambio_empleado_vtn.T.see(END)
                except Exception as e:
                        print('No se realizo el cambio de numero en carpeta rostro')
                        print('Mensaje de Error: ' + str(e))
                #CARPETA DE DATASET DE HUELLAS
                try:
                    for x in range(0,3):
                        if os.path.exists(os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png"):
                            #src = path.realpath("guru99.txt")
                            os.rename(os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png",os.getcwd()+"/dataset_huella/"+str(x)+"_"+numN+".png")
                            self.cambio_empleado_vtn.T.insert(END,"Cambio "+ os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png"+"\n")
                            self.cambio_empleado_vtn.T.insert(END, "por "+os.getcwd()+"/dataset_huella/"+str(x)+"_"+numN+".png"+"\n")
                            self.cambio_empleado_vtn.T.see(END)
                        else:
                            print("No se encontro el achivo")
                            print(os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png")
                            self.cambio_empleado_vtn.T.insert(END, "No se encontro el archivo"+os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png"+"\n")
                            self.cambio_empleado_vtn.T.see(END)
                except Exception as e:
                        print('No se realizo el cambio de numero en carpeta rostro')
                        print('Mensaje de Error: ' + str(e))
                #CARPETA DE DATASET DE FOTOS DE EMPLEADOS
                try:
                    if os.path.exists(os.getcwd()+"/fotos_empleados/"+numA+".png"):
                        #src = path.realpath("guru99.txt")
                        os.rename(os.getcwd()+"/fotos_empleados/"+numA+".png",os.getcwd()+"/fotos_empleados/"+numN+".png")
                        self.cambio_empleado_vtn.T.insert(END, "Cambio "+ os.getcwd()+"/fotos_empleados/"+numA+".png"+"\n")
                        self.cambio_empleado_vtn.T.insert(END, "por "+os.getcwd()+"/fotos_empleados/"+numN+".png"+"\n")
                        self.cambio_empleado_vtn.T.see(END)
                    else:
                        print("No se encontro la foto de empleado")
                        print(os.getcwd()+"/fotos_empleados/"+numA+".png")
                        self.cambio_empleado_vtn.T.insert(END, "No se encontro el archivo"+os.getcwd()+"/dataset_huella/"+str(x)+"_"+numA+".png"+"\n")
                        self.cambio_empleado_vtn.T.see(END)
                except Exception as e:
                        print('No se realizo el cambio de numero en carpeta rostro')
                        print('Mensaje de Error: ' + str(e))



        def ventana_Configuracion(self):
            if self.entrada_vtn.numempleado.get()!="21737590":
                self.crear_cuadro_error("Clave de acceso denegada")
                #mbox.showerror("Error 1", "Clave de acceso denegada",parent=self.entrada_vtn) 
            else:
                # Fondo de pantalla
                self.config_vtn = Toplevel(self)
                self.config_vtn.geometry("+{}+{}".format(0, 0))
                self.config_vtn.overrideredirect(True)
                self.config_vtn.title("Configuraciones")
                self.canvas_config = Canvas(
                    self.config_vtn, bg="white", width=800, height=480)
                self.canvas_config.pack()
                portada = Image.open("imagenes/fondo_secundario.png")
                portada2 = portada.resize((800, 480), Image.ANTIALIAS)
                self.fondo_config = ImageTk.PhotoImage(portada2)
                self.canvas_config.create_image(400, 240, image=self.fondo_config)
                # Estado de la ventana
                print(self.config_vtn.state())
                # IMpresion de los botones
                # REGISTRO DE EMPLEADO
                self.config_vtn.img = Image.open("imagenes/registroempleadobtn.png")
                self.config_vtn.img = self.config_vtn.img.resize(
                    (200, 60), Image.ANTIALIAS)
                self.config_vtn.img = ImageTk.PhotoImage(self.config_vtn.img)
                self.config_vtn.registro_btn = Button(
                    self.config_vtn, width=200, height=60, image=self.config_vtn.img, command= lambda: self.ventana_numempleado(0), borderwidth=0)
                self.config_vtn.registro_btn.place(x=150, y=50)
                #
                self.config_vtn.img2 = Image.open("imagenes/descargabtn.png")
                self.config_vtn.img2 = self.config_vtn.img2.resize(
                    (200, 60), Image.ANTIALIAS)
                self.config_vtn.img2 = ImageTk.PhotoImage(self.config_vtn.img2)
                self.config_vtn.descarga_datos_btn = Button(
                    self.config_vtn, width=200, height=60, image=self.config_vtn.img2, command= lambda:self.ventana_descarga_usb("a"), borderwidth=0)
                self.config_vtn.descarga_datos_btn.place(x=450, y=50)
                # INICIO DESCANSO Y FIN DESCANSO
                self.config_vtn.img3 = Image.open("imagenes/cargabtn.png")
                self.config_vtn.img3 = self.config_vtn.img3.resize(
                    (200, 60), Image.ANTIALIAS)
                self.config_vtn.img3 = ImageTk.PhotoImage(self.config_vtn.img3)
                self.config_vtn.carga_datos_btn = Button(
                    self.config_vtn, width=200, height=60, image=self.config_vtn.img3, command=lambda:  self.ventana_carga_usb("a"), borderwidth=0)
                self.config_vtn.carga_datos_btn.place(x=150, y=150)
                #
                # INICIO DESCANSO Y FIN DESCANSO
                self.config_vtn.img5 = Image.open("imagenes/cambiarempleado.png")
                self.config_vtn.img5 = self.config_vtn.img5.resize(
                    (200, 60), Image.ANTIALIAS)
                self.config_vtn.img5 = ImageTk.PhotoImage(self.config_vtn.img5)
                self.config_vtn.carga_datos_btn = Button(
                    self.config_vtn, width=200, height=60, image=self.config_vtn.img5, command= self.ventana_cambio_numero, borderwidth=0)
                self.config_vtn.carga_datos_btn.place(x=450, y=150)
                #
                self.config_vtn.img6 = Image.open("imagenes/obtenerreporte.png")
                self.config_vtn.img6 = self.config_vtn.img6.resize(
                    (200, 60), Image.ANTIALIAS)
                self.config_vtn.img6 = ImageTk.PhotoImage(self.config_vtn.img6)
                self.config_vtn.carga_datos_btn = Button(
                    self.config_vtn, width=200, height=60, image=self.config_vtn.img6, command= self.ventana_reportes, borderwidth=0)
                self.config_vtn.carga_datos_btn.place(x=150, y=250)
                #
                self.config_vtn.img4 = Image.open("imagenes/regresarbtn.png")
                self.config_vtn.img4 = self.config_vtn.img4.resize(
                    (50, 50), Image.ANTIALIAS)
                self.config_vtn.img4 = ImageTk.PhotoImage(self.config_vtn.img4)
                self.config_vtn.regreso_btn = Button(
                    self.config_vtn, width=50, height=50, image=self.config_vtn.img4, command=quit_config_vtn, borderwidth=0)
                self.config_vtn.regreso_btn.place(x=700, y=400)

        def crear_cuadro_error(self, message):
            self.aviso_error = Toplevel(self)
            self.aviso_error.geometry("+{}+{}".format(0, 0))
            self.aviso_error.overrideredirect(True)
            self.aviso_error.title("Error")
            self.aviso_error.canvas_config = Canvas(self.aviso_error, bg="white", width=500, height=300)
            self.aviso_error.canvas_config.pack()
            portada7 = Image.open("imagenes/fondo_negro.png")
            portada8 = portada7.resize((500, 300), Image.ANTIALIAS)
            self.aviso_error.fondo_config = ImageTk.PhotoImage(portada8)
            self.aviso_error.canvas_config.create_image(250, 150, image=self.aviso_error.fondo_config)
            #
            self.aviso_error.label1 = Label(
            self.aviso_error, text=message, font="Verdana 12 bold", fg="white", bg="black")
            self.aviso_error.label1.place(x=50, y=50)
            #
            self.aviso_error.img = Image.open("imagenes/siguientebtn.png")
            self.aviso_error.img = self.aviso_error.img.resize((200, 60), Image.ANTIALIAS)
            self.aviso_error.img = ImageTk.PhotoImage(self.aviso_error.img)
            self.aviso_error.registro_btn = Button(
            self.aviso_error, width=200, height=60, image=self.aviso_error.img, command= lambda: self.aviso_error.destroy(), borderwidth=0)
            self.aviso_error.registro_btn.place(x=150, y=150)
            '''self.aviso = Toplevel(self)
            self.aviso.geometry("300x300+0+0")
            self.aviso.attributes("-topmost", True)
            self.aviso.update()
            self.aviso.title("IMPORTANTE")
            self.aviso.label = Label( self.aviso, text="Ya se han tomado las imagenes suficientes", padx=100, pady=100)
            self.aviso.label.pack()
            self.aviso.avisobtn = Button(self.aviso, width=180, height=55, text="Aceptar", command=self.destroy, borderwidth=0)
            self.aviso.avisobtn.pack()
            self.aviso.grab_set()  # Prevents other Tkinter windows from being used'''

        def crear_controles(self):
                self.frame = Frame(self)
                self.frame.pack()
                self.canvas_principal = Canvas(
                    self.frame, bg="white", width=800, height=480)
                self.canvas_principal.pack()
                # SE crea el ffondo de la aplicacion
                portada = Image.open("imagenes/fondo_principal.png")
                portada2 = portada.resize((800, 480), Image.ANTIALIAS)
                self.photoimage = ImageTk.PhotoImage(portada2)
                self.canvas_principal.create_image(400, 240, image=self.photoimage)
                # Se crean los botones para el sistema
                # ENTRADA Y SALIDA
                self.img = Image.open("imagenes/entradabtn.png")
                self.img = self.img.resize((200, 60), Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(self.img)
                self.entrada_btn = Button(self.frame, width=200, height=60,
                                          image=self.img, command=lambda: self.ventana_checada("Entrada"), borderwidth=0)
                self.entrada_btn.place(x=150, y=50)
                #
                self.img2 = Image.open("imagenes/salidabtn.png")
                self.img2 = self.img2.resize((200, 60), Image.ANTIALIAS)
                self.img2 = ImageTk.PhotoImage(self.img2)
                self.entrada_btn = Button(
                    self.frame, width=200, height=60, image=self.img2, command=lambda:self.ventana_checada("Salida"), borderwidth=0)
                self.entrada_btn.place(x=450, y=50)
                # INICIO DESCANSO Y FIN DESCANSO
                self.img3 = Image.open("imagenes/iniciodescansobtn.png")
                self.img3 = self.img3.resize((200, 60), Image.ANTIALIAS)
                self.img3 = ImageTk.PhotoImage(self.img3)
                self.entrada_btn = Button(
                    self.frame, width=200, height=60, image=self.img3,command=lambda:self.ventana_checada("Salida a Descanso"), borderwidth=0)
                self.entrada_btn.place(x=150, y=150)
                #
                self.img4 = Image.open("imagenes/findescansobtn.png")
                self.img4 = self.img4.resize((200, 60), Image.ANTIALIAS)
                self.img4 = ImageTk.PhotoImage(self.img4)
                self.entrada_btn = Button(
                    self.frame, width=200, height=60, image=self.img4, command=lambda:self.ventana_checada("Entrada Descanso"), borderwidth=0)
                self.entrada_btn.place(x=450, y=150)
                # ENTRADA T.E. Y SALIDA T.E.
                self.img5 = Image.open("imagenes/entradatebtn.png")
                self.img5 = self.img5.resize((200, 60), Image.ANTIALIAS)
                self.img5 = ImageTk.PhotoImage(self.img5)
                self.entrada_btn = Button(
                    self.frame, width=200, height=60, image=self.img5, command=lambda:self.ventana_checada("Entrada T.E."), borderwidth=0)
                self.entrada_btn.place(x=150, y=250)
                #
                self.img6 = Image.open("imagenes/salidatebtn.png")
                self.img6 = self.img6.resize((200, 60), Image.ANTIALIAS)
                self.img6 = ImageTk.PhotoImage(self.img6)
                self.entrada_btn = Button(
                    self.frame, width=200, height=60, image=self.img6, command=lambda:self.ventana_checada("Salida T.E."), borderwidth=0)
                self.entrada_btn.place(x=450, y=250)
                # CONFIGURACION
                self.img7 = Image.open("imagenes/configuracionbtn.png")
                self.img7 = self.img7.resize((100, 100), Image.ANTIALIAS)
                self.img7 = ImageTk.PhotoImage(self.img7)
                self.entrada_btn = Button(
                    self.frame, width=100, height=100, image=self.img7, command=self.ventana_entrar)
                    #ventana_Configuracion
                self.entrada_btn.place(x=550, y=350)


root = Tk()
root.wm_title("Checador")

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
# print("Width",windowWidth,"Height",windowHeight)

# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+0+0")
#root.overrideredirect(True)
screen_width = root.winfo_screenwidth()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() 
print(screen_width)
print(screen_height)
app = ChecadorAPP(root)
app.mainloop()
