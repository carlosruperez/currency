FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /webapps

RUN apt-get update && apt-get install \
  -y --no-install-recommends apt-utils \
  python-dev python3-dev \
  build-essential libssl-dev libffi-dev \
  libxml2-dev libxslt1-dev zlib1g-dev \
   python3-psycopg2

RUN pip install -U pip setuptools

# Copying the requirements, this is needed because at this point the volume isn't mounted yet
COPY requirements.txt /webapps/

# Installing requirements, if you don't use this, you should.
# More info: https://pip.pypa.io/en/stable/user_guide/
RUN pip install -r requirements.txt

COPY . /webapps/
