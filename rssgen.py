import datetime
import glob
import html
import json
import os
import PyRSS2Gen

DIR = "/ytpod/public"
URL = "https://do-3.amartynov.ru/ytpod"
KEEP_DAYS = 15

info_path_list = glob.glob(DIR + "/*.info.json")
info_path_list.sort(reverse=True)

episodes = [ ]
trash = [ ]

trash_start_date = datetime.datetime.today() - datetime.timedelta(days=KEEP_DAYS)

for info_path in info_path_list:
    with open(info_path) as f:
        info = json.load(f)

    mp3_name = os.path.basename(info_path).replace(".info.json", ".mp3")
    date = datetime.datetime.strptime(info["upload_date"], "%Y%m%d")

    if date < trash_start_date:
        trash += [ info_path, os.path.join(DIR, mp3_name) ]
        continue

    title = info["title"]
    author = info["uploader"]
    orig_url = info["webpage_url"]

    episodes.append(PyRSS2Gen.RSSItem(
        title = title,
        link = orig_url,
        description = "<p>%s</p> <p><a href=\"%s\"><img src=\"%s\"></a></p>" % (
            html.escape(author),
            html.escape(orig_url),
            html.escape(info["thumbnail"])
        ),
        author = author,
        enclosure = PyRSS2Gen.Enclosure(
            url = URL + "/" + mp3_name,
            type = "audio/mpeg",
            length = 0
        ),
        guid = orig_url,
        pubDate = date
    ))

    print("Episode: " + title)

rss = PyRSS2Gen.RSS2(
    title = "YouTube",
    link = "",
    description = "",
    image = PyRSS2Gen.Image(
        url = "https://via.placeholder.com/720/272727/f00?text=YT",
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
