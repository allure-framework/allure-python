Select test by label
-----------------------------

By using ``--allure-label`` commandline option with a ``lablel_name=label1,label2`` format, only tests with
corresponding labels will be run.


For example, if you want to run tests with label 'Application' equals to 'desktop' or 'mobile' only,
run pytest with ``--allure-label Application=desktop,mobile`` option.

To filter tests with several different labels multiple ``--allure-label`` options can be specified:

``--allure-label Application=desktop,mobile --allure-label layer=api``

    >>> import allure

    >>> @allure.label("Application", "desktop")
    ... def test_custom_label_one():
    ...     pass

    >>> @allure.label("Application", "mobile")
    ... def test_custom_label_another():
    ...     pass

    >>> @allure.label("Application", "mobile", "desktop")
    ... def test_custom_label_both():
    ...     pass

    >>> @allure.label("layer", "api")
    ... def test_layer_label():
    ...     pass

    >>> def test_no_labels():
    ...     pass
