#! /usr/bin/python
# -*- coding: utf-8 -*-

""" pncast.ru """

from __future__ import unicode_literals
from flask import Flask, redirect, render_template, make_response, send_file, \
                  request, send_from_directory
from flask_caching import Cache
from flask_compress import Compress
from pncast import helper, youtube, logo, db, podcast
from re import sub

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
Compress(app)

CACHE_TTL = 3600
YOUTUBE_TTL = 21420
FEED_LIMIT = 100

app.url_map.converters['video_id'] = helper.VideoConverter
app.url_map.converters['author_id'] = helper.AuthorConverter
app.url_map.converters['theme_id'] = helper.ThemeConverter


def make_response_rss(feed):
    """ Render podcast.Feed """
    result = make_response(render_template('items.xml', feed=feed))
    result.mimetype = 'text/xml'
    return result


@app.route('/')
@cache.cached(timeout=CACHE_TTL)
def index():
    """ Main page """
    authors = db.author.select().order_by(db.author.count.desc())
    themes = db.theme.select().order_by(db.theme.count.desc())
    page = render_template('content.html', **locals())
    return make_response(page)


@app.route('/audio/<video_id:request_video>.m4a')
@cache.cached(timeout=YOUTUBE_TTL)
def audio(request_video):
    """ Redirects to youtube audio by video id with server ip masquerade """
    client_addr = '&ip=%s' % request.remote_addr
    server_audio_url = youtube.get_audio_url(request_video.youtube_url)
    audio_url = sub(helper.IP_PATTERN, client_addr, server_audio_url)
    return redirect(audio_url, 303)


@app.route('/theme/<theme_id:request_theme>/rss.xml')
@cache.cached(timeout=CACHE_TTL)
def theme(request_theme):
    """ theme feed """
    items = db.video.select().where(db.video.themes.contains(request_theme.id))
    logo_url = '/logo/theme/%s.png' % request_theme.id
    theme_feed = podcast.Feed(items, title=request_theme.name, logo_url=logo_url)
    return make_response_rss(theme_feed)


@app.route('/author/<author_id:request_author>/rss.xml')
@cache.cached(timeout=CACHE_TTL)
def author(request_author):
    """ author feed """
    items = db.video.select().where(db.video.author == request_author.id)
    logo_url = '/logo/author/%s.png' % request_author.id
    author_feed = podcast.Feed(items,
                               title=request_author.name,
                               description=request_author.description,
                               logo_url=logo_url)
    return make_response_rss(author_feed)


@app.route('/last/rss.xml')
@cache.cached(timeout=CACHE_TTL)
def last():
    """ Last items feed """
    items = db.video.select().limit(FEED_LIMIT)
    last_feed = podcast.Feed(items, title='Последние лекции')
    return make_response_rss(last_feed)


@app.route('/logo/author/<author_id:item>.png')
@app.route('/logo/theme/<theme_id:item>.png')
@cache.cached(timeout=CACHE_TTL)
def feed_logo(item):
    """ Feed logo """
    item_logo = logo.create_image(item.name)
    return send_file(item_logo, mimetype='image/png')


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    """ Static files from root """
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run()
