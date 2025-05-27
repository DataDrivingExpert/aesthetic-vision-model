"""
Orquesta todo el flujo: recibe inputs, llama a inference_runner, procesa outputs. 
Idealmente debe contener lógica mínima.
"""

from .gen_graphs import AestheticGraph
from .input_handler import Preprocessor
from .inference_runner import InferenceRunner
from .output_formatter import OutputFormatter as OF
import os
from pathlib import Path
import shutil
from ultralytics.engine.results import Results
import numpy as np


class Controller(object):
    def __init__(self):
        # Grafos de simetría y continuidad generados
        aesthetic_graph = AestheticGraph()
        symmetry_graph, continuity_graph = aesthetic_graph.graphs

        # Cargar el modelo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # model_path = os.path.join(base_dir, '..', 'models', 'best.pt')
        # model_path = os.path.normpath(model_path)
        model_path = 'C:/Users/herre/Documents/uautonoma/trabajo-de-titulo/project/outputs/model_train/150_epochs_adamw/weights/best.pt'
        model = InferenceRunner(model_path)


        self.model = model
        self.outFormatter = OF()
        self.symmetry_graph = symmetry_graph
        self.continuity_graph = continuity_graph

    def __preprocess_input(self, input_data:tuple[str]):
        """
        Preprocesa los datos de entrada antes de pasarlos al modelo.
        """
        preprocessor = Preprocessor(input_data)
        preprocessed_data = preprocessor.perform(input_data)
        
        return preprocessed_data
    
    def __eval_global_symmetry(self,cls_ids:list[int]):
        """
        Evalúa la simetría global de los objetos detectados.
        """
        # cor: elementos correspondientes de la secuencia (e.g. 1-7,2-6,3-5) 
        score = 0
        g = self.symmetry_graph
        
        len_cls = len(cls_ids)
        for i in range(len_cls):
            if i != 3 and g.is_connected(g.get_v_by_id(cls_ids[i]), g.get_v_by_id(cls_ids[-(i+1)])):
                score += 1

        return score
    
    def __eval_local_symmetry(self,cls_ids:list[int]):
        """
        Evalúa la simetría local de los objetos detectados.
        """
        # cor: elementos correspondientes de la secuencia (e.g. 1-7,2-6,3-5) 
        score = 0
        g = self.symmetry_graph
        
        nth = len(cls_ids)
        for i in range(nth):
            if i != (nth - 1) and g.is_connected(g.get_v_by_id(cls_ids[i]), g.get_v_by_id(cls_ids[i+1])):
                score += 1

        return score
    
    def __eval_continuity(self,cls_ids:list[int]):
        """
        Evalúa la continuidad de los objetos detectados.
        """
        # cor: elementos correspondientes de la secuencia (e.g. 1-7,2-6,3-5) 
        score = 0
        g = self.continuity_graph
        
        nth = len(cls_ids)
        for i in range(nth):
            if i != (nth - 1) and g.is_connected(g.get_v_by_id(cls_ids[i]), g.get_v_by_id(cls_ids[i+1])):
                score += 1

        return score

    def __translate(self, results:Results):
        """
        Traduce los resultados del modelo a una evaluación del estímulo estético, en términos 
        de la simetría y continuidad de los objetos detectados.
        """
        evaluation = {
            'image_name': [],
            'global_symmetry': [],
            'local_symmetry': [],
            'continuity': [],
            'rejected': []
        }

        def register_eval(image_name, global_symmetry, local_symmetry, continuity, rejected):
            evaluation["image_name"].append(image_name)
            evaluation["global_symmetry"].append(global_symmetry)
            evaluation["local_symmetry"].append(local_symmetry)
            evaluation["continuity"].append(continuity)
            evaluation["rejected"].append(rejected)

        for r in results:
            boxes = r.boxes
            bb = boxes.xywh.cpu().numpy() # Bounding box en formato x_center y_center width height
            cls = boxes.cls.cpu().numpy() # ID de las clases detectadas
            img_name = Path(r.path).stem # Nombre de la imagen
            print(f'image_name from __translate = {img_name}')

            _sorted = [] # Lista de clases por cada objeto detectado en la imagen.
                         # Ordenadas de izquierda a derecha.
            for j in np.argsort(bb[:,0]):
                _sorted.append(int(cls[j]))
            
            print(f'{len(_sorted)=}')
            if len(_sorted) != 7:
                # Si no hay 7 objetos detectados, no se puede evaluar la imagen.
                register_eval(img_name,0,0,0,True)
                print('Image rejected')
                continue
            else:
                print('Image accepted')
                global_symm = self.__eval_global_symmetry(_sorted)
                local_symm = self.__eval_local_symmetry(_sorted)
                continuity = self.__eval_continuity(_sorted)
                register_eval(img_name, global_symm, local_symm, continuity, False)

        return evaluation

    def perform_eval(self, results:Results):
        """
        Realiza la evaluación de los resultados del modelo.
        """
        # Evaluar los resultados
        evaluation = self.__translate(results)
        self.outFormatter.write_output(evaluation)

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
        
        self.perform_eval(results)

    def retrieve_valid_files(self, dir_path:str):
        return Preprocessor.retrieve_valid_files(dir_path)

    def __clean_outputs(self):
        """
        Limpia los outputs generados por el preprocesador y las predicciones generadas por
        el programa.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, '..','..','outputs')

        pp_data_path = os.path.join(output_path, 'preprocessed_img')
        pred_data_path = os.path.join(output_path, 'predictions')

        for filename in os.listdir(pp_data_path):
            os.remove(os.path.join(pp_data_path, filename))

        shutil.rmtree(pred_data_path)
        os.mkdir(pred_data_path)
        os.mkdir(os.path.join(pred_data_path, 'images'))
        
    def save_results(self, dir):
        """
        Guarda los resultados de la evaluación en un directorio especificado.
        """
        self.outFormatter.save_output(dir)

    def clean_all(self):
        """
        Elimina los outputs generados por el preprocesador y las predicciones generadas por
        el programa.
        """
        self.__clean_outputs()

    