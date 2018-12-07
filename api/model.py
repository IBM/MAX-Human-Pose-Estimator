from flask_restplus import Namespace, Resource, fields, abort
from werkzeug.datastructures import FileStorage

from config import MODEL_META_DATA
from core.backend import ModelWrapper, read_image

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


# Creating a JSON response model: https://flask-restplus.readthedocs.io/en/stable/marshalling.html#the-api-model-factory
body_parts_prediction = api.model('body_parts_prediction', {
    "part_id": fields.Integer(required=True),
    "part_name": fields.String(required=True),
    "score": fields.Fixed(required=True),
    "x": fields.Integer(required=True),
    "y": fields.Integer(required=True)
})
line_prediction = api.model('LinePrediction', {
    'line': fields.List(fields.Integer(required=True, description='Connection line for the detected joins in the format '
                                                                '[x1, y1, x2, y2]'))
})
label_prediction = api.model('LabelPrediction', {
    'human_id': fields.Integer(required=True),
    'pose_lines': fields.List(fields.Nested(line_prediction), description='Detected pose lines for a person'),
    "body_parts": fields.List(fields.Nested(body_parts_prediction), description='Detected body parts for a person')
})
predict_response = api.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction), description='Predicted labels and probabilities')
})

# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = api.parser()
# Example parser for file input
input_parser.add_argument('file', type=FileStorage, location='files', required=True)


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(input_parser)
    @api.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        try:
            input_data = args['file'].read()
            image = read_image(input_data)
        except OSError as e:
            abort(400, "Please submit a valid image in PNG, Tiff or JPEG format")

        label_preds = self.model_wrapper.predict(image)

        result['predictions'] = label_preds
        result['status'] = 'ok'

        return result
