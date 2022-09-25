import tensorflow as tf


def load_model():
    return tf.keras.models.load_model("model.h5")


def pre_processing(data):
    return data


def predict(runner, data):
    return runner.run(data)


def post_processing(data):
    return data
