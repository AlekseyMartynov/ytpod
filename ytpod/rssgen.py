import datetime
import glob
import html
import json
import os
import PyRSS2Gen

DIR = "/ytpod/public"
URL = os.environ["YTPOD_URL"]
KEEP_DAYS = 15

info_path_list = glob.glob(DIR + "/*.info.json")
info_path_list.sort(reverse=True)

episodes = [ ]
trash = [ ]

keep_start_time = datetime.datetime.now() - datetime.timedelta(days=KEEP_DAYS)

for info_path in info_path_list:
    with open(info_path) as f:
        info = json.load(f)

    info_slug = os.path.basename(info_path)[:-10]
    info_time = datetime.datetime.strptime(info_slug[:12], "%Y%m%d%H%M")

    audio_name = ""
    thumb_name = ""

    for ext in [".opus", ".m4a", ".mp4", ".mp3"]:
        if os.path.isfile(DIR + "/" + info_slug + ext):
            audio_name = info_slug + ext
            break

    for ext in [".webp", ".jpg"]:
        if os.path.isfile(DIR + "/" + info_slug + ext):
            thumb_name = info_slug + ext
            break

    if info_time < keep_start_time or len(episodes) > 19 or not audio_name:
        trash.append(info_path)
        if audio_name:
            trash.append(DIR + "/" + audio_name)
        if thumb_name:
            trash.append(DIR + "/" + thumb_name)
        continue

    title = info.get("title")
    author = info.get("uploader") or info.get("uploader_id")
    orig_url = info.get("webpage_url")
    upload_date = info.get("upload_date") or "00000000"
    thumbnail_url = URL + "/" + thumb_name

    episodes.append(PyRSS2Gen.RSSItem(
        title = title,
        link = orig_url,
        description = "<p>%s &bull; %s.%s.%s</p> <p><a href=\"%s\"><img src=\"%s\"></a></p>" % (
            html.escape(author),
            upload_date[6:8], upload_date[4:6], upload_date[0:4],
            html.escape(orig_url),
            html.escape(thumbnail_url)
        ),
        author = author,
        enclosure = PyRSS2Gen.Enclosure(
            url = URL + "/" + audio_name,
            type = "audio/mpeg",
            length = 0
        ),
        guid = orig_url,
        pubDate = info_time
    ))

    print("Episode: " + title)

rss = PyRSS2Gen.RSS2(
    title = "YouTube",
    link = "",
    description = "",
    image = PyRSS2Gen.Image(
        url = "https://placehold.co/720/272727/f00.png?text=YT&font=opensans",
        title = "YouTube",
        link = ""
    ),
    items = episodes,
)

with open(os.path.join(DIR, "feed.xml"), "w", encoding = "utf-8") as f:
    rss.write_xml(f, encoding="utf-8")

for path in trash:
    try:
        os.unlink(path)
        print("Deleted: " + path)
    except:
        print("Cannot delete: " + path)
