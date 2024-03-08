import speedtest
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import threading
import time
import imageio
from tkinter import Tk, Label, Text, Button, filedialog, Frame, ttk, Scale, Canvas

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
        self.logof.grid(row=2, column=2, sticky='ew', padx=100, pady=3)

        self.msj = ttk.Frame(self.root, style='barratop.TFrame')
        self.msj = ttk.LabelFrame(self.root, text='Mensajes:', padding=(10, 10))
        self.msj.grid(row=3, column=1, sticky='ew', padx=0, pady=3, columnspan=2)       

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
        #dibujo
        self.gif_canvas = Canvas(self.msj, bg='#414141', width=250, height=250)
        self.gif_canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    def create_buttons(self):
        # Cargar y redimensionar la imagen del botón
        start_image_path = 'inicio.png'
        self.tk_start_image = self.resize_image(start_image_path, 150, 150)
        # Crear un botón con la imagen
        self.btn = ttk.Button(self.control, image=self.tk_start_image, command=self.iniciar_tarea)
        self.btn.grid(row=1, column=0, sticky='ew')
        # Botón de salir
        self.exit_b = ttk.Button(self.lat2, text='Salir', command=self.salir)
        self.exit_b.grid(row=0, column=0, sticky='we')
    
   
    def iniciar_tarea(self):
        # Desactivar el botón durante la tarea
        self.btn['state'] = 'disabled'
        # Crear y mostrar la barra de progreso
        self.progreso = ttk.Progressbar(self.control, mode='indeterminate')
        self.progreso.grid(row=2, column=0, sticky='ew')
        # Iniciar la tarea en un hilo separado
        hilo = threading.Thread(target=self.test)
        hilo.start()

    def actualizar_barra_progreso(self, valor):
        self.progreso['value'] = valor
        self.progreso.update_idletasks()

    def test(self):
        st = speedtest.Speedtest()
        st.get_best_server()       

        # Operaciones de prueba de velocidad
        d_st = st.download() / 1000000
        dwnT = round(d_st, 2)
        u_st = st.upload() / 1000000
        upldT = round(u_st, 2)
        st.get_servers([])
        ping = st.results.ping

        # Actualizar la barra de progreso desde el hilo principal
       

        # Configurar el mensaje con los resultados de la prueba
        compDwn = f'descarga: {dwnT} mbs \n subida: {upldT} mbs \n ping: {ping}'
        self.resultmsj.config(text=f'Resultado de la prueba = {compDwn}')

    def load_and_display_gif(self):
        # Ruta al archivo GIF
        gif_path = "load.gif"

        # Carga el GIF como una secuencia de imágenes
        gif_frames = imageio.get_reader(gif_path)

        # Obtiene el tamaño del Canvas
        canvas_width = self.gif_canvas.winfo_reqwidth()
        canvas_height = self.gif_canvas.winfo_reqheight()

        # Recorre todas las imágenes y las muestra en el Canvas
        for i, frame in enumerate(gif_frames):
            # Convierte el array de píxeles a una imagen de PIL
            image = Image.fromarray(frame)
            image = image.resize((150, 150))  # Ajusta el tamaño según tus necesidades

            # Convierte la imagen a un formato compatible con Tkinter
            tk_image = ImageTk.PhotoImage(image)

            # Configura la imagen en el Canvas
            canvas_x = (canvas_width - tk_image.width()) // 2  # Centra horizontalmente
            canvas_y = (canvas_height - tk_image.height()) // 2  # Centra verticalmente
            self.gif_canvas.create_image(canvas_x, canvas_y, anchor=tk.NW, image=tk_image)
            self.gif_canvas.image = tk_image

            # Actualiza la interfaz gráfica para mostrar el siguiente frame
            self.root.update_idletasks()

            # Espera un breve periodo para lograr la animación
            self.root.after(100)  


    def create_widgets(self):
        self.create_labels_and_entries()
        self.create_buttons()

        
    

    def salir(self):
        self.root.destroy()


if __name__=="__main__":
    root=ThemedTk(theme='equilux')
    app= velociraptor(root)
    root.mainloop()