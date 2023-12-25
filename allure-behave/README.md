## Allure Behave Formatter

[![Release Status](https://img.shields.io/pypi/v/allure-behave)](https://pypi.python.org/pypi/allure-behave)
[![Downloads](https://img.shields.io/pypi/dm/allure-behave)](https://pypi.python.org/pypi/allure-behave)

> The Allure adapter for [Behave](https://behave.readthedocs.io/en/latest/).

[<img src="https://allurereport.org/public/img/allure-report.svg" height="85px" alt="Allure Report logo" align="right" />](https://allurereport.org "Allure Report")

- Learn more about Allure Report at [https://allurereport.org](https://allurereport.org)
- 📚 [Documentation](https://allurereport.org/docs/) – discover official documentation for Allure Report
- ❓ [Questions and Support](https://github.com/orgs/allure-framework/discussions/categories/questions-support) – get help from the team and community
- 📢 [Official announcements](https://github.com/orgs/allure-framework/discussions/categories/announcements) –  stay updated with our latest news and updates
- 💬 [General Discussion](https://github.com/orgs/allure-framework/discussions/categories/general-discussion) – engage in casual conversations, share insights and ideas with the community
- 🖥️ [Live Demo](https://demo.allurereport.org/) — explore a live example of Allure Report in action

---

## Quick start

```shell
$ pip install allure-behave
$ behave -f allure_behave.formatter:AllureFormatter -o %allure_result_folder% ./features
$ allure serve %allure_result_folder%
```

### Support behave parallel

Current implementation of behave-parallel makes some allure features inaccessible.
So in this case you need patch your environment.py files instead using formatter.
If you don't use environment.py, just create empty one with calling allure like
in example below.

```python
from allure_behave.hooks import allure_report

### your code

allure_report("path/to/result/dir")
```

## Further readings

Learn more from [Allure behave's official documentation](https://allurereport.org/docs/behave/).
