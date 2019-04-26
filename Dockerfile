FROM codait/max-base:v1.1.1

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/human-pose-estimator/1.0
ARG model_file=assets.tar.gz

# Add the missing packages for OpenCV
RUN apt-get update && apt-get install libgtk2.0 -y && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc && apt-get install -y swig \
                   && apt-get install --reinstall -y build-essential && rm -rf /var/lib/apt/lists/*

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

RUN md5sum -c md5sums.txt # check file integrity

RUN cd core/tf_pose/pafprocess/ && swig -python -c++ pafprocess.i && python setup.py build_ext --inplace

EXPOSE 5000

CMD python app.py
