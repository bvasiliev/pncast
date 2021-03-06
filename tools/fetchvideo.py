#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pncast.youtube as youtube
import pncast.db as db
import pncast.parser as parser

def fetch_video(video_id):
    """ Fetch video info from api by id and save to DB """
    video_info = parser.fetch_video_info(video_id)
    if not video_info:
        return None

    audio_url = '/audio/%d.m4a' % video_id
    subject = video_info['title']
    description = video_info['description'].strip()
    date = parser.string_to_datetime(video_info['date'])
    date_rfc822 = parser.datetime_to_rfc822(date)
    url = parser.POSTNAUKA_URL_TEMPLATE % video_id
    youtube_id = video_info.get('youtube') or parser.find_youtube_id_on_page(url)
    youtube_url = parser.YOUTUBE_URL_TEMPLATE % youtube_id
    audio_info = youtube.get_audio_full_info(youtube_url)
    audio_duration = audio_info['duration']
    audio_duration_hms = parser.duration_to_hms(audio_duration)
    audio_filesize = audio_info['filesize'] or get_audio_size_directly(youtube_url)
    youtube_thumbnail = parser.YOUTUBE_THUMBNAIL_URL_TEMPLATE % audio_info['display_id']

    author_info = video_info['authors'][0]
    author_id = author_info['author_link'].split('/')[2]
    author_name = author_info['author_name']
    author_desc = author_info['author_description'].strip()

    author = db.get_or_update_author(author_id, author_name, author_desc)

    themes = parser.resolve_tags(video_info['tagscloud'])

    if  video_info['tags']:
        theme_id = video_info['tags']['eng']
        theme_name = video_info['tags']['rus']
        themes[theme_id] = theme_name

    video, result = db.video.get_or_create(id=video_id, \
        author=author.id, \
        subject=subject, \
        description=description, \
        date=date, \
        date_rfc822=date_rfc822, \
        url=url, \
        youtube_url=youtube_url, \
        audio_url=audio_url, \
        audio_duration=audio_duration, \
        audio_duration_hms=audio_duration_hms, \
        audio_filesize=audio_filesize, \
        youtube_thumbnail=youtube_thumbnail, \
        themes=themes)
    return result


def get_audio_size_directly(url):
    """ Trick for changed youtube API, must be removed """
    youtube_audio_url = youtube.get_audio_url(url)
    response = parser.requests.head(youtube_audio_url, allow_redirects=True)
    return int(response.headers['content-length'])


def fetch_new_items():
    """ Fetch new items from site """
    feed = parser.fetch_last_posts()
    existing_videos = (db.video.select(db.fn.array_agg(db.video.id))
                       .order_by()
                       .scalar()
                      )
    for item in feed:
        if item['type'] == 'video':
            item_id = int(item['id'])
            if item_id not in existing_videos:
                fetch_video(item_id)


if __name__ == '__main__':
    fetch_new_items()
