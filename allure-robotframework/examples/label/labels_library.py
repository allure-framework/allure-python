
import allure


@allure.label('layer', 'UI')
def open_browser_with_ui_layer():
    pass


def add_custom_label(label_type, *labels):
    allure.dynamic.label(label_type, *labels)
