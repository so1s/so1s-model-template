import os
import bentoml
import prepared
from utils import getType

input_type = getType(os.environ['INPUT_TYPE'])
output_type = getType(os.environ['OUTPUT_TYPE'])
model_name = os.environ['MODEL_NAME']
runner = bentoml.keras.get(model_name).to_runner()
svc = bentoml.Service(model_name, runners=[runner])


@svc.api(input=input_type, output=output_type)
def predict(input):
    model_input = prepared.pre_processing(input)
    model_output = prepared.predict(runner, model_input)
    return prepared.post_processing(model_output)
