# -*- coding: utf-8 -*-
# Este generador de diplomas lee una lista con nombre, dni y calificación para
# rellenarlos en una plantilla LaTeX con un marcador para cada campo.
# Opcionalemente compila los ficheros LaTeX generados y los une en uno solo.
# Si la plantilla LaTeX da error de compilación, pulsar intro varias veces.

import os

def generate(filename,level):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	path = os.path.join(base_dir + "/app")
	os.chdir(path)
	salida = open("output.tex","w") # crea fichero LaTeX para cada persona
	person = [filename,level] # pasar la cadena en lista ["testing.sb2","21"]
	
	text = open("certi.tex") # abrir documento LaTeX
	text = text.read() # leer documento LaTeX
	text_list = list(text) # pasa a lista, lista de caraceres uno a uno

	y_cali = text.find("%pointcalification") # busca marcador de calificación, busca la posicion en la que está esa palabra
	z_cali = len("%pointcalification")+2
	text_list[y_cali+z_cali:y_cali+z_cali] = list(person[1]) # inserta calificación

	y_name = text.find("%pointname") # lo mismo para el nombre
	z_name = len("%pointname")+2
	text_list[y_name+z_name:y_name+z_name] = list(person[0])

	text_final = "".join(text_list) # de lista a cadena

	salida.write(text_final) # guarda los cambio en el fichero creado
	salida.close() # cierra el fichero creado
	os.system("pdflatex output.tex")
	os.chdir(base_dir)
