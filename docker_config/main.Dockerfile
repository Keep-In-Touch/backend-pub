FROM python:3.9
USER root
# RUN chmod 777 -R /src
WORKDIR /src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /src/

ENV UWSGI_WSGI_FILE=kit/wsgi.py UWSGI_HTTP=:8000 \
UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 \
UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

RUN apt-get update
RUN apt install -y netcat
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

RUN ls

RUN python manage.py collectstatic --noinput



RUN chmod 777 -R /src

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000
