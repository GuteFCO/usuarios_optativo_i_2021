FROM python:latest

RUN mkdir -p /app/src

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app/src

EXPOSE 5000

COPY ./src /app/src

CMD ["flask", "run", "--host=0.0.0.0"]
