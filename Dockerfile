FROM python:2.7


RUN mkdir -p /app
COPY . /app
RUN pip install python-weixin
RUN pip install flask_oauthlib


EXPOSE 80

CMD ['python','/app/qq_demo.py']


