#! /usr/bin/python
# -*- coding: utf-8 -*-

""" Feed logo generator """

from __future__ import unicode_literals
from io import BytesIO
import os
import textwrap
import re
from PIL import Image, ImageDraw, ImageFont

WORKDIR = os.getcwd()

FONT_FILE = '%s/templates/DejaVuSans-Bold.ttf' % WORKDIR
LOGO_TEMPLATE = '%s/templates/feed-temp.png' % WORKDIR
W = 1400
H = 1400
MAX_FONT_SIZE = 180
NORMAL_TEXT_WIDTH = 10


def get_text_width(text):
    """ Return len of longest world in text """
    split_text = re.split(r'(\s|\-)', text)
    return len(max(split_text, key=len))


def create_image(message):
    """ Return png logo BytesIO with message text """
    backgroung = Image.open(LOGO_TEMPLATE)
    draw = ImageDraw.Draw(backgroung)
    result = BytesIO()

    text_width = get_text_width(message)
    if text_width > NORMAL_TEXT_WIDTH:
        font_size = MAX_FONT_SIZE * NORMAL_TEXT_WIDTH / text_width
    else:
        font_size = MAX_FONT_SIZE
        text_width = NORMAL_TEXT_WIDTH
    font = ImageFont.truetype(FONT_FILE, font_size)

    message_rows = textwrap.wrap(message, width=text_width)
    h_current = H / 4 - (font_size * len(message_rows) / 2)
    for row in message_rows:
        width, height = draw.textsize(row, font=font)
        draw.text(((W - width) / 2, h_current), row, font=font)
        h_current = h_current + font_size
    backgroung.save(result, 'PNG')
    result.seek(0)
    return result


if __name__ == '__main__':
    pass
