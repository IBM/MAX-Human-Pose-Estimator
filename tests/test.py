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

import requests
import pytest


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Human Pose Estimator'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max human pose estimator'
    assert metadata['name'] == 'MAX Human Pose Estimator TensorFlow Model'
    assert metadata['description'] == 'TensorFlow model trained on COCO data to detect human poses'
    assert metadata['license'] == 'Apache License 2.0'


def _check_response(r):
    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert len(response['predictions']) == 3
    assert response['predictions'][0]['human_id'] == 0
    assert len(response['predictions'][0]['pose_lines']) > 0
    assert len(response['predictions'][0]['body_parts']) > 0


def test_predict():

    model_endpoint = 'http://localhost:5000/model/predict'
    formats = ['jpg', 'png', 'tiff']
    img_path = 'samples/Pilots.{}'

    for f in formats:
        p = img_path.format(f)
        with open(p, 'rb') as file:
            file_form = {'file': (p, file, 'image/{}'.format(f))}
            r = requests.post(url=model_endpoint, files=file_form)
        _check_response(r)

    # Test by the image without faces
    img2_path = 'samples/IBM.jpeg'

    with open(img2_path, 'rb') as file:
        file_form = {'file': (img2_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert len(response['predictions']) == 0

    # Test by the text data
    img3_path = 'README.md'

    with open(img3_path, 'rb') as file:
        file_form = {'file': (img3_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__])
