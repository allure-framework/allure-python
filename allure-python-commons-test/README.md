## Allure Python Testing Utilities

[![Release Status](https://img.shields.io/pypi/v/allure-python-commons-test)](https://pypi.python.org/pypi/allure-python-commons-test)
[![Downloads](https://img.shields.io/pypi/dm/allure-python-commons-test)](https://pypi.python.org/pypi/allure-python-commons-test)

> The package contains pyhamcrest matchers to assert the Allure results. They
> come in handy when you need to test an Allure adapter.

[<img src="https://allurereport.org/public/img/allure-report.svg" height="85px" alt="Allure Report logo" align="right" />](https://allurereport.org "Allure Report")

- Learn more about Allure Report at [https://allurereport.org](https://allurereport.org)
- 📚 [Documentation](https://allurereport.org/docs/) – discover official documentation for Allure Report
- ❓ [Questions and Support](https://github.com/orgs/allure-framework/discussions/categories/questions-support) – get help from the team and community
- 📢 [Official announcements](https://github.com/orgs/allure-framework/discussions/categories/announcements) –  stay updated with our latest news and updates
- 💬 [General Discussion](https://github.com/orgs/allure-framework/discussions/categories/general-discussion) – engage in casual conversations, share insights and ideas with the community
- 🖥️ [Live Demo](https://demo.allurereport.org/) — explore a live example of Allure Report in action

---

## The matchers library

Here is the list of available matchers. Refer to [https://github.com/allure-framework/allure-python/tree/master/tests](https://github.com/allure-framework/allure-python/tree/master/tests) for usage examples.

|Module|Matcher|Check|
|------|-------|-----|
|container|`has_container`|The report contains a container that matches all the provided matchers.|
|container|`has_same_container`|The report contains a container that has all the specified tests as its children|
|container|`has_before`|The container has a before fixture with the specified name that matches all the provided matchers|
|container|`has_after`|The container has an after fixture with the specified name that matches all the provided matchers|
|content|`csv_equivalent`|The string (typically, an attachment's content) contains a CSV document that is equvalent to the provided one|
|label|`has_label`|The test contains a label with the specified name and (optionaly) the value|
|label|`has_severity`|The test has the specified severity label|
|label|`has_epic`|The test has the specified epic label|
|label|`has_feature`|The test has the specified feature label|
|label|`has_story`|The test has the specified story label|
|label|`has_tag`|The test has the specified tag label|
|label|`has_package`|The test has the specified package label|
|label|`has_suite`|The test has the specified suite label|
|label|`has_parent_suite`|The test has the specified parentSuite label|
|label|`has_sub_suite`|The test has the specified subSuite label|
|report|`has_test_case`|The report contains a test whose fullName ends, or name starts with the specified name. Additionally, the test must match all the provided matchers|
|report|`has_only_testcases`|Each test of the report matches at least one of the provided matchers|
|report|`has_only_n_test_cases`|Same as `has_test_case` but also checks if the number of matched tests is equal to the expected one|
|result|`has_title`|The test has an expected name|
|result|`has_description`|The test has a description that matches all the provided matchers|
|result|`has_description_html`|The test has a descriptionHtml that matches all the provided matchers|
|result|`has_step`|The test or step has a step with the specified name that matches all the provided matchers|
|result|`has_parameter`|The test or step has a parameter with the specified name whose value matches the provided matchers|
|result|`doesnt_have_parameter`|The test or step doesn't have a parameter with the specified name|
|result|`has_link`|The test has a link with the expected url, type (if provided) and name (if provided)|
|result|`has_issue_link`|The test has an issue link with the expected url and name (if provided)|
|result|`has_test_case_link`|The test has an issue link with the expected url and name (if provided)|
|result|`has_attachment`|The test or step has an attachment with the expected name and type.|
|result|`has_attachment_with_content`|The test or step has an attachment with the expected name and type. In addition, the content must match the provided matcher.|
|result|`with_id`|The test or container has the expected uuid|
|result|`with_status`|The test or step has the expected status|
|result|`has_status_details`|The status details of the test or step matches all the provided matchers|
|result|`with_message_contains`|The status details' message contains the provided text|
|result|`with_trace_contains`|The status details' trace contains the provided text|
|result|`with_excluded`|The parameter is excluded from the historyId calculation|
|result|`with_mode`|The parameter has the specified mode|
|result|`has_history_id`|The test has historyId|
