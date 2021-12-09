# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		XXXX.XX.XX		ProtoType
#

# 내장 라이브러리
import typing

# 서드파티 라이브러리
from starlette.datastructures import Headers, URL
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

# 자체 라이브러리

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"



class TrustedHostMiddleware:
	def __init__(self, app:ASGIApp, allowed_hosts: typing.Sequence[str] = ['*'], except_path_list: typing.Sequence[str] = [], www_redirect: bool = True) -> None:
		self.app = app
		self.allowed_hosts = allowed_hosts
		self.allow_any = "*" in self.allowed_hosts
		self.except_path_list = except_path_list
		self.www_redirect = www_redirect

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		if self.allow_any or scope["type"] not in ["http", "websocket"]:
			await self.app(scope, receive, send)
			return 

		headers = Headers(scope=scope)
		host = headers.get("host", "").split(":")[0]
		is_valid_host = False
		found_www_redirect = False
		for pattern in self.allowed_hosts:
			if ((pattern == host) or \
			   	(pattern.startswith("*") and host.endswith(pattern[1:])) or \
			   	URL(scope=scope).path in self.except_path_list):
				is_valid_host = True
				break

			if pattern == "www." + host:
				found_www_redirect = True

		if is_valid_host:
			await self.app(scope, receive, send)

		else:
			if found_www_redirect and self.www_redirect:
				url = URL(scope=scope)
				redirect_url = url.replace(netloc="www." + url.netloc)
				response = RedirectResponse(url=str(redirect_url))
			else:
				response = PlainTextResponse("Invalid Host Header", status_code=400)

			await response(scope, receive, send)

