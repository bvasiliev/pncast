#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import db


class feed:
	def __init__(self, items, title, description=None, logo_url=None):
		self.items = items
		self.date = self.items[0].date_rfc822
		self.title = capitalize_first(title)
		self.description = capitalize_first(description) or ''
		self.logo_url = logo_url or '/static/logo.png'


def capitalize_first(string):
	return string[:1].upper() + string[1:]

if __name__ == '__main__':
	pass

