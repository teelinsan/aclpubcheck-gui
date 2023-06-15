FROM python:3.9

WORKDIR .

COPY ./app.py ./app.py
COPY ./policy.xml ./policy.xml

RUN apt-get update
RUN wget https://github.com/acl-org/aclpubcheck/archive/refs/heads/main.zip
RUN unzip main.zip
RUN cd aclpubcheck-main
RUN apt-get install libmagickwand-dev
RUN pip install -e ./aclpubcheck-main
RUN cp policy.xml /etc/ImageMagick-6/policy.xml

RUN cd ..
RUN pip install gradio==3.34.0


EXPOSE 7860

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "7860"]