FROM python:3.7.2-stretch
ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD sleep 5 && flask db upgrade && python wsgi.py
