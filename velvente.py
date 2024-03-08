import speedtest
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import imageio
from tkinter import Tk, Label, Text, Button, filedialog, Frame, ttk, Scale, Canvas
import threading

class velociraptor:
    def __init__(self, root):
        self.root = root
        self.root.title('Velociraptor')
        self.root.geometry("1100x800")
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
        self.logof.grid(row=2, column=2, sticky='ew', padx=100, pady=3)

        self.casilla = ttk.Frame(self.root, style='barratop.TFrame')
        self.casilla = ttk.LabelFrame(self.root, text='Mensajes:', padding=(10, 10))
        self.casilla.grid(row=3, column=1, sticky='ew', padx=0, pady=3, columnspan=2) 
        #Frames de resultado
        self.msj = ttk.Frame(self.casilla, style='barratop.TFrame')
        self.msj = ttk.LabelFrame(self.casilla, text='Mensajes:', padding=(10, 10))
        self.msj.grid(row=0, column=0, sticky='ew', padx=0, pady=3, columnspan=3) 

        self.bajada = ttk.Frame(self.casilla, style='barratop.TFrame')
        self.bajada = ttk.LabelFrame(self.casilla, text='Bajada:', padding=(10, 10))
        self.bajada.grid(row=1, column=0, sticky='ew', pady=3) 

        self.subida = ttk.Frame(self.casilla, style='modulo.TFrame')
        self.subida = ttk.LabelFrame(self.casilla, text='Subida:', padding=(10, 10))
        self.subida.grid(row=1, column=1, sticky='ew', padx=0, pady=3)

        self.ping = ttk.Frame(self.casilla, style='modulo.TFrame')
        self.ping = ttk.LabelFrame(self.casilla, text='Subida:', padding=(10, 10))
        self.ping.grid(row=1, column=2, sticky='ew', padx=0, pady=3)  

        self.tk_logo_image = None
        self.tk_start_image = None

        
        self.create_widgets()
   
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
        # subida
        self.sub = ttk.Label(self.subida, text='Nada aún por aquí', background='#414141', foreground='white')
        self.sub.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        #bajda
        self.baj = ttk.Label(self.bajada, text='Nada aún por aquí', background='#414141', foreground='white')
        self.baj.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        #ping
        self.pi = ttk.Label(self.ping, text='Nada aún por aquí', background='#414141', foreground='white')
        self.pi.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        
        

    def create_buttons(self):
        # Cargar y redimensionar la imagen del botón
        start_image_path = 'inicio.png'
        self.tk_start_image = self.resize_image(start_image_path, 150, 150)
        # Crear un botón con la imagen
        self.btn = ttk.Button(self.control, image=self.tk_start_image, command=self.starting)
        self.btn.grid(row=1, column=0, sticky='ew')
        # Botón de salir
        self.exit_b = ttk.Button(self.lat2, text='Salir', command=self.salir)
        self.exit_b.grid(row=0, column=0, sticky='we')
    
   
    

    def starting(self):
        self.resultmsj.config(text=f'Realizando prueba. Por favor Aguarde')
        self.btn['state'] = 'disable'
        print("lading...")
        # Iniciar hilo para la tarea
        self.loading_thread = threading.Thread(target=self.test)
        self.loading_thread.start()    

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
        self.compDwn= 'descarga: ' + str(dwnT) + ' mbs \n ' + 'subida: ' + str(upldT) + ' mbs \n ping: ' + str(ping)
        self.Donde()  

    
    def Donde(self):
        self.resultmsj.config(text=f'Resultado de la prueba = {self.compDwn}')
        self.btn['state'] = 'enable'
        print('listo!')

    def create_widgets(self):
        self.create_labels_and_entries()
        self.create_buttons()

        
    

    def salir(self):
        self.root.destroy()


if __name__=="__main__":
    root=ThemedTk(theme='equilux')
    app= velociraptor(root)
    root.mainloop()