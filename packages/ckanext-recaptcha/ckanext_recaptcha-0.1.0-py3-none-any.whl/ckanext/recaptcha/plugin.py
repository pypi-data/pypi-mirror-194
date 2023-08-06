from __future__ import annotations
from typing import TYPE_CHECKING

import requests

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import config

if TYPE_CHECKING:
    from ckan.common import CKANConfig
    from ckan.config.middleware.flask_app import CKANFlask


class RecaptchaPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IMiddleware, inherit=True)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "recaptcha")

    # IMiddleware
    def make_middleware(self, app: CKANFlask, config: CKANConfig) -> CKANFlask:
        app.before_request(verify_recaptcha)
        return app

    # ITemplateHelpers
    def get_helpers(self):
        helpers = {
            "recaptcha_site_key": config.key,
            "recaptcha_render_mode": render_mode,
            "recaptcha_include_js": config.include_js,
        }
        if "csrf_input" not in tk.h:
            helpers["csrf_input"] = lambda: ""

        return helpers


def verify_recaptcha():
    if tk.request.method != "POST":
        return

    secret = config.secret()
    if not secret:
        return

    if tk.request.endpoint not in config.controlled_endpoints():
        return

    token = tk.request.form.get(config.field(), "")

    try:
        check_recaptcha(token, secret)
    except RecaptchaError:
        error_msg = tk._("Bad Captcha. Please try again.")
        tk.h.flash_error(error_msg)
        return tk.redirect_to(tk.request.url)


def check_recaptcha(token: str, secret: str, ip: str = "Unknown IP Address") -> None:

    recaptcha_server_name = "https://www.google.com/recaptcha/api/siteverify"

    params = dict(secret=secret, remoteip=ip, response=token)

    timeout = tk.asint(tk.config.get("ckan.requests.timeout", 5))
    response = requests.get(recaptcha_server_name, params, timeout=timeout)

    data = response.json()

    if not data["success"]:
        raise RecaptchaError()


class RecaptchaError(ValueError):
    pass


def render_mode(profile: str = "default") -> str:
    type_ = config.recaptcha_type(profile)

    if type_ == "v2-invisible":
        return "explicit"

    return config.key(profile) or ""
