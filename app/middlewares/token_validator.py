# -*- coding:utf-8 -*-
#
# 모듈 : 토큰 인증 모듈
# 설명 : 토큰 기반으로 인증을 수행하는 모듈
#
# [개발 로그]
# 0.1.0		2021.12.09		AccessControl 클래스 초기 모델 
#

# 내장 라이브러리
import time
import typing

# 서드파티 라이브러리
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

# 자체 라이브러리
from utils.date_utils import D

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"


class AccessControl:
	def __init__(self, app: ASGIApp, except_path_list: typing.Sequence[str] = [], except_path_regex: str = None) -> None:
		self.app = app
		self.except_path_list = except_path_list
		self.except_path_regex = except_path_regex

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		request = Request(scope=scope)
		headers = Headers(scope=scope)

		request.state.req_time = D.datetime()
		request.state.start = time.time()
		request.state.inspect = None
		request.state.user = None
		request.state.is_admin_access = None

		response = await self.app(scope, receive, send)
		return response