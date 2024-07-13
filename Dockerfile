FROM python:3.11-slim-buster

WORKDIR /app
COPY . /app

RUN mkdir -p /home
ADD docker-entrypoint.sh /home
RUN chmod +x /home/docker-entrypoint.sh

RUN pip3 install poetry
RUN poetry install 

EXPOSE 9010

ENTRYPOINT ["/home/docker-entrypoint.sh"]