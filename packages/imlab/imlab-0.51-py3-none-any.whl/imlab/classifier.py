import contextlib
import io
import pickle
import sys

from PIL import Image

from .classifier_wrapper import Wrapper, decode, preprocess


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout


class Classifier(Wrapper):
    """Classifier."""

    def __init__(
        self,
        weight: str = None,
        model_type: str = "MobileNetV2",
        image_size: int = 300,
        model: object = None,
        preprocess: callable = preprocess,
        decode: callable = decode,
        num_class: int = 0,
    ):
        """__init__.

        :param weight:
        :type weight: str
        :param model_type:
        :type model_type: str
        :param image_size:
        :type image_size: int
        :param model:
        :type model: object
        :param preprocess:
        :type preprocess: callable
        :param decode:
        :type decode: callable
        :param num_class:
        :type num_class: int
        """
        Wrapper.__init__(
            self,
            weight=weight,
            model_type=model_type,
            image_size=image_size,
            preprocess=preprocess,
            model=model,
            decode=decode,
            model_mod="use",
        )
        self.num_class = num_class

    def infer(self, image: object):
        to_predict = self.norm_input(image)
        to_predict = self.preprocess(to_predict)
        res = self.model(to_predict)
        return res.numpy()

    def predict_iter(self, image: object):
        res = self.infer(image)
        res = self.decode(res, top=self.num_class)
        for name, desc, score in res[0]:
            yield name, score

    def predict(self, image: object, num: int = 1) -> (str, float):
        """predict. predict image classe

        :param image:
        :type image: object
        :param num: number of result, if num==0, return a generator
        :type num: int
        :rtype: (str, float)
        """

        res = self.infer(image)
        res = self.decode(res, top=num)
        if num == 1:
            return (res[0][0], res[0][1])
        else:
            return [(name, score) for name, score in res][:num]

    def dump(self, file_handler) -> None:
        """dump.

        :param file_handler:
        :rtype: None
        """
        self.score = self.model.get_metrics_result()
        with nostdout():
            pickle.dump(self, file_handler)
