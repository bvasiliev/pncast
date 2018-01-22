#! /usr/bin/python
# -*- coding: utf-8 -*-

""" Postnauka API parser stuff """

from __future__ import unicode_literals
import json
from datetime import date, datetime
import requests
from email.Utils import formatdate
from jinja2 import Environment, FileSystemLoader


session = requests.Session()

JINJA = Environment(loader=FileSystemLoader('templates'))
TEMPLATE_RTF = JINJA.get_template('description.xml')


HTTP_HEADERS = {'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6',
                'Accept': 'application/json,image/webp,image/*,*/*;q=0.8',
                'Referer': 'https://postnauka.ru/api/v1/posts',
                'User-Agent': 'pncast.ru',
                'Proxy-Connection': 'keep-alive'}

API_URL = 'https://postnauka.ru/api/v1/posts'

API_URL_POST_TEMPLATE = 'https://postnauka.ru/api/v1/posts/%d?expand=youtube,date,tagscloud'
YOUTUBE_URL_TEMPLATE = 'https://www.youtube.com/watch?v=%s'
YOUTUBE_THUMBNAIL_URL_TEMPLATE = 'https://i.ytimg.com/vi/%s/maxresdefault.jpg'
POSTNAUKA_URL_TEMPLATE = 'http://postnauka.ru/video/%d'

THEME_BLACKLIST = ['video']


def site_request(url):
    """ Return content from http url"""
    try:
        request = session.get(url, headers=HTTP_HEADERS)
    except requests.exceptions.RequestException as exception:
        print exception
        return None
    if request.status_code is not 200:
        return None
    else:
        return request.content


def fetch_json(url):
    """ Loads json from http url """
    content = site_request(url)
    if content:
        return json.loads(content)
    else:
        return None


def fetch_video_info(video_id):
    """ Loads video info json from api by id """
    return fetch_json(API_URL_POST_TEMPLATE % video_id)


def fetch_last_posts():
    """ Loads last posts json from api """
    return fetch_json(API_URL)


def resolve_tags(tagscloud):
    """ Resolv api tags to themes dict {id: name} """
    themes = {}
    if isinstance(tagscloud, dict):
        tags = tagscloud.values()
    elif isinstance(tagscloud, list):
        tags = tagscloud
    else:
        return themes
    for tag in tags:
        if tag['alias'] not in THEME_BLACKLIST: themes[tag['alias']] = tag['name']
    return themes


def string_to_datetime(date_string):
    """ Return datetime from string """
    return datetime.strptime(date_string, '%d %B %Y')


def datetime_to_rfc822(date_obj):
    """ Return rfc822 string from datetime """
    return formatdate(float(date_obj.strftime('%s')))


def duration_to_hms(duration):
    """ Return 00:00 time from seconds int """
    mins, seconds = divmod(duration, 60)
    hours, mins = divmod(mins, 60)
    if not hours:
        return "%02d:%02d" % (mins, seconds)
    else:
        return "%d:%02d:%02d" % (hours, mins, seconds)


def redner_description_rtf(author, description, themes, url):
    return TEMPLATE_RTF.render(**locals())
   

if __name__ == '__main__':
    pass
