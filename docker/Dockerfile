FROM python:3.12

WORKDIR /app

# install google chrome
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# set display port to avoid crash
ENV DISPLAY=:99

COPY ../requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt