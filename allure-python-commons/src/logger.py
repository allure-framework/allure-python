import base64
import io
import os
from pathlib import Path
import json
import uuid
import shutil
import requests
from attr import asdict
from allure_commons import hookimpl

INDENT = 4


class AllureFileLogger:

    def __init__(self, report_dir, clean=False):
        self._report_dir = Path(report_dir).absolute()
        if self._report_dir.is_dir() and clean:
            shutil.rmtree(self._report_dir)
        self._report_dir.mkdir(parents=True, exist_ok=True)

    def _report_item(self, item):
        indent = INDENT if os.environ.get("ALLURE_INDENT_OUTPUT") else None
        filename = item.file_pattern.format(prefix=uuid.uuid4())
        data = asdict(
            item,
            filter=lambda attr, value: not (
                type(value) != bool and not bool(value)
            )
        )
        with io.open(self._report_dir / filename, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, indent=indent, ensure_ascii=False)

    @hookimpl
    def report_result(self, result):
        self._report_item(result)

    @hookimpl
    def report_container(self, container):
        self._report_item(container)

    @hookimpl
    def report_attached_file(self, source, file_name):
        destination = self._report_dir / file_name
        shutil.copy2(source, destination)

    @hookimpl
    def report_attached_data(self, body, file_name):
        destination = self._report_dir / file_name
        with open(destination, 'wb') as attached_file:
            if isinstance(body, str):
                attached_file.write(body.encode('utf-8'))
            else:
                attached_file.write(body)


class AllureHTTPLogger:

    def __init__(self, allure_server, project_id, clean=False):
        self._allure_server = allure_server
        self._project_id = project_id
        self._headers = {'Content-type': 'application/json'}
        self._ssl_verification = True
        self._results = []
        if clean:
            self.clean_history()

    def _report_item(self, item):
        filename = item.file_pattern.format(prefix=uuid.uuid4())
        data = asdict(
            item,
            filter=lambda attr, value: not (
                type(value) != bool and not bool(value)
            )
        )
        json_data = json.dumps(data, ensure_ascii=False)
        b64_content = base64.b64encode(json_data.encode('utf-8'))
        self._results.append({'file_name': filename, 'content_base64': b64_content.decode('UTF-8')})

    @hookimpl
    def send_results(self):
        if self._results:
            self._send_post_request('send-results', self._results)
            self._results = []

    @hookimpl
    def create_report(self, execution_name=None):
        return self._send_get_request('generate-report',
                                      params={'execution_name': execution_name or uuid.uuid4(),
                                              'execution_from': 'Python',
                                              'execution_type': 'github'})

    @hookimpl
    def report_result(self, result):
        self._report_item(result)

    @hookimpl
    def report_container(self, container):
        self._report_item(container)

    @hookimpl
    def report_attached_file(self, source, file_name):
        b64_content = base64.b64encode(source)
        self._results.append({'file_name': file_name, 'content_base64': b64_content.decode('UTF-8')})

    @hookimpl
    def report_attached_data(self, body, file_name):
        if isinstance(body, str):
            b64_content = base64.b64encode(body.encode('utf-8'))
        else:
            b64_content = base64.b64encode(body)
        self._results.append({'file_name': file_name, 'content_base64': b64_content.decode('UTF-8')})

    def clean_results(self):
        self._send_get_request('clean-results')

    def clean_history(self):
        self._send_get_request('clean-history')

    def _send_post_request(self, route: str, results: list):
        request_body = {"results": results}
        json_request_body = json.dumps(request_body)

        request_url = f'{self._allure_server}/allure-docker-service/{route}?project_id={self._project_id}'
        response = requests.post(request_url, headers=self._headers, data=json_request_body,
                                 verify=self._ssl_verification)
        response.raise_for_status()  # Raising exception if response is not ok
        return json.loads(response.content)

    def _send_get_request(self, route: str, params: dict = None):
        request_url = f'{self._allure_server}/allure-docker-service/{route}?project_id={self._project_id}'
        response = requests.get(request_url, params=params, headers=self._headers, verify=self._ssl_verification)
        response.raise_for_status()  # Raising exception if response is not ok
        return json.loads(response.content)


class AllureMemoryLogger:

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
        self.attachments[file_name] = source

    @hookimpl
    def report_attached_data(self, body, file_name):
        self.attachments[file_name] = body
