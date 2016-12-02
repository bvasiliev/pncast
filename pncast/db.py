#! /usr/bin/python

from __future__ import unicode_literals
from peewee import *
from playhouse.postgres_ext import *
from os import environ as env

postgres = PostgresqlExtDatabase(env['POSTGRESQL_DATABASE'], 
	user = env['POSTGRESQL_USER'],
	password = env['POSTGRESQL_PASSWORD'],
	host = env['POSTGRESQL_SERVICE_HOST'] 
	)


class psql(Model):
	class Meta:
		database = postgres
	
	
class author(psql):
	id 		= CharField(primary_key=True)
	name 		= TextField(null=True)
	description 	= TextField(null=True)
	count 		= IntegerField(default=1)


class theme(psql):
	id		= CharField(primary_key=True)
	name		= TextField()
	count		= IntegerField(default=1)


class video(psql): 
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

	
class theme_to_video(psql):
	theme = ForeignKeyField(theme)
	video = ForeignKeyField(video)
	class Meta:
		primary_key = CompositeKey('theme', 'video')


def select_video(cause=None):
	videos = (video.select(video, themes_names_subquery)
		.where(cause)
		.order_by(video.date.desc(), video.id.desc())
		)
	return videos


def select_video_by_theme(theme_id):
	theme_to_videos = (theme_to_video.select(video, themes_names_subquery)
		.join(video)
		.join(author)
		.where(theme_to_video.theme == theme_id)
		.order_by(video.date.desc(), video.id.desc())
		)
	videos = []
        for item in theme_to_videos:
        	item.video.themes = item.themes #SelectQuery objects mapping, not real data
		videos.append(item.video)
	return videos

def get_or_update_author(author_id, name, description):
	try:
		result, created = author.get_or_create(id = author_id, name = name, description = description)
	except IntegrityError:
		result = author.get(author.id == author_id)
		result.name = name
		result.description = description
		result.save()
	return result
	
	
themes_names_subquery = (fn.array(theme_to_video.select(theme.name)
	.join(theme)
	.where(video.id == theme_to_video.video)
	.order_by(theme.count.desc())
		)
	.alias('themes')
	)

	
if __name__ == '__main__':
	pass
