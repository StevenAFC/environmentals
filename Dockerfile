FROM python:latest

#python docker using Debian, adding raspbian respository to download gpiod. 
RUN echo 'deb http://raspbian.raspberrypi.org/raspbian/ bullseye main contrib non-free rpi' >> /etc/apt/sources.list

RUN wget https://archive.raspbian.org/raspbian.public.key -O - | apt-key add -

RUN apt-get update

RUN apt-get install -y gpiod

# Set up virtual environment
RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

RUN ls /opt/venv/lib/python3.10/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/

# Hack https://github.com/adafruit/Adafruit_Blinka/issues/547
RUN wget https://github.com/adafruit/Adafruit_Blinka/raw/main/src/adafruit_blinka/microcontroller/bcm283x/pulseio/libgpiod_pulsein64
RUN cp libgpiod_pulsein64 /opt/venv/lib/python3.10/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/libgpiod_pulsein64
RUN chmod u=rwx,g=rwx,o=rwx /opt/venv/lib/python3.10/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/libgpiod_pulsein64

# Run the application:
COPY main.py .
CMD . /opt/venv/bin/activate && exec python -u main.py