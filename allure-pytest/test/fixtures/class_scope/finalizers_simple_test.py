
import pytest


@pytest.fixture(scope='class')
def fixture_with_finalizer_a(request):
    def finalizer_fixture_a():
        pass
    request.addfinalizer(finalizer_fixture_a)


class TestClass(object):
    def test_a(self, fixture_with_finalizer_a):
        pass

    def test_b(self, fixture_with_finalizer_a):
        pass
