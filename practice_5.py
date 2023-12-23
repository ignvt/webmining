import os

import pytube
import requests
import youtube_dl


def process(urls):
    for url in urls:
        if "youtube.com" in url:
            yt_download(url, "yt")
        elif "reddit.com" in url:
            reddit_download(url, "reddit")


def yt_download(url, path):
    mkdir(path)
    video_with_highest_resolution = pytube.YouTube(url).streams.get_highest_resolution()
    video_with_highest_resolution.download(f"./{path}")


def reddit_download(url, path):
    response = requests.get(url + ".json")
    data = response.json()
    for video in data["data"]["children"]:
        if "secure_media" in video["data"] and video["data"]["secure_media"] is not None:
            if "reddit_video" in video["data"]["secure_media"]:
                video_url = video["data"]["secure_media"]["reddit_video"]["fallback_url"]
                mkdir(path)
                ydl_opts = {
                    "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])


def download(url, path):
    response = requests.get(url, stream=True)
    with open(path, "wb") as file:
        for part in response.iter_content(chunk_size=1024):
            file.write(part)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    sources = [
        "https://www.youtube.com/watch?v=ex9tML6udCU",
        "https://www.reddit.com/r/videomemes"
    ]
    process(sources)


if __name__ == "__main__":
    main()
