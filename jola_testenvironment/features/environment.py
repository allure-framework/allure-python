from enum import Enum
import os



class Option(str, Enum):
    OPTION_A = "Option A"
    OPTION_B = "Option B"

def before_all(context):
    os.environ["TEST_HISTORY_FACTOR"] = Option.OPTION_A.value

    print(f"INFO: {os.getenv('TEST_HISTORY_FACTOR')}")
    pass

def before_scenario(context, scenario):
    pass

def before_step(context, step):
        pass


def before_feature(context,feature):
    pass

def before_scenario(context,feature):
    pass

def after_all(context):
    pass