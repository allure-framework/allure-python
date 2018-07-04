*** Settings ***
Library    ./library/run.py
Library    ./library/test.py


*** Variables ***
${TC_ATTACH_DATA}    | *Settings*                 |               |              |\n
...                  | Library                    | AllureLibrary |              |\n
...                  |                            |               |              |\n
...                  | *TestCase*                 |               |              |\n
...                  | Demo Test Case Attach Data |               |              |\n
...                  |                            | Attach        | Hello world  |\n

${TC_ATTACH_DATA_WITH_NAME_AND_TYPE}
...    | *Settings*                                    |               |                      |\n
...    | Library                                       | AllureLibrary |                      |\n
...    |                                               |               |                      |\n
...    | *TestCase*                                    |               |                      |\n
...    | Demo Test Case Attach Data With Name And Type |               |                      |\n
...    |                                               | Attach        | Hello world          |\n
...    |                                               | ...           | name=my message      |\n
...    |                                               | ...           | attachment_type=TEXT |\n

${TC_ATTACH_FILE}    | *Settings*                 |               |                  |\n
...                  | Library                    | AllureLibrary |                  |\n
...                  |                            |               |                  |\n
...                  | *TestCase*                 |               |                  |\n
...                  | Demo Test Case Attach File |               |                  |\n
...                  |                            | Attach File   | \${SUITE SOURCE} |\n

@{TC_ATTACH_RECIPE__URANIUM_LIBRARY}
...    import os
...
...    def capture_page_screenshot():
...    \ \ cur_dir = "${TEMPDIR}"
...    \ \ screenshot_path = os.path.join(cur_dir, 'uranium-screenshot.txt')
...    \ \ with open(screenshot_path, 'w+') as screenshot:
...    \ \ \ \ screenshot.write("Grab some beer and be happy~(^o^)-c[~]")
...    \ \ return screenshot_path

@{TC_ATTACH_RECIPE__URANIUM_LIBRARY_HELPER}
...    import allure
...    from robot.libraries.BuiltIn import BuiltIn
...
...    class UraniumLibraryHelper(object):
...    \ \ ROBOT_LIBRARY_SCOPE = "TEST SUITE"
...    \ \ ROBOT_LISTENER_API_VERSION = 2
...
...    \ \ def __init__(self):
...    \ \ \ \ self.ROBOT_LIBRARY_LISTENER = self
...
...    \ \ def _start_suite(self, name, attrs):
...    \ \ \ \ BuiltIn().set_library_search_order('UraniumLibraryHelper')
...
...    \ \ def capture_page_screenshot(self):
...    \ \ \ \ ul = BuiltIn().get_library_instance('UraniumLibrary')
...    \ \ \ \ path = ul.capture_page_screenshot()
...    \ \ \ \ allure.attach.file(path, name="screenshot", attachment_type=allure.attachment_type.TEXT)
...    \ \ \ \ return path

${TC_ATTACH_RECIPE}    | *Settings*                           |                           |\n
...                    | Library                              | ./UraniumLibrary.py       |\n
...                    | Library                              | ./UraniumLibraryHelper.py |\n
...                    |                                      |                           |\n
...                    | *TestCase*                           |                           |\n
...                    | Demo Test Case With Magic Screenshot |                           |\n
...                    |                                      | Capture Page Screenshot   |\n


*** Test Cases ***
Test Case Attach Data
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    library.robot    ${TC_ATTACH_DATA}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Attach Data
    ${step_matcher}=   Should Has Step    ${allure_report}    ${tc_matcher}    AllureLibrary.Attach
    Should Has Status    ${allure_report}    ${step_matcher}    passed
    Should Has Attachment    ${allure_report}    ${step_matcher}

Test Case Attach Data With Name And Type
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    library.robot    ${TC_ATTACH_DATA_WITH_NAME_AND_TYPE}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}   Demo Test Case Attach Data With Name And Type
    ${step_matcher}=   Should Has Step    ${allure_report}    ${tc_matcher}    AllureLibrary.Attach
    Should Has Status    ${allure_report}    ${step_matcher}    passed
    Should Has Attachment    ${allure_report}    ${step_matcher}    name=my message

Test Case Attach File
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    ${test_case}=    Make Test Case    ${test_case_dir}    library.robot    ${TC_ATTACH_FILE}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}    Demo Test Case Attach File
    ${step_matcher}=   Should Has Step    ${allure_report}    ${tc_matcher}    AllureLibrary.Attach File
    Should Has Status    ${allure_report}    ${step_matcher}    passed
    Should Has Attachment    ${allure_report}    ${step_matcher}

Test Case Attach Recipe
    ${tmp_dir}=    Make Temp Dir
    ${test_case_dir}=    Make Dir    ${tmp_dir}    test
    Make File    ${test_case_dir}    UraniumLibrary.py    ${TC_ATTACH_RECIPE__URANIUM_LIBRARY}
    Make File    ${test_case_dir}    UraniumLibraryHelper.py    ${TC_ATTACH_RECIPE__URANIUM_LIBRARY_HELPER}
    ${test_case}=    Make Test Case    ${test_case_dir}    library.robot    ${TC_ATTACH_RECIPE}
    ${allure_report}=    Robot Run With Allure    ${tmp_dir}    ${test_case}
    ${tc_matcher}=    Should Has Test Case    ${allure_report}   Demo Test Case With Magic Screenshot
    ${step_matcher}=   Should Has Step    ${allure_report}
    ...                                   ${tc_matcher}
    ...                                   UraniumLibraryHelper.Capture Page Screenshot
    Should Has Attachment    ${allure_report}    ${step_matcher}    name=screenshot
