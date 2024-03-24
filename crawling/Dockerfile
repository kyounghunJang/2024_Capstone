FROM flink:latest

# install python3 and pip3
RUN apt-get update -y && \
apt-get install -y openjdk-11-jdk python3 python3-pip python3-dev gdebi-core sudo
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
# install PyFlink
COPY apache-flink*.tar.gz /
RUN pip3 install apache-flink-libraries
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64
RUN pip3 install apache-flink   



RUN wget http://launchpadlibrarian.net/660838579/chromium-codecs-ffmpeg-extra_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
# Fetch chromium-browse
RUN wget http://launchpadlibrarian.net/660838574/chromium-browser_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
# Fetch chromium-chromedriver
RUN wget http://launchpadlibrarian.net/660838578/chromium-chromedriver_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb

RUN sudo gdebi -n chromium-codecs-ffmpeg-extra_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
RUN sudo gdebi -n chromium-browser_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
RUN sudo gdebi -n chromium-chromedriver_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb

RUN sudo rm chromium-codecs-ffmpeg-extra_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
RUN sudo rm chromium-browser_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb
RUN sudo rm chromium-chromedriver_112.0.5615.49-0ubuntu0.18.04.1_arm64.deb