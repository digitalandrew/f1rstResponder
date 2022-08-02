FROM python:3

WORKDIR /usr/src/app

COPY f1rstResponder.py /usr/src/app/

ENTRYPOINT ["python", "f1rstResponder.py"]
