from RPA.Browser.Selenium import Selenium


class Browser(object):
    def __init__(self, browser):
        self.browser = browser

        if isinstance(browser, Selenium):
            self.browser_type = "Selenium"
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def wait_until_page_contains_element(self, xpath, timeout):
        if self.browser_type == "Selenium":
            return self.browser.wait_until_page_contains_element(xpath, timeout)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def click_element_when_visible(self, xpath):
        if self.browser_type == "Selenium":
            self.browser.click_element_when_visible(xpath)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def press_keys(self, key):
        if self.browser_type == "Selenium":
            self.browser.press_keys(None, key)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def execute_javascript(self, code):
        if self.browser_type == "Selenium":
            return self.browser.execute_javascript(code)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def find_element(self, xpath):
        if self.browser_type == "Selenium":
            return self.browser.find_element(xpath)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")
