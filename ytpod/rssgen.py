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

    info_basename = os.path.basename(info_path)
    info_time = datetime.datetime.strptime(info_basename[:12], "%Y%m%d%H%M")
    mp3_name = info_basename.replace(".info.json", ".mp3")
    mp3_path = os.path.join(DIR, mp3_name)
    thumb_name = mp3_name.replace(".mp3", ".webp")
    thumb_path = os.path.join(DIR, thumb_name)

    if info_time < keep_start_time or len(episodes) > 19 or not os.path.isfile(mp3_path):
        trash += [ info_path, mp3_path, thumb_path ]
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
            url = URL + "/" + mp3_name,
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
