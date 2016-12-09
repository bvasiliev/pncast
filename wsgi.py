#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pncast import helper, youtube, logo, db, podcast
from flask import Flask, redirect, render_template, make_response, send_file
from flask_caching import Cache
from flask_compress import Compress
import sys

reload(sys) 
sys.setdefaultencoding('utf-8')

application	= Flask(__name__)
cache 		= Cache(application, config={'CACHE_TYPE': 'simple'})
site_root 	= 'http://pncast.ru'
cache_ttl 	= 3600
youtube_ttl	= 21420
feed_last_items = 100

Compress(application)

application.jinja_env.globals.update(site_root = site_root)
application.jinja_env.filters['themes_flatten'] = helper.themes_flatten

#application.logger.addHandler(logger.handler)

application.url_map.converters['video_id'] = helper.video_converter
application.url_map.converters['author_id'] = helper.author_converter
application.url_map.converters['theme_id'] = helper.theme_converter

'''
@application.errorhandler(500)
@application.errorhandler(Exception)
def internal_server_error(error):
	""" Handle & log application errors """
	#application.logger.error('Server Error: %s', (error))
	return 'Something is wrong, we are working on it: %s' % error, 500
'''


def make_response_rss(feed):
	""" Render podcast feed """
	result = make_response(render_template('items.xml', feed=feed))
	result.mimetype = 'text/xml'
	return result


@application.route('/')
@cache.cached(timeout=cache_ttl)
def index():
	""" Main page """
	authors = db.author.select().order_by(db.author.count.desc())
	themes = db.theme.select().order_by(db.theme.count.desc())
	page = render_template('content.html', **locals())
	return make_response(page)


@application.route('/audio/<video_id:video>.m4a')
@cache.cached(timeout=youtube_ttl)
def audio(video):
	""" Redirects to youtube audio by video id  """
	audio_url = youtube.get_audio_url(video.youtube_url)
	return redirect(audio_url, 303)


@application.route('/theme/<theme_id:theme>/rss.xml')
@cache.cached(timeout=cache_ttl)
def theme(theme):
	""" Theme feed """
	items = db.video.select().where(db.video.themes.contains(theme.id))
	logo_url = '/logo/theme/%s.png' % theme.id
	feed_theme = podcast.feed(items, title=theme.name, logo_url=logo_url)
	return make_response_rss(feed_theme)
	

@application.route('/author/<author_id:author>/rss.xml')
@cache.cached(timeout=cache_ttl)
def author(author):
	""" Author feed """
	items = db.video.select().where(db.video.author == author.id)
	logo_url = '/logo/author/%s.png' % author.id
	feed_author = podcast.feed(items, title=author.name, description=author.description, logo_url=logo_url)	
	return make_response_rss(feed_author)


@application.route('/last/rss.xml')
@cache.cached(timeout=cache_ttl)
def last():
	""" Last items feed """
	items = db.video.select().limit(feed_last_items)
	feed_last = podcast.feed(items, title='Последние лекции')
	return make_response_rss(feed_last)


@application.route('/logo/author/<author_id:item>.png')
@application.route('/logo/theme/<theme_id:item>.png')
@cache.cached(timeout=cache_ttl)
def feed_logo(item):
	""" Feed logo """
	feed_logo = logo.create_image(item.name)
	return send_file(feed_logo, mimetype='image/png')


if __name__ == '__main__':
	application.run()
