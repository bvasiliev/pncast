#! /usr/bin/python

from __future__ import unicode_literals
from pncast import youtube, db
from datetime import datetime
from dateparser import parse as dateparser
from email.Utils import formatdate
import requests
import simplejson as json

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


def site_request(url):
	try:
		request = session.get(url, headers=http_headers, verify=False)
	except requests.exceptions.RequestException as e:
		print e
		return None
	if request.status_code is not 200:
		return None
	else:
		return request.content


def fetch_video(video_id):
	video = db.video.select().where(db.video.id == video_id)
	if video.exists():
		return None

	video_url = api_url_post_template % video_id
	content = site_request(video_url)
	if content:
		video_info = json.loads(content)
	else:
		return None

	audio_url = '/audio/%d.m4a' % video_id
	subject = video_info['title']
	description = video_info['description']
	date = string_to_datetime(video_info['date'])
	date_rfc822 = datetime_to_rfc822(date)
	url = postnauka_url_template % video_id
	youtube_url = youtube_url_template % video_info['youtube']
	audio_info = youtube.get_audio_full_info(youtube_url)

	author_info = video_info['authors'][0]
	author_id_url = author_info['author_link']
	author_id = author_id_url.split('/')[2]
	author_name = author_info['author_name']
	author_desc = author_info['author_description']

	author = db.get_or_update_author(author_id = author_id, name = author_name, description = author_desc)

	video, result = db.video.create_or_get(id = video_id, \
			author = author.id, \
			subject = subject, \
			description = description, \
			date = date, \
			date_rfc822 = date_rfc822, \
			url = url, \
			youtube_url = youtube_url, \
			audio_url = audio_url, \
			audio_duration = audio_info['duration'], \
			audio_duration_hms = duration_to_hms(audio_info['duration']), \
			audio_filesize = audio_info['filesize'], \
			youtube_thumbnail = audio_info['thumbnail']
			)

	'''api fuckup hack:'''	
	if isinstance(video_info['tagscloud'], dict):
		tagscloud = []
		for tag_id, tag in video_info['tagscloud'].iteritems():
			tagscloud.append(tag)
	else:
		tagscloud = video_info['tagscloud']

	if  video_info['tags']: tagscloud.append( {'alias': video_info['tags']['eng'], 'name': video_info['tags']['rus'] } )
	
	for tag in tagscloud:
		theme, created = db.theme.get_or_create(id = tag['alias'], name = tag['name'])
		theme_to_video, theme_to_video_created = db.theme_to_video.create_or_get(theme = theme.id, video = video.id)
		result = result and theme_to_video_created	
	return result


def string_to_datetime(date_string):
	return dateparser(date_string)


def datetime_to_rfc822(date):
	return formatdate(float(date.strftime('%s')))


def duration_to_hms(duration):
	mins, seconds = divmod(duration, 60)
	hours, mins = divmod(mins, 60)
	if not hours:
		return "%02d:%02d" % (mins, seconds)
	else:
		return "%d:%02d:%02d" % (hours, mins, seconds)


def fetch_feed(url):
	content = site_request(url)
	if content:
		feed = json.loads(content)
	else:
		return None
	for item in feed:
		if item['type'] == 'video':
			print item['id']
			fetch_video(int(item['id']))
	

if __name__ == '__main__':
	fetch_feed(api_url)
