# Test function to convert from YAML to XBEL
# Copyright (C) 2021 Ngô Ngọc Đức Huy
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from yaml2xbel import convert


def test_basic(basic_yml, basic_xbel) -> None:
    """Test convert function on basic.yml file."""
    with open(basic_xbel) as f:
        assert convert(basic_yml) == ''.join(f.read())
