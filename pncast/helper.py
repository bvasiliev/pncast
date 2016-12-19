#! /usr/bin/python
# -*- coding: utf-8 -*-

""" Flask url validators, jinja2 modifiers """

from __future__ import unicode_literals
from werkzeug.routing import BaseConverter, ValidationError
import pncast.db as db


class DBConverter(BaseConverter):
    """ Base url to DB converner """
    table = db.video
    def to_python(self, value):
        try:
            return self.table.get(self.table.id == value)
        except self.table.DoesNotExist:
            raise ValidationError()
    def to_url(self, value):
        return value.id


class VideoConverter(DBConverter):
    """ Extract video object from DB """
    regex = r'\d+'


class AuthorConverter(DBConverter):
    """ Extract author object from DB """
    regex = r'[a-zA-Z0-9-_]+'
    table = db.author


class ThemeConverter(DBConverter):
    """ Extract theme object from DB """
    regex = r'[a-zA-Z0-9-_]+'
    table = db.theme
