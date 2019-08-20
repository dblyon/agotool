FROM python:3.6

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
        cmake \
        build-essential \
        zlib1g-dev \
        wget \
        unzip \
        python3-dev \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        rsync \
        tree \
        vim \
    && apt-get clean

# Install MCL for clustering, install before python packages in case these change
#RUN mkdir -p /software
#RUN cd /software \
#    && wget http://micans.org/mcl/src/mcl-14-137.tar.gz \
#    && tar -xzvf mcl-14-137.tar.gz \
#    && rm mcl-14-137.tar.gz \
#    && cd /software/mcl-14-137 \
#    && ./configure \
#    && make install \
#    && cd /software \
#    && rm -rf /software/mcl-14-137

RUN pip install --upgrade pip
# Install Python packages
RUN pip install --no-cache-dir \
        numpy \
        cython \
        scipy \
        pandas \
        jupyter \
        notebook \
    && rm -rf /root/.cache

RUN mkdir -p /opt/services/flaskapp/src
#VOLUME ["/opt/services/flaskapp/src"]
#RUN echo $PYTHONPATH

# We copy the requirements.txt file first to avoid cache invalidations
COPY ./app/requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /root/.cache

COPY ./app /opt/services/flaskapp/src

RUN cd python && python setup.py build_ext --inplace -f

COPY ./app/.bashrc /root/.bashrc
#COPY . /opt/services/flaskapp/src
#COPY ./data/PostgreSQL/downloads/*.obo /agotool_data/PostgreSQL/downloads/

# change permissions for nginx, otherwise problems on Aquarius
#RUN find /opt/services/flaskapp/src/static -type f -exec chmod 644 {} \;

WORKDIR /opt/services/flaskapp/src
EXPOSE 5912
CMD ["python", "runserver.py", "0.0.0.0", "5912"]
