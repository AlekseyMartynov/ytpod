#!/bin/bash -e

NAME=ytpod

docker build -t private/$NAME .
docker rm -f $NAME || true

docker run -dti \
    --name=$NAME \
    --restart=unless-stopped \
    -v ytpod:/ytpod \
    --log-opt max-size=100k \
    --log-opt max-file=2 \
    private/$NAME
