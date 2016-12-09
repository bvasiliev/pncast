#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from werkzeug.routing import BaseConverter, ValidationError
import db


class db_converter(BaseConverter):
	""" Base url to DB converner """
	regex = r'[a-zA-Z0-9-_]+'
	def to_url(self, value):
		return value.id


class video_converter(db_converter):
	""" Extract video object from DB """
	regex = r'\d+'
	def to_python(self, value):
		try:
			return db.video.get(db.video.id == value)
		except db.video.DoesNotExist:
			raise ValidationError()


class author_converter(db_converter):
	""" Extract author object from DB """
	def to_python(self, value):
		try:
			return db.author.get(db.author.id == value)
		except db.author.DoesNotExist:
			raise ValidationError()


class theme_converter(db_converter):
	""" Extract theme object from DB """
	def to_python(self, value):
		try:
			return db.theme.get(db.theme.id == value)
		except db.theme.DoesNotExist:
			raise ValidationError()

