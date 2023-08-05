#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_chat_ws main application module

This module can be used by GUnicorn or Uvicorn to create application:

    >>> import asyncio
    >>> import json
    >>> import os

    >>> import uvicorn
    >>> from pyams_chat_ws.webapp import create_application

    >>> base = os.path.dirname(__file__)

    >>> with open(os.path.join(base, 'etc', 'config.json'), 'r') as config_file:
    ...     config = json.loads(config_file.read())

    >>> loop = asyncio.get_event_loop()
    >>> application = loop.run_until_complete(create_application(config))

    >>> if __name__ == '__main__':
    >>>     uvicorn.run(application, host='0.0.0.0', port=8000)

"""

# pylint: disable=logging-fstring-interpolation

from starlette.middleware.authentication import AuthenticationMiddleware

from .app import ChatApp
from .auth import JWTAuthenticationBackend


__docformat__ = 'restructuredtext'


async def create_application(config):
    app = await ChatApp.create(config)
    app.add_middleware(AuthenticationMiddleware,
                       backend=JWTAuthenticationBackend(config))
    return app
