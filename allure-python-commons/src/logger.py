import errno
import io
import os
import sys
import json
import uuid
import shutil
from six import text_type
from attr import asdict
from allure_commons import hookimpl

INDENT = 4


def delete_step_thrd(data):
    if isinstance(data, list):
        for field in data:
            field = delete_step_thrd(field)
    elif isinstance(data, dict):
        for field in data.keys():
            if field == 'thrd':
                data.pop('thrd')
                break
            field = delete_step_thrd(data[field])
    return data

class AllureFileLogger(object):

    def __init__(self, report_dir, clean=False):
        self._report_dir = report_dir

        try:
            os.makedirs(report_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            elif clean:
                for f in os.listdir(report_dir):
                    f = os.path.join(report_dir, f)
                    if os.path.isfile(f):
                        os.unlink(f)

    def _report_item(self, item):
        indent = INDENT if os.environ.get("ALLURE_INDENT_OUTPUT") else None
        filename = item.file_pattern.format(prefix=uuid.uuid4())
        data = asdict(item, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        data = delete_step_thrd(data)

        with io.open(os.path.join(self._report_dir, filename), 'w', encoding='utf8') as json_file:
            if sys.version_info.major < 3:
                json_file.write(
                    unicode(json.dumps(data, indent=indent, ensure_ascii=False, encoding='utf8')))  # noqa: F821
            else:
                json.dump(data, json_file, indent=indent, ensure_ascii=False)

    @hookimpl
    def report_result(self, result):
        self._report_item(result)

    @hookimpl
    def report_container(self, container):
        self._report_item(container)

    @hookimpl
    def report_attached_file(self, source, file_name):
        destination = os.path.join(self._report_dir, file_name)
        shutil.copy2(source, destination)

    @hookimpl
    def report_attached_data(self, body, file_name):
        destination = os.path.join(self._report_dir, file_name)
        with open(destination, 'wb') as attached_file:
            if isinstance(body, text_type):
                attached_file.write(body.encode('utf-8'))
            else:
                attached_file.write(body)


class AllureMemoryLogger(object):

    def __init__(self):
        self.test_cases = []
        self.test_containers = []
        self.attachments = {}

    @hookimpl
    def report_result(self, result):
        data = asdict(result, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        self.test_cases.append(data)

    @hookimpl
    def report_container(self, container):
        data = asdict(container, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        self.test_containers.append(data)

    @hookimpl
    def report_attached_file(self, source, file_name):
        pass

    @hookimpl
    def report_attached_data(self, body, file_name):
        self.attachments[file_name] = body
