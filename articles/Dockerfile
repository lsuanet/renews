FROM python:3.7.0-slim
MAINTAINER Lars Suanet

# create logging dir
RUN mkdir /logs
RUN touch /logs/app.log

# install requirements
RUN apt-get update
RUN apt-get install -y libpq-dev python-dev build-essential
RUN pip install --upgrade pip setuptools
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

# add application to image
COPY app /app
WORKDIR /app/

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]