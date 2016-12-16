#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import date
from email.Utils import formatdate
import requests
import json

session = requests.Session()

http_headers = {'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6',
	'Accept': 'application/json,image/webp,image/*,*/*;q=0.8', 
	'Referer': 'https://postnauka.ru/api/v1/posts',
	'User-Agent': 'pncast.ru',
	'Proxy-Connection': 'keep-alive' }

api_url = 'https://postnauka.ru/api/v1/posts'

api_url_post_template = 'https://postnauka.ru/api/v1/posts/%d?expand=youtube,date,tagscloud'
youtube_url_template = 'https://www.youtube.com/watch?v=%s'
postnauka_url_template = 'http://postnauka.ru/video/%d'

month_ru = { 
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
	try:
		request = session.get(url, headers=http_headers)
	except requests.exceptions.RequestException as e:
		print e
		return None
	if request.status_code is not 200:
		return None
	else:
		return request.content


def fetch_json(url):
	content = site_request(url)
	if content:
		return json.loads(content)
	else:
		return None


def fetch_video_info(video_id):
	return fetch_json(api_url_post_template % video_id)


def fetch_last_posts():
	return fetch_json(api_url)


def resolve_tags(tagscloud):
	""" Resolv tags to themes """
	themes = {}
	if isinstance(tagscloud, dict):
		""" api fuckup hack """
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
	dd, month, yyyy = date_string.split()
	mm = month_ru[month]
	return date( year=int(yyyy), month=int(mm), day=int(dd) )


def datetime_to_rfc822(date):
	return formatdate(float(date.strftime('%s')))


def duration_to_hms(duration):
	mins, seconds = divmod(duration, 60)
	hours, mins = divmod(mins, 60)
	if not hours:
		return "%02d:%02d" % (mins, seconds)
	else:
		return "%d:%02d:%02d" % (hours, mins, seconds)


if __name__ == '__main__':
	pass
