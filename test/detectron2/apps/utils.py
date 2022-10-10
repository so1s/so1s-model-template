import bentoml, prepared
from bentoml.io import NumpyNdarray, JSON, Text, File, Multipart, Image, PandasDataFrame, PandasSeries
import os

from detectron2.engine import DefaultPredictor

type_dict = {
    "numpy": NumpyNdarray(),
    "json": JSON(),
    "text": Text(),
    "file": File(),
    "multipart": Multipart(),
    "image": Image(),
    "dataframe": PandasDataFrame(),
    "series": PandasSeries()
}


def save_runner():
    tag = os.environ['MODEL_NAME']
    library = os.environ['LIBRARY']

    if library == 'build_v2':
        model = prepared.load_model()
        bentoml.tensorflow.save(tag, model)
    elif library == 'keras':
        model = prepared.load_model()
        bentoml.keras.save(tag, model)
    elif library == 'pytorch':
        model = prepared.load_model()
        bentoml.pytorch.save(tag, model)
    elif library == 'pytorch_lightning':
        model = prepared.load_model()
        bentoml.pytorch_lightning.save(tag, model)
    elif library == 'sklearn':
        model = prepared.load_model()
        bentoml.sklearn.save(tag, model)
    elif library == 'xgboost':
        model = prepared.load_model()
        bentoml.xgboost.save(tag, model)
    elif library == 'transformers':
        model = prepared.load_model()
        bentoml.transformers.save(tag, model)
    elif library == 'detectron2':  # not supported yet at bentoml
        pass
    else:
        raise TypeError('No Match Framework. Please check Framework.')


def get_data_type(type):
    get_type = type_dict.get(type)
    if get_type is None:
        raise TypeError('No Match Type. Please Input in [numpy, json, text, file, multipart, image, dataframe, series]')
    else:
        return get_type


def get_runner(library, tag):
    if library == 'build_v2':
        return bentoml.tensorflow.load_runner(tag)
    elif library == 'keras':
        return bentoml.keras.load_runner(tag)
    elif library == 'pytorch':
        return bentoml.pytorch.load_runner(tag)
    elif library == 'pytorch_lightning':
        return bentoml.pytorch_lightning.load_runner(tag)
    elif library == 'sklearn':
        return bentoml.sklearn.load_runner(tag)
    elif library == 'xgboost':
        return bentoml.xgboost.load_runner(tag)
    elif library == 'transformers':
        return bentoml.transformers.load_runner(tag)
    elif library == 'detectron2':  # not supported yet at bentoml
        class Detectron2Runnable(bentoml.Runnable):
            SUPPORTED_RESOURCES = ("cpu",)
            SUPPORTS_CPU_MULTI_THREADING = False

            def __init__(self):
                self.cfg = prepared.load_model()
                self.predictor = DefaultPredictor(self.cfg)

            @bentoml.Runnable.method(batchable=False)
            def run(self, input_img):
                return self.predictor(input_img)

        return bentoml.Runner(Detectron2Runnable)
    else:
        raise TypeError('No Match Framework. Please check Framework.')
