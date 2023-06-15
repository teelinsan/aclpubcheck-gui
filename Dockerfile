FROM python:3.9

WORKDIR .

COPY ./requirements.txt ./requirements.txt
COPY ./app.py ./app.py
COPY ./policy.xml ./policy.xml

RUN apt-get update
RUN https://github.com/acl-org/aclpubcheck/archive/refs/heads/main.zip
RUN unzip /content/main.zip
RUN cd aclpubcheck-main
RUN apt-get install libmagickwand-dev
RUN pip install -e .
RUN cp policy.xml /etc/ImageMagick-6/policy.xml

RUN cd ..
RUN pip install --no-cache-dir --upgrade -r requirements.txt


EXPOSE 7860

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "7860"]