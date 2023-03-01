FROM alpine:3.17

RUN apk add --no-cache ffmpeg gcompat

ADD yt-dlp-update.sh /
RUN sh /yt-dlp-update.sh

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV CONDA_PREFIX=/tmp
