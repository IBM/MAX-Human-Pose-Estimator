# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'human-pose-estimator-tensorflow'
DEFAULT_MODEL_PATH = 'assets/{}.pb'.format(MODEL_NAME)
MODEL_LICENSE = 'Apache License 2.0'

MODEL_META_DATA = {
    'id': '{}'.format(MODEL_NAME.lower()),
    'name': 'Openpose TensorFlow Model',
    'description': 'Openpose TensorFlow model trained on COCO data to detect human poses',
    'type': 'Human pose detection',
    'license': '{}'.format(MODEL_LICENSE)
}

DEFAULT_IMAGE_SIZE_STR = '432x368'
DEFAULT_IMAGE_SIZE = (432,368)  # Recommends: 432x368 or 656x368 or 1312x736
DEFAULT_BATCH_SIZE = 2
DEFAULT_PREPROCESS_THREADS = 2