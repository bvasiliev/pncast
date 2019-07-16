#! /usr/bin/python

""" Youtube iteration """

from __future__ import unicode_literals
import youtube_dl


class YoutubeLogger(object):
    """ Log youtube errors to stdout """
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print msg


YOUTUBE_OPTIONS = {
    'format': '140',
    'simulate': False,
    'quiet': True,
    'socket-timeout': 5,
    'logger': YoutubeLogger(),
    }


downloader = youtube_dl.YoutubeDL(YOUTUBE_OPTIONS)


def get_audio_full_info(url):
    """ Return video info dict from youtube url """
    with downloader:
        result = downloader.extract_info(url)
    return result


def get_audio_url(url):
    """ Return audio url from youtube url """
    return get_audio_full_info(url)['url']


def get_audio_duration(url):
    """ Return audio duration in seconds from youtube url """
    return get_audio_full_info(url)['duration']


def get_audio_filesize(url):
    """ Return audio size in bytes from youtube url """
    return get_audio_full_info(url)['filesize']


if __name__ == '__main__':
    pass
