from __future__ import unicode_literals
import yt_dlp as youtube_dl  # Note the change here to yt_dlp

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=hyEbJoPfHtw'])