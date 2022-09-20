FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install -r requirements.txt

COPY f1rstResponder.py /usr/src/app/

ENTRYPOINT ["python", "f1rstResponder.py"]