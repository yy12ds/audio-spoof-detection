FROM python:3.10

RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /usr/src/

COPY ./apps /usr/src/apps
COPY ./local.sqlite /usr/src/local.sqlite
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./model.pt /usr/src/model.pt

RUN pip install --upgrade pip

# CPU版PyTorch（軽量）

RUN pip install torch torchvision torchaudio torchcodec --index-url https://download.pytorch.org/whl/cpu


RUN pip install -r requirements.txt

RUN echo "building..."

ENV FLASK_APP="apps.app:create_app('local')"
ENV IMAGE_URL="/storage/images"

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]
