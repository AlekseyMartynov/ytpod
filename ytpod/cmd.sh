. /opt/venv/bin/activate

mkdir -p /ytpod/public
chmod 0777 /ytpod_update

while true; do
    for i in m4a part webm; do
        rm -f /ytpod/public/*.$i
    done

    /yt-dlp --update-to stable

    for url in $(awk '{print $1}' /ytpod/urls.txt); do
        /yt-dlp -v -i -x \
            --cookies /cookies.txt \
            --no-write-playlist-metafiles \
            --audio-format mp3 \
            --audio-quality 5 \
            --playlist-items 1-3 \
            --match-filter '!is_live & duration > 299 & url!*=yt_premiere_broadcast' \
            --download-archive '/ytpod/archive.txt' \
            --write-info-json \
            --embed-chapters \
            --write-thumbnail \
            --convert-thumbnails webp \
            -o "/ytpod/public/$(date +%Y%m%d%H%M)-%(id)s.%(ext)s" \
            $url
    done

    python3 /rssgen.py

    rm -f /ytpod_update/requested

    for i in `seq 12345`; do
        sleep 1
        [ -f /ytpod_update/requested ] && break
    done
done
