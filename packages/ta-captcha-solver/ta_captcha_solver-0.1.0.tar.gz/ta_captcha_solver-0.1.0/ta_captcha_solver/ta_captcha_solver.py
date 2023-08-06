from collections import defaultdict

from .captcha.image_captcha import ImageCaptcha
from .captcha.re_captcha_v2 import ReCaptchaV2

from .exceptions import ParamsException


class TACaptchaSolver(object):
    @staticmethod
    def get(**params):
        params = TACaptchaSolver.validate_params(**params)
        if "image" in params["captcha_type"]:
            return ImageCaptcha(**params)
        elif "v2" in params["captcha_type"]:
            return ReCaptchaV2(**params)
        else:
            raise ParamsException(
                "Incorrect captcha_type provided. Dont know what captcha need to solve!"
            )

    @staticmethod
    def validate_params(**params):
        params = defaultdict(str, params)

        if not params["captcha_type"] or not isinstance(params["captcha_type"], str):
            raise ParamsException(
                "No captcha_type provided or incorrect data type. Dont know what captcha need to solve!"
            )

        if not params["browser"]:
            raise ParamsException(
                "No browser provided. Cannot work without any browser!"
            )

        if not params["captcha_guru_api_key"] or not isinstance(
            params["captcha_guru_api_key"], str
        ):
            raise ParamsException(
                "No api key provided or incorrect data type. Cannot work without third party API tool!"
            )

        return params
