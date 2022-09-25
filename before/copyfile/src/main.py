import numpy as np
from bentoml.io import NumpyNdarray
import bentoml

from sklearn import svm
from sklearn import datasets

# Load training data set
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train the model
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

# Save model to the BentoML local model store
saved_model = bentoml.sklearn.save_model("iris_classifier", clf)
print(f"Model saved: {saved_model}")

iris_classifier_runner = bentoml.sklearn.get(
    "iris_classifier:latest").to_runner()

svc = bentoml.Service("iris_classifier", runners=[iris_classifier_runner])


@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    result = iris_classifier_runner.predict.run(input_series)
    return result
