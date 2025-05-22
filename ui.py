import customtkinter as ctk
from src.connector.controller import Controller
from tkinter import filedialog
from PIL import Image
from typing import Literal
import pandas as pd
import threading
import os

class AestheticApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables de configuración de la aplicación
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.statics_path = os.path.join(self.base_dir, 'static')

        # Variables de la aplicación
        self.controller = Controller()  # Instancia del controlador
        self.loaded_data:list[str] = [] # Lista de imágenes cargadas
        self.deployed_data:list[str] = [] # Lista de imágenes desplegadas
        self.deployed_index = 0         # Índice de la imagen actual en pantalla
        self.d_local_symm = None   # CTkLabel para mostrar el resultado de la simetría local
        self.d_global_symm = None    # CTkLabel para mostrar el resultado de la simetría global
        self.d_continuity = None   # CTkLabel para mostrar el resultado de la continuidad
        self.img_canvas = None      # Label para mostrar la imagen
        self.mode_btn_icons = (
            ctk.CTkImage(Image.open(os.path.join(self.statics_path, 'Inbox.png')), size=(30, 30)),
            ctk.CTkImage(Image.open(os.path.join(self.statics_path, 'Chip.png')), size=(30, 30))
        )
        self.mode_btn = None        # Botón para cambiar entre modo de entrada y predicción
        self.canvas_mode:Literal['input','pred'] = 'input'
        self.model_thread = None    # Hilo para la predicción
        self.has_predicted = False  # Bandera para verificar si se ha hecho una predicción

        self.prediction_results = [] # Resultados de la predicción

        # Variable para el loader
        self.loader_frames = self.__load_gif(os.path.join(self.statics_path, 'loader.gif'))
        self.loader_index = 0

        # Configuración de la ventana principal
        self.title("Degree Project")
        self.geometry("1138x640+0+0")
        # self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_layout()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_layout(self):
        # Main Layout Frame
        layout_frame = ctk.CTkFrame(master=self)
        layout_frame.grid(row=0, column=0, sticky='nsew')
        layout_frame.grid_columnconfigure(0, weight=1)
        layout_frame.grid_rowconfigure(1, weight=1)

        self.create_header(layout_frame)
        self.create_two_columns(layout_frame)
        self.create_button_row(layout_frame)

    def create_header(self, parent):
        header_frame = ctk.CTkFrame(master=parent)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        folder_icon = Image.open(os.path.join(self.statics_path, 'folder.png'))
        _folder = ctk.CTkImage(folder_icon, size=(30, 30))

        photo_icon = Image.open(os.path.join(self.statics_path, 'photograph.png'))
        _photo = ctk.CTkImage(photo_icon, size=(30, 30))

        ctk.CTkLabel(master=header_frame, text="Aesthetic Recognition System", font=("", 30)).grid(
            row=0, column=0, padx=5, pady=15, sticky='w')
        
        _inbox, _ = self.mode_btn_icons

        self.mode_btn = ctk.CTkButton(master=header_frame, image=_inbox, text="Mode: input images", command=self.__update_mode, fg_color="#2B2B2B", hover_color="#2F2F2F")
        self.mode_btn.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        ctk.CTkButton(master=header_frame, image=_photo,text="Upload single image", command=self.upload_single,fg_color="#2B2B2B", hover_color="#2F2F2F").grid(
            row=0, column=2, padx=5, pady=5, sticky='e')

        ctk.CTkButton(master=header_frame, image=_folder, text='Select image folder', command=self.upload_directory,fg_color="#2B2B2B", hover_color="#2F2F2F").grid(
            row=0, column=3, padx=5, pady=5, sticky='e')

    def create_two_columns(self, parent):
        two_cols_frame = ctk.CTkFrame(master=parent)
        two_cols_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        two_cols_frame.grid_columnconfigure(0, weight=3)
        two_cols_frame.grid_columnconfigure(1, weight=1)
        two_cols_frame.grid_rowconfigure(0, weight=1)

        self.create_left_column(two_cols_frame)
        self.create_right_column(two_cols_frame)

    def create_left_column(self, parent):
        left_col_frame = ctk.CTkFrame(master=parent)
        left_col_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        left_col_frame.grid_rowconfigure(0, weight=1)
        left_col_frame.grid_columnconfigure(1, weight=1)

        nav_frame = ctk.CTkFrame(master=left_col_frame)
        nav_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        nav_frame.grid_rowconfigure((0, 1), weight=1)

        left_png = Image.open(os.path.join(self.statics_path, 'left-arrow.png'))
        right_png = Image.open(os.path.join(self.statics_path, 'right-arrow.png'))

        icon_size = (50, 50)

        left_arrow = ctk.CTkImage(left_png, size=icon_size)
        right_arrow = ctk.CTkImage(right_png, size=icon_size)

        ctk.CTkButton(master=nav_frame, image=left_arrow, command=self.__previous_img, text="",fg_color="#2B2B2B", hover_color="#2B2B2B")\
            .grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        ctk.CTkButton(master=nav_frame, image=right_arrow, command=self.__next_img, text="",fg_color="#2B2B2B", hover_color="#2B2B2B")\
            .grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        

        self.img_canvas = ctk.CTkLabel(master=left_col_frame, text="IMAGES WILL SHOW HERE", font=("", 25))
        self.img_canvas.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
    def update_image_canvas(self, image_path=None):
        
        exist_img = False
        if image_path:
            pil_image = Image.open(image_path)
            exist_img = True
        elif self.deployed_data != []:
            pil_image = Image.open(self.deployed_data[self.deployed_index])
            exist_img = True
        else:
            pass

        if exist_img:
            pil_image.thumbnail((640,640), Image.LANCZOS)
            ctkImage = ctk.CTkImage(pil_image, size=pil_image.size)
            self.img_canvas.configure(image=ctkImage, text="")
            self.img_canvas.image = ctkImage
        else:
            self.img_canvas.configure(image="", text="No image loaded")
            self.img_canvas.image = None
            
    def create_right_column(self, parent):
        right_col_frame = ctk.CTkFrame(master=parent)
        right_col_frame.grid(row=0, column=1, pady=5, sticky='nsew')
        right_col_frame.grid_columnconfigure(0, weight=1)
        right_col_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.d_local_symm = self.create_score_frame(right_col_frame, 0,"Local Symmetry Score")
        self.d_global_symm = self.create_score_frame(right_col_frame, 1,"Global Symmetry Score")
        self.d_continuity = self.create_score_frame(right_col_frame, 2,"Continuity Score")

    def create_score_frame(self, parent, row, label_text):
        score_frame = ctk.CTkFrame(master=parent)
        score_frame.grid(row=row, column=0, padx=5, pady=5, sticky='nsew')
        score_frame.grid_columnconfigure(0, weight=1)
        score_frame.grid_rowconfigure((0, 1, 2), weight=1)

        score = ctk.CTkLabel(master=score_frame, text='0', font=("", 40))
        score.grid(row=0, column=0, sticky='nsew')

        ctk.CTkLabel(master=score_frame, text="Points", font=("", 15)).grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        ctk.CTkLabel(master=score_frame, text=label_text, font=("", 20)).grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        return score

    def create_button_row(self, parent):
        btn_row = ctk.CTkFrame(master=parent)
        btn_row.grid(row=2, column=0, padx=5, pady=5, sticky='we')
        btn_row.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(master=btn_row, text="evaluate", command=self.evaluate).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(master=btn_row, text="clear all", command=self.clear_all).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(master=btn_row, text="save results", command=self.save_results).grid(row=0, column=2, padx=5, pady=15)

    # --- Lógica de botones ---
    def upload_single(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.loaded_data.append(file_path)
            self.deployed_data.extend(self.loaded_data)
            self.update_image_canvas()
            

    def upload_directory(self):
        directory_path = filedialog.askdirectory(
            title="Selecciona una carpeta con imágenes"
        )
        if directory_path:
            pass

    
    def __load_gif(self, path):
        gif = Image.open(path)
        frames = []
        try:
            while True:
                frame = ctk.CTkImage(gif.copy().convert("RGBA").resize((100, 100)))
                frames.append(frame)
                gif.seek(len(frames))  # Siguiente frame
        except EOFError:
            pass
        return frames
    
    def __play_loader(self):
        if self.model_thread.is_alive():
            frame = self.loader_frames[self.loader_index]
            self.img_canvas.configure(image=frame)
            self.loader_index = (self.loader_index + 1) % len(self.loader_frames)
            self.after(100, self.__play_loader)

    def __update_predictions(self):
        # Ubicar la salida de la predicción
        prediction_path = os.path.join(self.base_dir, 'outputs', 'predictions','images')
        prediction_filenames = os.listdir(prediction_path)
        prediction_data = [os.path.join(prediction_path, filename) for filename in prediction_filenames]

        self.prediction_results = prediction_data

    def __previous_img(self):
        if self.deployed_index > 0:
            self.deployed_index -= 1
            self.update_image_canvas(self.deployed_data[self.deployed_index])
            self.__update_metrics()
        else:
            pass

    def __next_img(self):
        if self.deployed_index < len(self.deployed_data) - 1:
            self.deployed_index += 1
            self.update_image_canvas(self.deployed_data[self.deployed_index])
            self.__update_metrics()
        else:
            pass

    def __update_mode(self):
        inbox, chip = self.mode_btn_icons
        if self.canvas_mode == 'input':
            self.canvas_mode = 'pred'
            self.mode_btn.configure(text="Mode: prediction images", image=chip)
            self.deployed_data = self.prediction_results
        else:
            self.canvas_mode = 'input'
            self.mode_btn.configure(text="Mode: input images", image=inbox)
            self.deployed_data = self.loaded_data

        self.deployed_index = 0
        self.update_image_canvas()

    def __update_metrics(self):
        # Ubicar la salida de la predicción
        prediction_path = os.path.join(self.base_dir, 'outputs', 'predictions')
        df = pd.read_excel(os.path.join(prediction_path, 'analysis.xlsx'))
        img_name = self.deployed_data[self.deployed_index]
        img_name = os.path.basename(img_name)

        data = df[df['image_name'] == img_name]

        if not data.empty:
            local_symm = data['local_symmetry'].values[0]
            global_symm = data['global_symmetry'].values[0]
            continuity = data['continuity'].values[0]

            self.d_local_symm.configure(text=local_symm)
            self.d_global_symm.configure(text=global_symm)
            self.d_continuity.configure(text=continuity)
        else:
            self.d_local_symm.configure(text="0")
            self.d_global_symm.configure(text="0")
            self.d_continuity.configure(text="0")
        pass

    def evaluate(self):
        if self.loaded_data:
            self.model_thread = threading.Thread(target=self.controller.run_inference, args=(self.loaded_data,))
            self.model_thread.start()
            self.__play_loader()
            self.watch_thread()
        pass

    def clear_all(self):
        pass

    def save_results(self):
        pass

    def on_close(self):
        self.controller.close()
        self.destroy()

    def watch_thread(self):
        if self.model_thread.is_alive():
            self.after(100, self.watch_thread)
        else:
            # Ubicar la salida de la predicción
            self.__update_predictions()
            self.__update_mode()
            self.__update_metrics()
            pass
            


if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = AestheticApp()
    app.mainloop()
