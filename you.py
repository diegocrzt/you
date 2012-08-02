#!/usr/bin/env python
from __future__ import print_function

import argparse
import collections
import datetime
import functools
import itertools
import logging
import operator
import pprint
import re

from player import Player
from search import search, extract
from window import Window

# Logging
LOG_FILENAME = 'you.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

log = logging.getLogger(__name__)


class You(object):
    def __init__(self, args):
        self.window = window = Window()
        self.player = None
        window.set_input_callback(self.on_input)
        window.set_select_callback(self.on_select)
        window.run()

    def on_input(self, text):
        results = search(text)
        self.window.set_results(results)

    def on_select(self, video):
        self.extract(video)

    def play(self, video, uri):
        if not self.player:
            self.player = Player(window=self.window)
        self.player.play(video, uri)

    def extract(self, video):
        if not self.player:
            self.player = Player(window=self.window)

        def callback(info):
            log.info(info)
            if 'url' not in info:
                # TODO: fuck
                return
            self.play(video, info['url'])

        extract(video.url, callback=callback)



# def print_info():
#     """Print information about the media"""
#     try:
#         print_version()
#         media = player.get_media()
#         print('State: %s' % player.get_state())
#         print('Media: %s' % media.get_mrl())
#         print('Track: %s/%s' % (player.video_get_track(), player.video_get_track_count()))
#         print('Current time: %s/%s' % (player.get_time(), media.get_duration()))
#         print('Position: %s' % player.get_position())
#         print('FPS: %s (%d ms)' % (player.get_fps(), mspf()))
#         print('Rate: %s' % player.get_rate())
#         print('Video size: %s' % str(player.video_get_size(0)))  # num=0
#         print('Scale: %s' % player.video_get_scale())
#         print('Aspect ratio: %s' % player.video_get_aspect_ratio())
#        #print('Window:' % player.get_hwnd()
#     except Exception:
#         print('Error: %s' % sys.exc_info()[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A videoless command-line YouTube player.')

    parser.add_argument('--config', nargs='?', dest='config', metavar='filename',
                        default='~/.you', help='you configuration.')
    parser.add_argument('--update', action='store_true',
                        help="Placeholder option -- not implemented")
    parser.add_argument('term', nargs='*',
                        help='The text to search for.')

    args = parser.parse_args()

    You(args)
