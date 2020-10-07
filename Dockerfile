FROM python:3.7

COPY . /opt/app
WORKDIR /opt/app

RUN conda install -r requirements.txt

CMD python App/main.py