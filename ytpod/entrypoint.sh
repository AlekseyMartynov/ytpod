renice -n 10 -p $$
ionice -c 3  -p $$

. /opt/venv/bin/activate

mkdir -p /ytpod/public
chmod 0777 /ytpod_update

touch /ytpod_update/urls_dynamic.txt
chmod 0666 /ytpod_update/urls_dynamic.txt

combine_urls() {
    cat /ytpod_update/urls_dynamic.txt
    awk '{print $1}' /ytpod/urls.txt
}

while true; do
    for i in m4a part webm; do
        rm -f /ytpod/public/*.$i
    done

    /yt-dlp --update-to stable

    for url in $(combine_urls); do
        /yt-dlp -v -i -x \
            --extractor-args "youtube:player_client=default,-web_creator" \
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

    inotifywait -t 12345 -e close_write --include 'requested' /ytpod_update
done
