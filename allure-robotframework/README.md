## Allure Robot Framework Listener

[![Release Status](https://img.shields.io/pypi/v/allure-robotframework)](https://pypi.python.org/pypi/allure-robotframework)
[![Downloads](https://img.shields.io/pypi/dm/allure-robotframework)](https://pypi.python.org/pypi/allure-robotframework)

> An Allure adapter for [Robot Framework](https://robotframework.org/).

[<img src="https://allurereport.org/public/img/allure-report.svg" height="85px" alt="Allure Report logo" align="right" />](https://allurereport.org "Allure Report")

- Learn more about Allure Report at [https://allurereport.org](https://allurereport.org)
- 📚 [Documentation](https://allurereport.org/docs/) – discover official documentation for Allure Report
- ❓ [Questions and Support](https://github.com/orgs/allure-framework/discussions/categories/questions-support) – get help from the team and community
- 📢 [Official announcements](https://github.com/orgs/allure-framework/discussions/categories/announcements) –  stay updated with our latest news and updates
- 💬 [General Discussion](https://github.com/orgs/allure-framework/discussions/categories/general-discussion) – engage in casual conversations, share insights and ideas with the community
- 🖥️ [Live Demo](https://demo.allurereport.org/) — explore a live example of Allure Report in action

---

## Installation and Usage

```shell
$ pip install allure-robotframework
$ robot --listener allure_robotframework ./my_robot_test
```

The default output directory is `output/allure`.
Use the listener's argument to change it:

```shell
$ robot --listener allure_robotframework:/set/your/path/here ./my_robot_test
```

The listener supports [the robotframework-pabot library](https://pypi.python.org/pypi/robotframework-pabot):

```shell
$ pabot --listener allure_robotframework ./my_robot_test
```

The advanced listener settings:

  - ALLURE_MAX_STEP_MESSAGE_COUNT=5. If a robotframework step contains less
    messages than has been specified by this setting, each message is shown as a substep.
    This reduces the number of attachments in large projects. The default value
    is zero - all messages are displayed as attachments.

### Usage examples

See the usage examples [here](https://github.com/allure-framework/allure-python/tree/master/allure-robotframework/examples).

## Contributing to allure-robotframework

This project exists thanks to all the people who contribute. Especially to
[Megafon](https://corp.megafon.com) and [@skhomuti](https://github.com/skhomuti)
who has initially started allure-robotframework and has been maintaining it
since then.
