import os
import bentoml
import prepared
import utils

input_type = utils.get_data_type(os.environ['INPUT_TYPE'])
output_type = utils.get_data_type(os.environ['OUTPUT_TYPE'])
model_name = os.environ['MODEL_NAME']
library = os.environ['LIBRARY']

artifacts = prepared.load_artifacts()
svc = bentoml.Service(model_name)

@svc.api(input=input_type, output=output_type)
def predict(input):
    return prepared.run(artifacts, input)
