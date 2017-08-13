from nose.tools import with_setup


def setup_f():
    print('setting test in module 2')


def teardown_f():
    print('tearing down test in module 2')


class TestClass2():

    @classmethod
    def setup_class(cls):
        print("setup class2")

    @with_setup(setup_f)
    def test_dummy2(arg):
        print("test dummy 2")

    def test_4(arg):
        print('test 4')


@with_setup(setup_f, teardown_f)
def test_3():
    print('in test 3')


def tearDown():
    print("tearing down in module 2")