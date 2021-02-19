FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

# This refers to local, development ML server. Change it to your published FunctionApp:
ENV ML_SERVER 'http://mlserver/api/MLServer?data='

COPY ./app /app

# required for Pillow:
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
