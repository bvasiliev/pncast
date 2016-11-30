#! /usr/bin/python

from __future__ import unicode_literals
from datetime import datetime
from pncast import youtube, db
from time import sleep
from lxml import html
import rfc822
import requests

session = requests.Session()

http_headers = {'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6',
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Referer': 'http://postnauka.ru/video/',
        'User-Agent': 'pncast.ru',
        'Proxy-Connection': 'keep-alive' }



def get_audio_content_length(url):
	'''Trick for changed youtube API, must be removed'''
	youtube_audio_url = youtube.get_audio_url(url)
	response = requests.head(youtube_audio_url, allow_redirects=True)
	length = int(response.headers['content-length'])
	return length







videos = db.video.select().where((db.video.audio_filesize == 0))

for video in videos:
	print video.id, video.subject
	audio_filesize = get_audio_content_length(video.youtube_url)
	video.audio_filesize = audio_filesize
	video.save()

"""
	audio_info = youtube.get_audio_full_info(video.youtube_url)
	try:
		video.audio_duration = audio_info['duration']
		video.audio_filesize = audio_info['filesize']
		video.youtube_thumbnail = audio_info['thumbnail']
		video.save()
	except KeyError:
		print "error", video.id
		continue
videos = db.video.select()

for video in videos:
	print video.id, video.subject
	try:
		video.audio_url = "/audio/" + str(video.id) + ".m4a"
		video.save()
	except KeyError:
		print "error", video.id
		continue
"""
