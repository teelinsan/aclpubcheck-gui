FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    imagemagick \
    libmagickwand-dev

WORKDIR .

COPY ./app.py ./app.py
COPY ./policy.xml ./policy.xml

RUN wget https://github.com/acl-org/aclpubcheck/archive/refs/heads/main.zip
RUN unzip main.zip
RUN cd aclpubcheck-main
RUN pip install -e ./aclpubcheck-main
RUN cp policy.xml /etc/ImageMagick-6/policy.xml

RUN cd ..
RUN pip install gradio==3.34.0


EXPOSE 7860

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "7860"]