FROM alpine:3.9

RUN apk add --no-cache python3 ffmpeg
RUN pip3 install youtube-dl

ADD cmd.sh /

CMD [ "sh", "/cmd.sh" ]
