#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import db
import textwrap
import re

workdir = os.getcwd()

font_file 	= '%s/templates/DejaVuSans-Bold.ttf' % workdir
logo_template 	= '%s/templates/feed-temp.png' % workdir
W 		= 1400
H 		= 1400
max_font_size 	= 180
normal_text_width = 10


def get_text_width(text):
	split_text = re.split('(\s|\-)', text) #text.split()
	text_width = len(max(split_text, key=len))
	return text_width


def create_image(message):
	backgroung = Image.open(logo_template)
	draw = ImageDraw.Draw(backgroung)
	result = BytesIO()

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
	backgroung.save(result, 'PNG')
	result.seek(0)
	return result


if __name__ == '__main__':
	pass
