#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import db


class feed:
	def __init__(self, theme_id=None, author_id=None, title=None, limit=None):
		if theme_id:
			self.items = db.select_video_by_theme(theme_id)
			self.logo_url = '/logo/theme/%s.png' % theme_id
			self.title = capitalize_first(title)
		elif author_id:
			self.items = db.select_video(db.video.author == author_id)
			self.logo_url = '/logo/author/%s.png' % author_id
			self.description = capitalize_first(self.items[0].author.description)
			self.summary = self.description
			self.title = title
		else:
			self.items = db.select_video().limit(limit)
			self.logo_url = '/static/logo.png'
			self.title = title
		self.date = self.items[0].date_rfc822

def capitalize_first(string):
	return string[:1].upper() + string[1:]

if __name__ == '__main__':
	pass

