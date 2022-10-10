import os
import bentoml
import prepared
import utils

input_type = utils.get_data_type(os.environ['INPUT_TYPE'])
output_type = utils.get_data_type(os.environ['OUTPUT_TYPE'])
model_name = os.environ['MODEL_NAME']
library = os.environ['LIBRARY']

<<<<<<< HEAD
model = prepared.load_model()
svc = bentoml.Service(model_name)
=======
runner = utils.get_runner(library, model_name)
svc = bentoml.Service(model_name, runners=[runner])

>>>>>>> b48f64a (feat: add support multiple framework (include detectron2))

@svc.api(input=input_type, output=output_type)
def predict(input):
    model_input = prepared.pre_processing(input)
<<<<<<< HEAD
    model_output = prepared.predict(model, model_input)
=======
    model_output = prepared.predict(runner, model_input)
>>>>>>> b48f64a (feat: add support multiple framework (include detectron2))
    return prepared.post_processing(model_output)
