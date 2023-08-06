import contextlib
import io
import os
import pickle
import sys
from collections import OrderedDict

import torch

from .extractor import Extractor
from .picture import Picture
from .yolo.yolov7 import Model

path_dir = os.path.dirname(os.path.abspath(__file__))


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout


def load_torch(weight: str, classes: list, image_size: int) -> Extractor:
    """load_torch. load pytorch model

    :param weight:
    :type weight: str
    :param classes:
    :type classes: list
    :param image_size:
    :type image_size: int
    :rtype: Extractor
    """
    model = Model(classes=classes)
    model.load_state_dict(torch.load(weight))
    model.eval()
    return Extractor(image_size=image_size, model=model, classes=classes)


def load(model: str = "yoloV7_coco.extractor") -> Extractor:
    """load. Load model

    :param model:
    :type model: str
    :rtype: Extractor
    """
    with open(model, "rb") as f:
        with nostdout():
            model = pickle.load(f)

    return model


def detect(
    image: object, model: Extractor, show: bool = False, save: str = "", score: int = 2
) -> [((int, int, int, int), str)]:
    """detect. detect entities from image

    :param image: image to detect
    :type image: object
    :param model: model to be used
    :type model: Extractor
    :param show: show the picture with bunding box
    :type show: bool
    :param save: save the picture
    :type save: str
    :param score: show the score on picture
    :type score: int
    :rtype: [((int, int, int, int), str)]
    """
    box_cla = model.predict(image)
    if show is True or save != "":
        picture = Picture(image, box_cla)
        picture.draw(conf_prec=score)
        if show is True:
            picture.image.show()
        if save != "":
            picture.image.save(save)
    return box_cla


def iml(image: object, model: str = "yoloV7_coco.extractor", **kwargs):
    """iml. detect entities from image

    :param image: image to be detected
    :type image: object
    :param model: model to use
    :type model: str
    :param kwargs:
    """
    model = load(os.path.join(path_dir, "model", model))
    return detect(image, model, **kwargs)
