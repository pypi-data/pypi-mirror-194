# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
.. _ref-guides-integrating-an-oauth2-authorization-server

=============================================================
Implementing an OAuth 2.x/OpenID Connect authorization server
=============================================================
"""
from .authorizationendpoint import AuthorizationEndpoint
from .authorizationcodecallbackendpoint import AuthorizationCodeCallbackEndpoint
from .loginendpoint import LoginEndpoint
from .oidcregistrationendpoint import OIDCRegistrationEndpoint


__all__: list[str] = [
    'AuthorizationEndpoint',
    'AuthorizationCodeCallbackEndpoint',
    'LoginEndpoint',
    'OIDCRegistrationEndpoint',
]