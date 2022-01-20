FROM python:3-alpine
LABEL maintainer="zekro <contact@zekro.de>"
WORKDIR /var/stargrab
COPY requirements.txt .
COPY stargrab stargrab
RUN apk add git --no-cache
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /var/repos
ENV SG_TARGET="/var/repos"
ENTRYPOINT [ "python", "stargrab/main.py" ]