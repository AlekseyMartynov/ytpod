FROM alpine:3.13

RUN apk add --no-cache python3 py3-pip ffmpeg gcc musl-dev
RUN pip3 install yt-dlp PyRSS2Gen

ADD cmd.sh rssgen.py /

CMD [ "sh", "/cmd.sh" ]
