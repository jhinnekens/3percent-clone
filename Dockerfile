
FROM python:3.6.9

COPY . /app

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]