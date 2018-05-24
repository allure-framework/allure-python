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


class AllureFileLogger(object):

    def __init__(self, report_dir, clean=False):
        self._report_dir = report_dir

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        elif clean:
            for f in os.listdir(report_dir):
                f = os.path.join(report_dir, f)
                if os.path.isfile(f):
                    os.unlink(f)

    def _report_item(self, item):
        indent = INDENT if os.environ.get("ALLURE_INDENT_OUTPUT") else None
        filename = item.file_pattern.format(prefix=uuid.uuid4())
        data = asdict(item, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
        with io.open(os.path.join(self._report_dir, filename), 'w', encoding='utf8') as json_file:
            if sys.version_info.major < 3:
                json_file.write(unicode(json.dumps(data, indent=indent, ensure_ascii=False, encoding='utf8')))
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
