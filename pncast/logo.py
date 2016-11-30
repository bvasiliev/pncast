#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PIL import Image, ImageDraw, ImageFont
import db #local
import textwrap
import re
import os.path

logo_folder 	= '/var/www/pn/static/logo/'
url_path 	= '/static/logo/'
font_file 	= '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf'
logo_template 	= '/var/www/pn/templates/feed-temp.png'
W 		= 1400
H 		= 1400
max_font_size 	= 180
normal_text_width = 10


def get_text_width(text):
	split_text = re.split('(\s|\-)', text) #text.split()
	text_width = len(max(split_text, key=len))
	return text_width


def create_image(message, filepath):
	backgroung = Image.open(logo_template)
	draw = ImageDraw.Draw(backgroung)
	
	text_width = get_text_width(message)
	if text_width > normal_text_width:
		font_size = max_font_size * normal_text_width / text_width
	else:
		font_size = max_font_size
		text_width = normal_text_width
	font = ImageFont.truetype(font_file, font_size)

	message_rows = textwrap.wrap(message, width=text_width)
	H_current = H / 4 - (font_size * len(message_rows) / 2) 
	for row in message_rows:
		w, h = draw.textsize(row, font=font)
		draw.text(((W - w) / 2, H_current ), row, font=font)
		H_current = H_current + font_size
	backgroung.save(filepath)


def get_image_url(table, r_id):
	filename = r_id + '.png'
	filepath = logo_folder + filename
	
	if os.path.isfile(filepath):
		return url_path + filename, False
	
	if table == 'author':
		name = db.author.select(db.author.name).where(db.author.id == r_id).scalar()
	elif table == 'theme':
		name = db.theme.select(db.theme.name).where(db.theme.id == r_id).scalar()
	else:
		return None, False

	if name:
		create_image(name, filepath)
		return  url_path + filename, True
	else:
		return None, False


if __name__ == '__main__':
	pass
