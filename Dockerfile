FROM codait/max-base:v1.1.1

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=https://max-assets-dev.s3.us-south.cloud-object-storage.appdomain.cloud/max-human-pose-estimator/1.0
ARG model_file=assets.tar.gz

RUN apt-get update && apt-get install -y gcc swig libgtk2.0 \
                   && apt-get install --reinstall -y build-essential && rm -rf /var/lib/apt/lists/*

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

# check file integrity
RUN md5sum -c md5sums.txt

RUN cd core/tf_pose/pafprocess/ && swig -python -c++ pafprocess.i && python setup.py build_ext --inplace

EXPOSE 5000

CMD python app.py
