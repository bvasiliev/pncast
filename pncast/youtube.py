#! /usr/bin/python

from __future__ import unicode_literals
import youtube_dl


class youtube_logger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)


youtube_options = {
	'format': '140',
	'simulate': True,
	'quiet': True,
	'socket-timeout': 5,
	'logger': youtube_logger(),
	}


downloader = youtube_dl.YoutubeDL(youtube_options)
rickroll = "http://www.youtube.com/watch?v=GUl9_5kK9ts"


def get_audio_full_info(url):
	with downloader:
		result = downloader.extract_info(url)
	return result


def get_audio_url(url):
	with downloader:
		result = downloader.extract_info(url)
	audio_url = result['url']
	return audio_url


def get_audio_duration(url):
	with downloader:
		result = downloader.extract_info(url)
	audio_duration = result['duration']
	return audio_duration


def get_audio_filesize(url):
	with downloader:
		result = downloader.extract_info(url)
	audio_filesize = result['filesize']
	return audio_filesize


if __name__ == '__main__':
	pass
