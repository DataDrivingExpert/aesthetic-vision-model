"""
Convierte la salida cruda del modelo (ej. logits, bounding boxes) en 
algo visualizable o entendible por la UI.
"""
import pandas as pd
import os

class OutputFormatter(object):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir,"..","..","outputs","predictions")
        self.filename = "analysis.xlsx"
        pass

    def write_output(self, output:dict):
        """
        Escribe la salida formateada en un archivo.
        """
        df = pd.DataFrame(output)
        df.to_excel(os.path.join(self.output_dir, self.filename), index=False)
