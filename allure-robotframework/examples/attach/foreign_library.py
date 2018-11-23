import os
from tempfile import mkdtemp


class ForeignLibrary(object):

    def capture_page_screenshot(self):
        tmp = mkdtemp()
        screenshot_path = os.path.join(tmp, 'screenshot.txt')
        with open(screenshot_path, 'w+') as screenshot:
            screenshot.write("Grab some beer and be happy~(^o^)-c[~]")
            return screenshot_path


foreign_library = ForeignLibrary
