FROM alpine:3.22

RUN apk add --no-cache ffmpeg inotify-tools python3
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /yt-dlp && chmod +x /yt-dlp

ADD cookies.txt /

STOPSIGNAL SIGKILL
