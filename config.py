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

# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'MAX Human Pose Estimator'
API_DESC = 'Detect humans in an image and estimate the pose for each person.'
API_VERSION = '1.1.0'

# default model
MODEL_NAME = 'MAX Human Pose Estimator'
DEFAULT_MODEL_PATH = 'assets/human-pose-estimator-tensorflow.pb'
MODEL_LICENSE = 'Apache License 2.0'

DEFAULT_IMAGE_SIZE_STR = '432x368'
DEFAULT_IMAGE_SIZE = (432, 368)  # Recommends: 432x368 or 656x368 or 1312x736
DEFAULT_BATCH_SIZE = 2
DEFAULT_PREPROCESS_THREADS = 2
