#! /usr/bin/python
# -*- coding: utf-8 -*-

""" Postnauka API parser stuff """

from __future__ import unicode_literals
import json
from datetime import date
import requests
from email.Utils import formatdate


session = requests.Session()

HTTP_HEADERS = {'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6',
                'Accept': 'application/json,image/webp,image/*,*/*;q=0.8',
                'Referer': 'https://postnauka.ru/api/v1/posts',
                'User-Agent': 'pncast.ru',
                'Proxy-Connection': 'keep-alive'}

API_URL = 'https://postnauka.ru/api/v1/posts'

API_URL_POST_TEMPLATE = 'https://postnauka.ru/api/v1/posts/%d?expand=youtube,date,tagscloud'
YOUTUBE_URL_TEMPLATE = 'https://www.youtube.com/watch?v=%s'
POSTNAUKA_URL_TEMPLATE = 'http://postnauka.ru/video/%d'

MONTH_RU = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
    }


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
        tags = []
        for tag_id, tag in tagscloud.iteritems():
            tags.append(tag)
    elif isinstance(tagscloud, list):
        tags = tagscloud
    else:
        return themes
    for tag in tags:
        themes[tag['alias']] = tag['name']
    return themes


def string_to_datetime(date_string):
    """ Return datetime from russian string """
    dd, month, yyyy = date_string.split()
    mm = MONTH_RU[month]
    return date(year=int(yyyy), month=int(mm), day=int(dd))


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


if __name__ == '__main__':
    pass
