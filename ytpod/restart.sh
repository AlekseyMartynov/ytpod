#!/bin/bash -e

NAME=ytpod

docker build -t private/$NAME .
docker rm -f $NAME || true

. secrets

docker run -dti \
    --name=$NAME \
    --restart=unless-stopped \
    -e YTPOD_URL="$YTPOD_URL" \
    -v ytpod:/ytpod \
    -v ytpod_update:/ytpod_update \
    --log-opt max-size=100k \
    --log-opt max-file=2 \
    private/$NAME
