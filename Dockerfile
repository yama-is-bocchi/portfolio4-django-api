FROM python:3.10.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /docker_api
WORKDIR /docker_api
ADD requirements.txt /docker_api/
RUN pip install --upgrade pip && pip install -r requirements.txt