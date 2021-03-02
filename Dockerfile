FROM tiangolo/uwsgi-nginx-flask:python3.8

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 0

# This refers to local, development ML server. Change it to your published FunctionApp:
ENV ML_SERVER 'http://mlserver/api/MLServer'

# Install OpenSSH and set the password for root to "Docker!". In this example, "apt-get" is the install instruction for an Alpine Linux-based image.
COPY debian_sources.list /etc/apt/sources.list.d/
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd

COPY sshd_config /etc/ssh/
EXPOSE 2222 80

COPY ./app /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
