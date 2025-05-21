"""
Orquesta todo el flujo: recibe inputs, llama a inference_runner, procesa outputs. 
Idealmente debe contener lógica mínima.
"""

from .gen_graphs import AestheticGraph
from .input_handler import Preprocessor
from .inference_runner import InferenceRunner
import os


class Controller(object):
    def __init__(self):
        # Grafos de simetría y continuidad generados
        aesthetic_graph = AestheticGraph()
        symmetry_graph, continuity_graph = aesthetic_graph.graphs

        # Cargar el modelo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, '..', 'models', 'best.pt')
        model_path = os.path.normpath(model_path)
        model = InferenceRunner(model_path)

        self.model = model
        self.symmetry_graph = symmetry_graph
        self.continuity_graph = continuity_graph

    def __preprocess_input(self, input_data:tuple[str]):
        """
        Preprocesa los datos de entrada antes de pasarlos al modelo.
        """
        preprocessor = Preprocessor(input_data)
        preprocessed_data = preprocessor.perform(input_data)
        
        return preprocessed_data

    def run_inference(self, input_data):
        """
        Ejecuta la inferencia en los datos de entrada y devuelve los resultados.
        """
        # Preprocesar los datos de entrada
        self.__preprocess_input(input_data)

        # Ubicar la salida del preprocesador
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # pp: preprocessed
        pp_data_path = os.path.join(base_dir, '..','..','outputs','preprocessed_img')
        pp_filenames = os.listdir(pp_data_path)
        pp_data = [os.path.join(pp_data_path, filename) for filename in pp_filenames]

        results = self.model.predict(tuple(pp_data))
        
        # Procesar los resultados según sea necesario
        print(results)
        return results

    