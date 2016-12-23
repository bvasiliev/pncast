#! /usr/bin/python

""" database connection module """

from __future__ import unicode_literals
from os import environ as env
import urlparse
from playhouse.postgres_ext import PostgresqlExtDatabase, HStoreField
from peewee import Model, IntegerField, TextField, CharField, DateTimeField, \
                   ForeignKeyField, coerce_to_unicode, fn

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(env['DATABASE_URL'])


class Psql(Model):
    """ Postgresql connection options """
    class Meta(object):
        database = PostgresqlExtDatabase(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)


class HStoreFieldUnicode(HStoreField):
    """ Adapts peewee HStoreField to store non-ascii values """
    def coerce(self, field):
        if isinstance(field, dict):
            for key, value in field.iteritems():
                field[key] = coerce_to_unicode(value)
        return field


class author(Psql):
    """ authors - real table """
    id = CharField(primary_key=True)
    name = TextField(null=True)
    description = TextField(null=True)
    count = IntegerField(default=1)


class theme(Psql):
    """ themes - materialized view from video.themes """
    id = CharField(primary_key=True)
    name = TextField()
    count = IntegerField(default=1)


class video(Psql):
    """ videos - real table """
    author = ForeignKeyField(author, null=True)
    subject = TextField()
    description = TextField()
    date = DateTimeField()
    date_rfc822 = CharField()
    url = TextField()
    youtube_url = TextField()
    audio_url = TextField(null=True)
    audio_duration = IntegerField(null=True)
    audio_duration_hms = CharField(null=True)
    audio_filesize = IntegerField(null=True)
    youtube_thumbnail = TextField(null=True)
    themes = HStoreFieldUnicode(null=True)
    class Meta(object):
        order_by = ['-date', '-id']


def get_or_update_author(author_id, name, description):
    """ Get or create author record, update if changed """
    try:
        result, created = author.get_or_create(id=author_id,
                                               name=name,
                                               description=description)
    except IntegrityError:
        result = author.get(author.id == author_id)
        result.name = name
        result.description = description
        result.save()
    return result


if __name__ == '__main__':
    pass
