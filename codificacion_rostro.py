# USAGE
# Cuando estes codificando en laptop, equipo de escritorio o GPU debes de usar la detección de cnn (codificación lenta, más preciso):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# Cuando estes trabajando en un equipos sencillo como una Raspberry o un dispositivo pobre usar hog (codificación rapida, más preciso):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# Importamos las librerias necesarias
from imutils import paths
from tkinter import *
# En windows hay que instalar visual studio (community o el de paga) con herramientas de C++ para poder ytr
import face_recognition
import argparse
import pickle
import cv2  # Para desarrollos rapidos usar la verión de OpenCV de PIP
import os

class CodificadorImagenes:

	def __init__(self):
		self.ruta = os.getcwd()
		self.rutaImagenes = self.ruta+"/dataset"
		# hog para raspberry cnn para laptop, escritorio o servidor (equipos mas potentes)
		self.modelo = "hog"
		self.codificacionesConocidas = []
		self.nombresConocidos = []
		print("[INFO] cuantificando rostros...")
		self.rutaImagenes = list(paths.list_images(self.rutaImagenes))

	def iniciar_codificación(self,texto,bar,btn):
		#iteramos todas las imagenes para obtener su nombre
		for (i, pathImagen) in enumerate(self.rutaImagenes):
			#Obtenemos los nombres de las personas por medio de las carpetas que se crean al registrarlas
			print("[INFO] procesando la imagen {}/{}".format(i + 1,	len(self.rutaImagenes)))
			texto.insert(END,str("[INFO] procesando la imagen {}/{}".format(str(i + 1),len(self.rutaImagenes))+'\n') )
			texto.update_idletasks()
			bar['value'] = (i + 1)*(100/len(self.rutaImagenes))
			bar.update_idletasks()
			nombre = pathImagen.split(os.path.sep)[-2]

			# Cargamos las imagenes por medio de OpenCV para convertirlas a color
			# usando el orden por dlib (RGB)
			imagen = cv2.imread(pathImagen)
			rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

			# detectamos X y Y para dibujar el rectangulo o cuadrado que encierre las caracteristicas de la persona
			# correpondientemente a cada rostro de la persona
			boxes = face_recognition.face_locations(rgb, model=self.modelo)

			# calculamos las caracteristicas del rostro de la persona
			codificaciones = face_recognition.face_encodings(rgb, boxes)

			# iteramos cada codificacion y la guaramos en arrays y los nombres tambien
			for cod in codificaciones:
				# a cada codificacion se le añade un nombre por cada set de codificaciones
				self.codificacionesConocidas.append(cod)
				self.nombresConocidos.append(nombre)

				# guardamos las codificaciones y los nombres en un archivo serializandolos como objetos con el uso de Pickle
				# hay que usar la extensión ".pickle" para poder trabajarlos
				print("[INFO] serializando codificaciones...")
				data = {"Codificaciones": self.codificacionesConocidas,
				    "Nombres": self.nombresConocidos}
				f = open("codificaciones.pickle", "wb")
				f.write(pickle.dumps(data))
				f.close()
		btn.config(state='normal')
		texto.insert(END,str("*** FIN DEL PROCESO *** \n") )
		texto.insert(END,str("Puede cerrar la ventana... \n") )
