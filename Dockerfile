FROM alpine:3.11

RUN apk add --no-cache python3 ffmpeg
RUN pip3 install youtube-dl PyRSS2Gen

ADD cmd.sh rssgen.py /

CMD [ "sh", "/cmd.sh" ]
