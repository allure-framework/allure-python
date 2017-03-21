# Allure pytest plugin

## Installation
In process. We are hope to get beta on PyPi in april


## Changes

### Attachments
You still can attach some content, but arguments order was changed:

pytest.allure.attach(*content*, name=*name*,  attachment_type=*type*, extension=*extension*)

Where **type** is a mime string or one of presets like pytest.allure.attachment_type.XML. Extension is defined for all presets.

```python
def test_attach_from_test():
    pytest.allure.attach(xml_body)
    pytest.allure.attach(xml_body,
                         name='my xml attachment',
                         attachment_type=pytest.allure.attachment_type.XML)
    # ...
```

Also you can attach files:
pytest.allure.attach.file(*path to file*, name=*name*,  attachment_type=*type*, extension=*extension*)

```python
def test_attach_from_test():
    pytest.allure.attach(xml_body)
```

### Steps
Step name formatting with function parameters is deprecated. All parameters of step function will be reported and shown in report.


### Issues
#### Dynamic issues
Current version doesn't support dynamic_issue, but you can do it with pytest fixtures:
```python
import pytest


@pytest.fixture
def dynamic_issue(request):
    def mark(link):
        request.node.add_marker(pytest.allure.issue(link))
    return mark


@pytest.mark.parametrize('issue, result', [('ISSUE-1', True), ('ISSUE-2', False)])
def test_dynamic_issue(dynamic_issue, issue, result):
    dynamic_issue(issue)
    assert result
```
