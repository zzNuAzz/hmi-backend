import pytube
import sys

url = sys.argv[1]
yt = pytube.YouTube(url)
mp4files = yt.streams.get_highest_resolution().download(output_path="video/", filename="pythontutorial.mp4")

# d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
    # d_video.download("video/")
