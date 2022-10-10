import torch, bentoml

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.data import MetadataCatalog
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2, os

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer

def load_model():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cpu"

    return cfg


def pre_processing(data):
    global base_img

    numpy_img = np.array(data)
    cv2_img = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)
    cv2_img = cv2_img[:, :, ::-1]
    base_img = cv2_img

    return cv2_img


def predict(runner, data):
    if os.environ['LIBRARY'] == 'detectron2':
        return runner.run.run(data)
    else:
        return runner.run(data)


def post_processing(data):
    cfg = load_model()
    v = Visualizer(base_img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(data["instances"].to("cpu"))
    im = out.get_image()[:, :, ::-1]

    return im
