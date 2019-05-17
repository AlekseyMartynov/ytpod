mkdir -p /ytpod/public

while true; do
    pip3 install --upgrade youtube-dl

    for url in $(cat /ytpod/urls.txt); do
        youtube-dl -v -i -x \
            --audio-format mp3 \
            --audio-quality 5 \
            --playlist-items 1-3 \
            --match-filter '!is_live & duration > 299' \
            --download-archive '/ytpod/archive.txt' \
            --write-info-json \
            -o "/ytpod/public/$(date +%Y%m%d%H%M)-%(id)s.%(ext)s" \
            $url
    done

    python3 /rssgen.py

    sleep 12345
done
