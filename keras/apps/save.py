import os
import prepared
import bentoml

model_name = os.environ['MODEL_NAME']
model = prepared.load_model()
saved_model = bentoml.keras.save_model(model_name, model)
