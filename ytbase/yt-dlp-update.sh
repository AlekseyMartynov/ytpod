RELEASE_REPO=ytdl-patched/yt-dlp
RELEASE_FILE=yt-dlp

if wget https://github.com/$RELEASE_REPO/releases/latest/download/$RELEASE_FILE -O /yt-dlp-tmp; then
    rm -f /yt-dlp
    mv /yt-dlp-tmp /yt-dlp
    chmod +x /yt-dlp
fi
