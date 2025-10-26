renice -n 10 -p $$
ionice -c 3  -p $$

mkdir -p /ytpod/public
chmod 0777 /ytpod_update

touch /ytpod_update/urls_dynamic.txt
chmod 0666 /ytpod_update/urls_dynamic.txt

mkfifo /run/yt-dlp-out /run/yt-dlp-err

stdbuf -oL tail -f -n +1 /run/yt-dlp-out &
stdbuf -oL tail -f -n +1 /run/yt-dlp-err | tee -a /ytpod/public/yt-dlp-err.txt &

. /opt/venv/bin/activate

combine_urls() {
    cat /ytpod_update/urls_dynamic.txt
    awk '{print $1}' /ytpod/urls.txt
}

while true; do
    for i in part webm ytdl; do
        rm -f /ytpod/public/*.$i
    done

    /yt-dlp --update-to stable

    truncate -s 0 /ytpod/public/yt-dlp-err.txt

    for url in $(combine_urls); do
        /yt-dlp -v -i -x \
            --color stdout:always \
            --cookies /cookies.txt \
            --no-write-playlist-metafiles \
            --playlist-items 1-3 \
            --match-filter '!is_live & duration > 299 & url!*=yt_premiere_broadcast' \
            --download-archive '/ytpod/archive.txt' \
            --write-info-json \
            --embed-chapters \
            --write-thumbnail \
            -o "/ytpod/public/$(date +%Y%m%d%H%M)-%(id)s.%(ext)s" \
            $url 1>/run/yt-dlp-out 2>/run/yt-dlp-err
    done

    python3 /rssgen.py

    rm -f /ytpod_update/requested

    inotifywait -t 12345 -e close_write --include 'requested' /ytpod_update
done
