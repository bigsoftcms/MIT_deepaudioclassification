FROM tensorflow/tensorflow:1.6.0

RUN apt-get update -y && apt-get install -y \
    libmagic-dev \
    sox \
    libsox-fmt-mp3 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


ADD pip-requirements.txt /pip-requirements.txt
RUN pip install -r /pip-requirements.txt
