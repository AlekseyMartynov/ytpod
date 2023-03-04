FROM private/ytbase

RUN apk add --no-cache py3-pip
RUN pip3 install PyRSS2Gen --use-pep517

ADD cmd.sh rssgen.py /

CMD [ "sh", "/cmd.sh" ]
