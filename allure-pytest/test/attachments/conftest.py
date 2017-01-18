import pytest


XML = '''<?xml version="1.0" encoding="UTF-8"?>
<bla-bla-tag>
    <inside-bla-bla>BLA bla</inside-bla-bla>
</bla-bla-tag>
'''

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">
<path d="M50,3l12,36h38l-30,22l11,36l-31-21l-31,21l11-36l-30-22h38z" fill="#FF0" stroke="#FC0" stroke-width="2"/>
</svg>
'''


def create_file(tmpdir, body):
    _file = tmpdir.join('test.wtf')
    _file.write(body)
    return _file.strpath


@pytest.fixture
def xml(tmpdir):
    return create_file(tmpdir, XML)


@pytest.fixture
def svg(tmpdir):
    return create_file(tmpdir, SVG)
