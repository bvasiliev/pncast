#! /usr/bin/python

from __future__ import unicode_literals
from peewee import *
from playhouse.postgres_ext import *
from os import environ as env
import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(env['DATABASE_URL'])

postgres = PostgresqlExtDatabase(
		database = url.path[1:],
		user = url.username,
		password = url.password,
		host = url.hostname,
		port = url.port
		)


class psql(Model):
	class Meta:
		database = postgres
	
	
class author(psql):
	""" Authors - real table """
	id 		= CharField(primary_key=True)
	name 		= TextField(null=True)
	description 	= TextField(null=True)
	count 		= IntegerField(default=1)


class theme(psql):
	""" Themes - materialized view from video.themes """
	id		= CharField(primary_key=True)
	name		= TextField()
	count		= IntegerField(default=1)


class video(psql):
	""" Videos - real table """
	author		= ForeignKeyField(author, null=True)
	subject		= TextField()
	description 	= TextField()
	date 		= DateTimeField()
	date_rfc822 	= CharField()
	url 		= TextField()
	youtube_url 	= TextField()
	audio_url 	= TextField(null=True)
	audio_duration 	= IntegerField(null=True)
	audio_duration_hms = CharField(null=True)
	audio_filesize 	= IntegerField(null=True)
	youtube_thumbnail = TextField(null=True)
	themes 		= HStoreField(null=True)
	class Meta:
		order_by = ['-date', '-id']


class theme_to_video(psql):
	""" Legacy many2many ralations for DB without limits """
	theme = ForeignKeyField(theme)
	video = ForeignKeyField(video)
	class Meta:
		primary_key = CompositeKey('theme', 'video')


def get_or_update_author(author_id, name, description):
	try:
		result, created = author.get_or_create(id = author_id, name = name, description = description)
	except IntegrityError:
		result = author.get(author.id == author_id)
		result.name = name
		result.description = description
		result.save()
	return result
	
	
if __name__ == '__main__':
	pass
