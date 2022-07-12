FROM python

RUN pip install flask
RUN pip install requests

ADD calculator.py /root
COPY templates /root/templates
WORKDIR /root
