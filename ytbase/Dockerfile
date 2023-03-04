FROM alpine:3.17

RUN apk add --no-cache ffmpeg python3

ADD yt-dlp-update.sh /
RUN sh /yt-dlp-update.sh
