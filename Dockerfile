FROM python:3.5

MAINTAINER David Lyon <dblyon@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV HOME /root
ENV PYTHONPATH "/usr/lib/python3/dist-packages:/usr/local/lib/python3.5/site-packages"

# Install dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
        gcc \
        build-essential \
        zlib1g-dev \
        wget \
        unzip \
        cmake \
        python3-dev \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
    && apt-get clean

# Install Python packages
RUN pip install --upgrade pip \
    && pip install \
        numpy \
        scipy \
        cython \
        pandas \
    && rm -fr /root/.cache

RUN mkdir -p /opt/services/flaskapp/src
#VOLUME ["/opt/services/flaskapp/src"]
# We copy the requirements.txt file first to avoid cache invalidations
RUN echo $PYTHONPATH
COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements.txt
COPY . /opt/services/flaskapp/src
EXPOSE 5911
CMD ["python", "runserver.py"]
