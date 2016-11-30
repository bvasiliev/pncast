#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pncast import youtube, logo, db, podcast, logger #local
from flask import Flask, redirect, render_template, make_response, abort
from flask.ext.cache import Cache
from flask.ext.compress import Compress

app 		= Flask(__name__)
cache 		= Cache(app, config={'CACHE_TYPE': 'simple'})
site_root 	= 'http://pncast.ru'
cache_ttl 	= 3600
youtube_ttl	= 21420
feed_last_items = 100

Compress(app)

app.jinja_env.globals.update(
        site_root = site_root)

app.logger.addHandler(logger.handler)


@app.errorhandler(500)
def internal_server_error(error):
	app.logger.error('Server Error: %s', (error))
	return 'Something is wrong, we are working on it', 500


@app.errorhandler(Exception)
def unhandled_exception(e):
	app.logger.error('Unhandled Exception: %s', (e))
	return 'Something is wrong, we are working on it', 500


def make_response_rss(feed):
	result = make_response(render_template('items.xml', feed=feed))
	result.mimetype = 'text/xml'
	return result


def get_audio_url(video_id):
	try:
		video = db.video.get(db.video.id == video_id)
		result = youtube.get_audio_url(video.youtube_url)
	except db.video.DoesNotExist:
		result = youtube.get_audio_url(youtube.rickroll)
	return result


@app.route('/')
@cache.cached(timeout=cache_ttl)
def index():
	authors = db.author.select().order_by(db.author.count.desc())
	themes = db.theme.select().order_by(db.theme.count.desc())
	return render_template('content.html', **locals())


@app.route('/audio/<int:audio_id>.m4a')
@cache.cached(timeout=youtube_ttl) 
def audio(audio_id):
	audio_url = get_audio_url(audio_id)
	return redirect(audio_url, 303)


@app.route('/theme/<string:theme_id>/rss.xml')
@cache.cached(timeout=cache_ttl)
def theme(theme_id):
	theme_name = db.theme.select(db.theme.name).where(db.theme.id == theme_id).scalar()
	if not theme_name:
		abort(404)
	feed_theme = podcast.feed(theme_id=theme_id, title=theme_name)
	return make_response_rss(feed_theme)
	

@app.route('/author/<string:author_id>/rss.xml')
@cache.cached(timeout=cache_ttl)
def author(author_id):
	author_name = db.author.select(db.author.name).where(db.author.id == author_id).scalar()
	if not author_name:
		abort(404)
	feed_author = podcast.feed(author_id=author_id, title=author_name)
	return make_response_rss(feed_author)


@app.route('/last/rss.xml')
@cache.cached(timeout=cache_ttl)
def last():
	feed_last = podcast.feed(title='Последние лекции', limit=feed_last_items)
	return make_response_rss(feed_last)


@app.route('/logo/<string:table>/<string:r_id>.png')
@cache.cached(timeout=cache_ttl)
def feed_logo(table, r_id):
	logo_url, created = logo.get_image_url(table, r_id)
	if logo_url: 
		return redirect(logo_url, 301)
	else:
		abort(404)


@app.route('/theme/<string:theme_name>')
@cache.cached(timeout=cache_ttl)
def theme_redirect(theme_name):
	theme_name = theme_name.strip()
	theme_id = db.theme.select(db.theme.id).where(db.theme.name == unicode(theme_name)).scalar()
	if not theme_id:
		abort(404)
	theme_feed_url = '/theme/%s/rss.xml' % theme_id
	return redirect(theme_feed_url, 301)


@app.route('/author/<string:author_name>')
@cache.cached(timeout=cache_ttl)
def author_redirect(author_name):
	author_name = author_name.strip()
	author_id = db.author.select(db.author.id).where(db.author.name == unicode(author_name)).scalar()
	if not author_id:
		abort(404)
	author_feed_url = '/author/%s/rss.xml' % author_id
	return redirect(author_feed_url, 301)


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
