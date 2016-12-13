#! /usr/bin/python

from __future__ import unicode_literals
from pncast import youtube, db, parser

youtube_url_template = 'https://www.youtube.com/watch?v=%s'
postnauka_url_template = 'http://postnauka.ru/video/%d'


def fetch_video(video_id):
	video = db.video.select().where(db.video.id == video_id)
	if video.exists():
		return None

	video_info = parser.fetch_video_info(video_id)
	if not video_info: 
		return None
	
	audio_url = '/audio/%d.m4a' % video_id
	subject = video_info['title']
	description = video_info['description']
	date = parser.string_to_datetime(video_info['date'])
	date_rfc822 = parser.datetime_to_rfc822(date)
	url = postnauka_url_template % video_id
	youtube_url = youtube_url_template % video_info['youtube']
	audio_info = youtube.get_audio_full_info(youtube_url)

	author_info = video_info['authors'][0]
	author_id_url = author_info['author_link']
	author_id = author_id_url.split('/')[2]
	author_name = author_info['author_name']
	author_desc = author_info['author_description']

	author = db.get_or_update_author(author_id, author_name, author_desc)
	
	themes = parser.resolve_tags(video_info['tagscloud'])
	if  video_info['tags']:
		theme_id = video_info['tags']['eng']
		theme_name = video_info['tags']['rus']
		themes[theme_id] = theme_name

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
			audio_duration_hms = parser.duration_to_hms(audio_info['duration']), \
			audio_filesize = audio_info['filesize'], \
			youtube_thumbnail = audio_info['thumbnail'], \
			themes = themes
			)
	return result


def fetch_new_items():
	feed = parser.fetch_last_posts()
	for item in feed:
		if item['type'] == 'video':
			print item['id']
			fetch_video(int(item['id']))

	
if __name__ == '__main__':
	fetch_new_items()
