import allure


__all__ = ['attach', 'attach_file']


def _attachment_type(name):
    try:
        return allure.attachment_type[name]
    except KeyError:
        return name


def attach(data, name=None, attachment_type=None, extension=None):
    allure.attach(data, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)


def attach_file(source, name=None, attachment_type=None, extension=None):
    allure.attach.file(source, name=name, attachment_type=_attachment_type(attachment_type), extension=extension)
