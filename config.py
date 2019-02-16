# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'MAX Human Pose Estimator'
API_DESC = 'Detect humans and their poses'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'MAX Human Pose Estimator'
DEFAULT_MODEL_PATH = 'assets/human-pose-estimator-tensorflow.pb'
MODEL_LICENSE = 'Apache License 2.0'

DEFAULT_IMAGE_SIZE_STR = '432x368'
DEFAULT_IMAGE_SIZE = (432,368)  # Recommends: 432x368 or 656x368 or 1312x736
DEFAULT_BATCH_SIZE = 2
DEFAULT_PREPROCESS_THREADS = 2