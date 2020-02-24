
FROM python:3.6.9

COPY . /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt
WORKDIR /app/src
ENTRYPOINT ["python"]
CMD ["run.py"]