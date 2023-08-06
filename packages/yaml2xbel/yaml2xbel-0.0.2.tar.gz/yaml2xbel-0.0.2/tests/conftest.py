from os.path import abspath, dirname, join

from pytest import fixture

RES_DIR = abspath(join(dirname(__file__), 'res'))


@fixture
def basic_yml():
    """Provide a basic bookmark in YAML format."""
    return join(RES_DIR, 'basic.yml')


@fixture
def basic_xbel():
    """Provide a basic bookmark in XBEL format."""
    return join(RES_DIR, 'basic.xbel')
