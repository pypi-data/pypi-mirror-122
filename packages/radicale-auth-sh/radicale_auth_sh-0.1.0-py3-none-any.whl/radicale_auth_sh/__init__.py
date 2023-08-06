"""Plugin radicale-auth-sh
==========================

Simple salted and hashed password authentication plugin.

"""
from radicale.auth import BaseAuth
from radicale.log import logger
from .crypt import ph


__author__ = "Ashwin V. Mohanan"
__version__ = "0.1.0"


PLUGIN_CONFIG_SCHEMA = {"auth": {"secret": {"value": "", "type": str}}}


class Auth(BaseAuth):
    def __init__(self, configuration):
        super().__init__(configuration.copy(PLUGIN_CONFIG_SCHEMA))

    def login(self, login, password):
        # Get password from configuration option
        secret = self.configuration.get("auth", "secret")
        # Check authentication
        logger.info("Login attempt by %r", login)

        if ph.verify(secret, password):
            return login
        return ""
