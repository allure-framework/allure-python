import allure
import allure_commons


@allure_commons.fixture
def before_feature(context, feature):
    allure.attach(
        "Attachment from before_feature",
        name="Dynamic attachment",
        attachment_type=allure.attachment_type.TEXT
    )
