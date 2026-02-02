FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    gcc libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libstdc++6 \
    fontconfig \
    # poppler-utils \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install paddlepaddle -f https://www.paddlepaddle.org.cn/whl/linux/cpu/noavx/stable.html
# RUN pip install 'paddlex[ocr]'

# to limit paddle ocr threads 
# ENV OMP_NUM_THREADS=1
# ENV MKL_NUM_THREADS=1
# ENV OPENBLAS_NUM_THREADS=1
# ENV NUMEXPR_NUM_THREADS=1
# ENV PADDLE_NUM_THREADS=1

EXPOSE 8000

COPY app app
