# Use TensorFlow GPU base image
FROM tensorflow/tensorflow:2.14.0-gpu

# Update package list and install necessary libraries
RUN apt-get update && apt-get install -y \
    x11-apps \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libfreetype6-dev libportmidi-dev libjpeg-dev \
    clang \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN pip install protobuf==3.20.3

WORKDIR /tf

COPY . .

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV DISPLAY=host.docker.internal:0.0

# run the training script
CMD ["python", "train.py"]

