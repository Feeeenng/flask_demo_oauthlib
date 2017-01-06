FROM ubuntu:16.04


RUN pip install python-weixin
RUN pip install flask_oauthlib


EXPOSE 80

CMD ['python','qq_demo.py']


