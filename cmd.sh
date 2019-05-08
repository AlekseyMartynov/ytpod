mkdir -p /ytpod/public

while true; do
    pip3 install --upgrade youtube-dl

    for url in $(cat /ytpod/urls.txt); do
        youtube-dl -v -i -x \
            --audio-format mp3 \
            --audio-quality 5 \
            --playlist-items 1-3 \
            --match-filter '!is_live' \
            --download-archive '/ytpod/archive.txt' \
            --write-info-json \
            -o '/ytpod/public/%(upload_date)s-%(id)s.%(ext)s' \
            $url
    done

    python3 /rssgen.py

    sleep 12345
done
