#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pncast import helper, youtube, logo, db, podcast
from flask import Flask, redirect, render_template, make_response, abort
from flask_cache import Cache
from flask_compress import Compress

application	= Flask(__name__)
cache 		= Cache(application, config={'CACHE_TYPE': 'simple'})
site_root 	= 'http://pncast.ru'
cache_ttl 	= 3600
youtube_ttl	= 21420
feed_last_items = 100

Compress(application)

application.jinja_env.globals.update(
        site_root = site_root)

#application.logger.addHandler(logger.handler)

application.url_map.converters['video_id'] = helper.video_converter
application.url_map.converters['author_id'] = helper.author_converter
application.url_map.converters['theme_id'] = helper.theme_converter
application.url_map.converters['author_name'] = helper.author_name_converter
application.url_map.converters['theme_name'] = helper.theme_name_converter


@application.errorhandler(500)
@application.errorhandler(Exception)
def internal_server_error(error):
	""" Handle & log application errors """
	#application.logger.error('Server Error: %s', (error))
	return 'Something is wrong, we are working on it: %s' % error, 500


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
	return render_template('content.html', **locals())


@application.route('/audio/<video_id:video>.m4a')
@cache.cached(timeout=youtube_ttl)
def audio(video):
	""" Redirects to youtube audio by postnauka video id  """
	audio_url = youtube.get_audio_url(video.youtube_url)
	return redirect(audio_url, 303)


@application.route('/theme/<theme_id:theme>/rss.xml')
@cache.cached(timeout=cache_ttl)
def theme(theme):
	""" Theme feed """
	feed_theme = podcast.feed(theme_id=theme.id, title=theme.name)
	return make_response_rss(feed_theme)
	

@application.route('/author/<author_id:author>/rss.xml')
@cache.cached(timeout=cache_ttl)
def author(author):
	""" Author feed """
	feed_author = podcast.feed(author_id=author.id, title=author.name)
	return make_response_rss(feed_author)


@application.route('/last/rss.xml')
@cache.cached(timeout=cache_ttl)
def last():
	""" Last items feed """
	feed_last = podcast.feed(title='Последние лекции', limit=feed_last_items)
	return make_response_rss(feed_last)


@application.route('/logo/<string:table>/<string:item_id>.png') #FIXME
@cache.cached(timeout=cache_ttl)
def feed_logo(table, item_id):
	""" Creates static feed img & redirects to """
	logo_url, created = logo.get_image_url(table, item_id)
	if logo_url: 
		return redirect(logo_url, 301)
	else:
		abort(404)


@application.route('/theme/<theme_name:theme>')
@cache.cached(timeout=cache_ttl)
def theme_redirect(theme):
	""" Redirects to theme feed by name, for front xls simplifying """
	theme_feed_url = '/theme/%s/rss.xml' % theme.id
	return redirect(theme_feed_url, 301)


@application.route('/author/<author_name:author>')
@cache.cached(timeout=cache_ttl)
def author_redirect(author):
	""" Redirects to author feed by name, for front xls simplifying """
	author_feed_url = '/author/%s/rss.xml' % author.id
	return redirect(author_feed_url, 301)


if __name__ == '__main__':
	application.run()
