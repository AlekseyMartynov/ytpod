FROM private/ytbase

RUN apk add --no-cache py3-pip
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip3 install PyRSS2Gen

ADD entrypoint.sh rssgen.py /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
