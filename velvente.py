import speedtest
import math
import requests
import tkinter
from tkinter import*
from tkinter import ttk
from tkinter import Tk, Label, Text, Button, filedialog, Frame, ttk, Scale, Canvas
import tkinter as tk
from tkinter import ttk
import os
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


class velociraptor:
    def __init__(self, root):
        self.root = root
        self.root.title('Velociraptor')
        self.root.geometry("1100x400")
        self.root.configure(bg='#414141')

        style = ttk.Style()        
        self.root.set_theme('equilux')  
        style.configure('barratop.TFrame', background='#414141')
        style.configure('modulo.TFrame', background='white')

        self.nav_bar = ttk.Frame(self.root, height=50, style='barratop.TFrame')
        self.nav_bar.grid(row=0, column=0, sticky='ew', pady=0, padx=0, columnspan=4)

        self.lat1 = ttk.Frame(self.root, width=200, style='barratop.TFrame')
        self.lat1.grid(row=0, column=0, sticky='ns', pady=0, padx=0, rowspan=4)

        self.lat2 = ttk.Frame(self.root, width=200, style='barratop.TFrame')
        self.lat2.grid(row=0, column=3, sticky='ns', pady=0, padx=0, rowspan=4)

        self.control = ttk.Frame(self.root, width=400, height=200, style='barratop.TFrame')
        self.control = ttk.LabelFrame(self.root, text='Presione el botón y aguarde', padding=(10, 10))
        self.control.grid(row=2, column=1, sticky='ew', padx=20, pady=3)
        
        
        self.logof = ttk.Frame(self.root, width=400, height=200, style='barratop.TFrame')
        #self.logof = ttk.LabelFrame(self.root, text='Empresa', padding=(10, 10))
        self.logof.grid(row=2, column=2, sticky='ew', padx=100, pady=3)

        self.msj = ttk.Frame(self.root, style='barratop.TFrame')
        self.msj = ttk.LabelFrame(self.root, text='Mensajes:', padding=(10, 10))
        self.msj.grid(row=3, column=1, sticky='ew', padx=0, pady=3, columnspan=2)

        #barra de progreso
        self.barra_progreso = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.barra_progreso.grid(row=5, column=1, columnspan=2, pady=10)

        self.tk_logo_image = None
        self.tk_start_image = None
        self.create_widgets()

    def create_widgets(self):
        self.create_labels_and_entries()
        self.create_buttons()

    def resize_image(self, image_path, width, height):
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    def create_labels_and_entries(self):
        # Cargar y redimensionar la imagen
        logo_image_path = 'logo.png'
        self.tk_logo_image = self.resize_image(logo_image_path, 200, 200)
        # Mostrar la imagen en un Label
        self.logolabel = ttk.Label(self.logof, image=self.tk_logo_image, padding=0)
        self.logolabel.grid(row=0, column=0, padx=10, pady=10)
        # Configurar mensaje
        self.resultmsj = ttk.Label(self.msj, text='Nada aún por aquí', background='#414141', foreground='white')
        self.resultmsj.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    def create_buttons(self):
        # Cargar y redimensionar la imagen del botón
        start_image_path = 'inicio.png'
        self.tk_start_image = self.resize_image(start_image_path, 150, 150)
        # Crear un botón con la imagen
        self.btn = ttk.Button(self.control, image=self.tk_start_image, command=self.test)
        self.btn.grid(row=1, column=0, sticky='ew')
        # Botón de salir
        self.exit_b = ttk.Button(self.lat2, text='Salir', command=self.salir)
        self.exit_b.grid(row=0, column=0, sticky='we')
    

    def test(self):
        
    
        
        st = speedtest.Speedtest()
        st.get_best_server()
        d_st = st.download()/1000000
        dwnT = round(d_st,2)
        u_st = st.upload()/1000000
        upldT = round(u_st,2)
        print("tu velocidad es", dwnT, "Mbs")
        print("tu subida es", upldT, "Mbs")
        st.get_servers([])
        ping = st.results.ping
        print("tu ping es de", ping)
        compDwn= 'descarga: ' + str(dwnT) + ' mbs \n ' + 'subida: ' + str(upldT) + ' mbs \n ping: ' + str(ping)
        #telegram#
        self.resultmsj.config(text=f'Resultado de la prueba = {compDwn} h')
        
    

    def salir(self):
        self.root.destroy()












   





if __name__=="__main__":
    root=ThemedTk(theme='equilux')
    app= velociraptor(root)
    root.mainloop()