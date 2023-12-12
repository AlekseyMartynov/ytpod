FROM alpine:3.17

# Use older ffmpeg because of https://github.com/yt-dlp/yt-dlp/issues/8641
RUN apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/v3.15/community ffmpeg=4.4.1-r2

RUN apk add --no-cache python3
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /yt-dlp && chmod +x /yt-dlp
