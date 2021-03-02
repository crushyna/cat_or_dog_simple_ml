FROM tiangolo/uwsgi-nginx-flask:python3.8

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 0

# This refers to local, development ML server. Change it to your published FunctionApp:
ENV ML_SERVER 'http://mlserver/api/MLServer'

# Install OpenSSH and set the password for root to "Docker!". In this example, "apk add" is the install instruction for an Alpine Linux-based image.
COPY debian_sources.list /etc/apt/sources.list.d/

RUN apt-get update
RUN apt-get install openssh-client \
     && echo "root:Docker!" | chpasswd

# Copy the sshd_config file to the /etc/ssh/ directory
COPY sshd_config /etc/ssh/

# Open port 2222 for SSH access
EXPOSE 80 2222

COPY ./app /app

# required for Pillow:
# RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
