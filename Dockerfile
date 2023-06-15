FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    imagemagick \
    libmagickwand-dev

# Create a new directory and set it as the working directory
WORKDIR /code

COPY ./app.py /code/app.py
COPY ./policy.xml /code/policy.xml

RUN cp /code/policy.xml /etc/ImageMagick-6/policy.xml
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app


RUN wget https://github.com/acl-org/aclpubcheck/archive/refs/heads/main.zip
RUN unzip main.zip
RUN cd aclpubcheck-main
RUN pip install -e ./aclpubcheck-main


RUN pip install gradio==3.34.0


EXPOSE 7860

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "7860"]
