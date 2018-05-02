# Python application base for Docker on RPI
FROM resin/rpi-raspbian:latest
ENTRYPOINT []

# Install base packages
RUN apt-get -qy install \
python3 \
python3-pip \
python3-dev \
gcc \
make

RUN apt-get -q update
RUN apt-get -q upgrade

# Copy application to app to docker dir
COPY ./ /usr/app
WORKDIR /usr/app

# View location and directory
RUN pwd && ls

# Install python requirements
# RUN pip3 install -r ./requirements.txt

# Run program script
# CMD ["bash", "start.sh"]
