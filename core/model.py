#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from maxfw.model import MAXModelWrapper

import io
import logging
import time
from PIL import Image
import numpy as np
from flask_restplus import abort

from core.tf_pose.estimator import TfPoseEstimator
from config import DEFAULT_MODEL_PATH, DEFAULT_IMAGE_SIZE, MODEL_NAME

logger = logging.getLogger('MAX-Human-Pose-Estimator')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': '{}'.format(MODEL_NAME.lower()),
        'name': '{} TensorFlow Model'.format(MODEL_NAME),
        'description': 'Openpose TensorFlow model trained on COCO data to detect human poses',
        'type': 'Human pose estimation',
        'license': 'Apache License 2.0',
        'source': 'https://developer.ibm.com/exchanges/models/all/max-human-pose-estimator/'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        self.model = TfPoseEstimator(path, target_size=DEFAULT_IMAGE_SIZE)
        logger.info('Loaded model')
        # Metadata
        self.w, self.h = DEFAULT_IMAGE_SIZE
        logger.info("W = {}, H = {} ".format(self.w, self.h))

    def _read_image(self, image_data):
        try:
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
               image = image.convert('RGB')
            # Convert RGB to BGR for OpenCV.
            image = np.array(image)[:, :, ::-1]
            return image
        except IOError as e:
            logger.error(str(e))
            abort(400, "Please submit a valid image in PNG, TIFF or JPEG format")

    def _predict(self, x):
        t = time.time()
        humans = self.model.inference(x, resize_to_default=True,
                                      upsample_size=4.0)
        results = TfPoseEstimator.draw_human_pose_connection(x, humans)
        logger.info('inference in %.4f seconds.' % (time.time() - t))
        return results
