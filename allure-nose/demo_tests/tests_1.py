from nose.tools import with_setup


def setup_f():
    print('setting test in module 1')


class TestClass():

    @classmethod
    def setup_class(cls):
        print("setup class in module 1")

    @with_setup(setup_f)
    def test_dummy(hz):
        print("YO")
        # assert False

    def test_2(hz):
        print(hz)
        print('test 2')


def tearDown():
    print("tearing down in module 1")