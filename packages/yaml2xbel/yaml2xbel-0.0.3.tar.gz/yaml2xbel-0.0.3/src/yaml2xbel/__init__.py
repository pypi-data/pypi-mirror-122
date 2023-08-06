# Initialization code
# Copyright (C) 2021 - Ngô Ngọc Đức Huy
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

__version__ = '0.0.3'
__doc__ = 'XBEL generator from YAML'

XBEL_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n'
XBEL_HEADER += '<?xml-stylesheet type="text/xsl" href="bookmarks.xsl"?>\n'
XBEL_HEADER += '<!DOCTYPE xbel PUBLIC'
XBEL_HEADER += ' "+//IDN python.org//DTD XML Bookmark Exchange Language'
XBEL_HEADER += ' 1.0//EN//XML"\n\t\t       '
XBEL_HEADER += '"http://www.python.org/topics/xml/dtds/xbel-1.0.dtd">\n\n'


def convert(filename) -> str:
    """Convert YAML to XBEL format."""
    with open(filename) as source:
        data = load(source, Loader=Loader)
        output = XBEL_HEADER
        output += '<xbel>\n'
        for folder in data:
            output += '\t<folder>\n'
            output += f'\t\t<title>{folder}</title>\n'
            for item in data[folder]:
                output += f'\t\t<bookmark href="{data[folder][item]}">\n'
                output += f'\t\t\t<title>{item}</title>\n'
                output += '\t\t</bookmark>\n'
            output += '\t</folder>\n'
        output += '</xbel>\n'
        return output
    return 'Bad input'
