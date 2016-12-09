#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from werkzeug.routing import BaseConverter, ValidationError
import db


class db_converter(BaseConverter):
	""" Base url to DB converner """
	table = db.video
	def to_python(self, value):
		try:
			return self.table.get(self.table.id == value)
		except self.table.DoesNotExist:
			raise ValidationError()
	def to_url(self, value):
		return value.id


class video_converter(db_converter):
	""" Extract video object from DB """
	regex = r'\d+'


class author_converter(db_converter):
	""" Extract author object from DB """
	regex = r'[a-zA-Z0-9-_]+'
	table = db.author


class theme_converter(db_converter):
	""" Extract theme object from DB """
	regex = r'[a-zA-Z0-9-_]+'
	table = db.theme


def themes_flatten(themes_dict):
	return ', '.join(val for (key, val) in themes_dict.iteritems())
