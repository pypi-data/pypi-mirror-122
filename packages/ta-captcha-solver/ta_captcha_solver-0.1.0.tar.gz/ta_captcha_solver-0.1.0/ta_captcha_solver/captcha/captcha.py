from abc import ABC, abstractmethod
from collections import defaultdict

from ..exceptions import (
    UICaptchaNotSolved,
    ParamsException,
)

from ..browser.browser import Browser
from ..api.captcha_guru import CaptchaGuru


class Captcha(ABC):
    def __init__(self, **params):
        self.browser = Browser(params["browser"])
        self.api_provider = CaptchaGuru(params["captcha_guru_api_key"])

        self.params = defaultdict(str, params)
        self.token = None

    @abstractmethod
    def solve(self):
        pass

    def click_solve_captcha(self):
        self.browser.click_element_when_visible(self.params["click_xpath"])

    def check_captcha(self):
        try:
            self.browser.wait_until_page_contains_element(
                self.params["check_xpath"], timeout=5
            )
        except:
            raise UICaptchaNotSolved()
