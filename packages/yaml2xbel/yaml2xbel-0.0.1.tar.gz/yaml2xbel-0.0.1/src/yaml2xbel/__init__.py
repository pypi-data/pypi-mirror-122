# Initialization code
# Copyright (C) 2021 - Ngô Ngọc Đức Huy
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os.path import abspath, dirname, join

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__version__ = '0.0.1'
__doc__ = 'XBEL generator from YAML'

XBEL_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="bookmarks.xsl"?>
<!DOCTYPE xbel PUBLIC "+//IDN python.org//DTD XML Bookmark Exchange Language 1.0//EN//XML"
		       "http://www.python.org/topics/xml/dtds/xbel-1.0.dtd">

"""


def convert(filename) -> str:
    """Convert YAML to XBEL format."""
    with open (filename) as source:
        data = load(source, Loader=Loader)
        output = XBEL_HEADER
        output += '<xbel>\n'
        for folder in data:
            output += '\t<folder>\n'
            output += f'\t\t<title>{folder}</title>\n'
            for item in data[folder]:
                output += f'\t\t<bookmark href="{data[folder][item]}">\n'
                output += f'\t\t\t<title>{item}</title>\n'
                output += f'\t\t</bookmark>\n'
            output += '\t</folder>\n'
        output += '</xbel>\n'
        return output
    return 'Bad input'
