import pytest


def _create_file(tmpdir, body, extension):
    _file = tmpdir.join('attach.{extension}'.format(extension=extension))
    _file.write(body)
    return _file.strpath


@pytest.fixture
def xml_body():
    return """<?xml version="1.0" encoding="UTF-8"?>
<bla-bla-tag>
    <inside-bla-bla>BLA bla</inside-bla-bla>
</bla-bla-tag>
"""


@pytest.fixture
def svg_body():
    return """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">
<path d="M50,3l12,36h38l-30,22l11,36l-31-21l-31,21l11-36l-30-22h38z" fill="#FF0" stroke="#FC0" stroke-width="2"/>
</svg>
"""


@pytest.fixture
def xml_file(tmpdir, xml_body):
    return _create_file(tmpdir, xml_body, 'xml')


@pytest.fixture
def svg_file(tmpdir, svg_body):
    return _create_file(tmpdir, svg_body, 'svg')
