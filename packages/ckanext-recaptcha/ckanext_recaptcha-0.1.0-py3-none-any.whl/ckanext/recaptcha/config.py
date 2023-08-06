from __future__ import annotations
from collections.abc import Container
from typing import Optional

import ckan.plugins.toolkit as tk

TPL_ENDPOINTS = "ckanext.recaptcha.{profile}.controlled_endpoints"
DEFAULT_ENDPOINTS = []

TPL_KEY = "ckanext.recaptcha.{profile}.site_key"
DEFAULT_KEY = None

TPL_SECRET = "ckanext.recaptcha.{profile}.secret_key"
DEFAULT_SECRET = None

TPL_TYPE = "ckanext.recaptcha.{profile}.type"
DEFAULT_TYPE = "v3"

TPL_FIELD = "ckanext.recaptcha.{profile}.field_name"
DEFAULT_FIELD = "g-recaptcha-response"

TPL_JS = "ckanext.recaptcha.{profile}.include_js"
DEFAULT_JS = True


def controlled_endpoints(profile: str = "default") -> Container[str]:
    return set(
        tk.aslist(
            tk.config.get(TPL_ENDPOINTS.format(profile=profile), DEFAULT_ENDPOINTS)
        )
    )


def key(profile: str = "default") -> Optional[str]:
    return tk.config.get(TPL_KEY.format(profile=profile), DEFAULT_KEY)


def secret(profile: str = "default") -> Optional[str]:
    return tk.config.get(TPL_SECRET.format(profile=profile), DEFAULT_SECRET)


def recaptcha_type(profile: str = "default") -> str:
    return tk.config.get(TPL_TYPE.format(profile=profile), DEFAULT_TYPE)


def field(profile: str = "default") -> str:
    return tk.config.get(TPL_FIELD.format(profile=profile), DEFAULT_FIELD)


def include_js(profile: str = "default") -> bool:
    return tk.asbool(tk.config.get(TPL_JS.format(profile=profile), DEFAULT_JS))
