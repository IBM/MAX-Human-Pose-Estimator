from core.model import ModelWrapper
from flask_restplus import fields, abort
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

input_parser = MAX_API.parser()
input_parser.add_argument('file', type=FileStorage, location='files',
                          required=True,
                          help='An image encoded as JPEG, PNG, or TIFF')

body_parts_prediction = MAX_API.model('body_parts_prediction', {
    'part_id': fields.Integer(required=True,
                              description='ID for the body part'),
    'part_name': fields.String(required=True,
                               description='Name of the body part'),
    'score': fields.Fixed(required=True,
                          description='The prediction score for the body part'),
    'x': fields.Integer(required=True,
                        description='X coordinate of the center point of the '
                                    'body part'),
    'y': fields.Integer(required=True,
                        description='Y coordinate of the center point of the '
                                    'body part')
})

line_prediction = MAX_API.model('LinePrediction', {
    'line': fields.List(fields.Integer(required=True,
                                       description='Coordinates for line '
                                                   'connecting two body parts, '
                                                   'in the format [x1, y1, x2, '
                                                   'y2]; (x1, y1) represents '
                                                   'the starting point of the '
                                                   'line, while (x2, y2) '
                                                   'represents the ending point'))})

label_prediction = MAX_API.model('LabelPrediction', {
    'human_id': fields.Integer(required=True,
                               description='ID for the detected person'),
    'pose_lines': fields.List(fields.Nested(line_prediction),
                              description='Detected pose lines for a person'),
    'body_parts': fields.List(fields.Nested(body_parts_prediction),
                              description='Detected body parts for a person')})

predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True,
                            description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction),
                               description='Predicted labels and probabilities')})

class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}
        args = input_parser.parse_args()
        try:
            input_data = args['file'].read()
            image = self.model_wrapper._read_image(input_data)
        except OSError as e:
            abort(400, "Please submit a valid image in PNG, Tiff or JPEG format")

        label_preds = self.model_wrapper.predict(image)
        result['predictions'] = label_preds
        result['status'] = 'ok'

        return result