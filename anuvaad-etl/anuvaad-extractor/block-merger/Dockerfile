FROM anuvaadio/python3.6-opencv-4.1.0:5
COPY / /app
WORKDIR /app
ARG D_F
ENV DEBUG_FLUSH=$D_F
# RUN apk update && apk add -U \
#       --virtual .build-dependencies \
#         build-base \
#         openblas-dev \
#         unzip \
#         wget \
#         cmake \
#         libjpeg-turbo-dev \
#         libpng-dev \
#         jasper-dev \
#         tiff-dev \
#         libwebp-dev \
#         clang-dev \
#         linux-headers

RUN apk add tesseract-ocr
RUN tesseract -v
RUN apk add --upgrade tesseract-ocr-data-hin
RUN apk add --upgrade tesseract-ocr-data-tam
RUN apk add --upgrade tesseract-ocr-data-kan
RUN pip install -r requirements.txt
RUN apk update && apk add poppler-utils
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh
ENTRYPOINT ["sh","/usr/bin/start.sh"]
