#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import db


class feed:
	def __init__(self, items, title, description='', logo_url='/static/logo.png'):
		self.items = items
		self.date = self.items[0].date_rfc822
		self.title = capitalize_first(title)
		self.description = capitalize_first(description)
		self.logo_url = logo_url


def capitalize_first(string):
	return string[:1].upper() + string[1:]

if __name__ == '__main__':
	pass

