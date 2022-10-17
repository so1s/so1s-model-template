from bentoml.io import NumpyNdarray, JSON, Text, File, Multipart, Image, PandasDataFrame, PandasSeries

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

def get_data_type(type):
    get_type = type_dict.get(type)
    if get_type is None:
        raise TypeError('No Match Type. Please Input in [numpy, json, text, file, multipart, image, dataframe, series]')
    else:
        return get_type
