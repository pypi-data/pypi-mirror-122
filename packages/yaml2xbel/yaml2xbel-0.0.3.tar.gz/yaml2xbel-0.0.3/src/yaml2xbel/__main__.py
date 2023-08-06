# Copyright (C) 2021 - Ngô Ngọc Đức Huy
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sys import argv

from yaml2xbel import convert

if __name__ == '__main__':
    with open('bookmarks.xbel', 'w') as output:
        output.write(convert(argv[1]))
