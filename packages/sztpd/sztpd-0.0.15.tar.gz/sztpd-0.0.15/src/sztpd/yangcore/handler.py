
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
from abc import ABCMeta,abstractmethod
from aiohttp import web
class RouteHandler(metaclass=ABCMeta):
	'\n    Abstract base class for `aiohttp` route handlers for a RESTCONF API.\n      - only NMDA-based routes, per RFC 8527, are supported at this time.\n      - support for legacy RESTCONF routes, per RFC 8040, may be added later.\n    '
	@abstractmethod
	async def handle_get_restconf_root(self,request):'\n        Called when there is a GET request to /\n        '
	@abstractmethod
	async def handle_get_yang_library_version(self,request):'\n        Called when there is a GET request to /yang-library\n        '
	@abstractmethod
	async def handle_get_opstate_request(self,request):'\n        Called when there is a GET request to /ds/ietf-datastores:operational.\n        '
	@abstractmethod
	async def handle_get_config_request(self,request):'\n        Called when there is a GET request to /ds/ietf-datastores:running.\n        '
	@abstractmethod
	async def handle_post_config_request(self,request):'\n        Called when there is a POST request to /ds/ietf-datastores:running.\n        '
	@abstractmethod
	async def handle_put_config_request(self,request):'\n        Called when there is a PUT request to /ds/ietf-datastores:running.\n        '
	@abstractmethod
	async def handle_delete_config_request(self,request):'\n        Called when there is a DELETE request to /ds/ietf-datastores:running.\n        '
	@abstractmethod
	async def handle_action_request(self,request):'\n        Called when there is a POST request to /ds/ietf-datastores:operational.\n        '
	@abstractmethod
	async def handle_rpc_request(self,request):'\n        Called when there is a POST request to /operations.\n        '