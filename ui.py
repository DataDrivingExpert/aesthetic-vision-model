import customtkinter as ctk
from src.connector.controller import Controller
from tkinter import filedialog

class AestheticApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controller = Controller()

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
        header_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(master=header_frame, text="Aesthetic Recognition System", font=("", 30)).grid(
            row=0, column=0, padx=5, pady=15, sticky='w')

        ctk.CTkButton(master=header_frame, text="Upload single image", command=self.upload_single).grid(
            row=0, column=1, padx=5, pady=5, sticky='e')

        ctk.CTkButton(master=header_frame, text="Upload directory", command=self.upload_directory).grid(
            row=0, column=2, padx=5, pady=5, sticky='e')

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
        left_col_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(master=left_col_frame, text="CAMERA INPUT", font=("", 25)).grid(
            row=0, column=0, padx=5, pady=5, sticky='nsew')

    def create_right_column(self, parent):
        right_col_frame = ctk.CTkFrame(master=parent)
        right_col_frame.grid(row=0, column=1, pady=5, sticky='nsew')
        right_col_frame.grid_columnconfigure(0, weight=1)
        right_col_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_score_frame(right_col_frame, 0, "Local Symmetry Score")
        self.create_score_frame(right_col_frame, 1, "Global Symmetry Score")
        self.create_score_frame(right_col_frame, 2, "Continuity Score")

    def create_score_frame(self, parent, row, label_text):
        score_frame = ctk.CTkFrame(master=parent)
        score_frame.grid(row=row, column=0, padx=5, pady=5, sticky='nsew')
        score_frame.grid_columnconfigure(0, weight=1)
        score_frame.grid_rowconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(master=score_frame, text="3", font=("", 40)).grid(row=0, column=0, sticky='nsew')
        ctk.CTkLabel(master=score_frame, text="Points", font=("", 15)).grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        ctk.CTkLabel(master=score_frame, text=label_text, font=("", 20)).grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def create_button_row(self, parent):
        btn_row = ctk.CTkFrame(master=parent)
        btn_row.grid(row=2, column=0, padx=5, pady=5, sticky='we')
        btn_row.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(master=btn_row, text="evaluate", command=self.evaluate).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(master=btn_row, text="clear all", command=self.clear_all).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(master=btn_row, text="save results", command=self.save_results).grid(row=0, column=2, padx=5, pady=15)

    # --- Lógica de botones (por ahora placeholders) ---
    def upload_single(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.controller.run_inference((file_path,))
            

    def upload_directory(self):
        directory_path = filedialog.askdirectory(
            title="Selecciona una carpeta con imágenes"
        )
        if directory_path:
            print("Directorio seleccionado:", directory_path)

    def evaluate(self):
        print("Evaluando...")

    def clear_all(self):
        print("Limpiando interfaz...")

    def save_results(self):
        print("Guardando resultados...")

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = AestheticApp()
    app.mainloop()
