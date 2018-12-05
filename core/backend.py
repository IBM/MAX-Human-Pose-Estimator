import io
import logging
import time
from PIL import Image
import numpy as np
from core.tf_pose.estimator import TfPoseEstimator

from config import DEFAULT_MODEL_PATH, DEFAULT_IMAGE_SIZE

logger = logging.getLogger('MAX-Human-Pose-Estimator')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    # Convert RGB to BGR for OpenCV.
    image = np.array(image)[:,:,::-1]

    return image

class ModelWrapper(object):
    """Model wrapper for TensorFlow models in SavedModel format"""

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        self.model = TfPoseEstimator(path, target_size=DEFAULT_IMAGE_SIZE)
        logger.info('Loaded model')
        # Metadata
        self.w, self.h = DEFAULT_IMAGE_SIZE
        logger.info("W = {}, H = {} ".format(self.w, self.h))


    def predict(self, x):
        t = time.time()
        humans = self.model.inference(x, resize_to_default=True, upsample_size=4.0)
        results = TfPoseEstimator.draw_human_pose_connection(x, humans)
        logger.info('inference in %.4f seconds.' % (time.time() - t))
        return results