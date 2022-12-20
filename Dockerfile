FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app/
WORKDIR /app/
EXPOSE 8000
EXPOSE 5555