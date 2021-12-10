# -*- coding:utf-8 -*-
#
# 모듈 : 토큰 인증 모듈
# 설명 : 토큰 기반으로 인증을 수행하는 모듈
#
# [개발 로그]
# 0.1.2		2021.12.11		정규표현식 함수 추가 
# 0.1.1		2021.12.11		토큰 인증로직 추가 
# 0.1.0		2021.12.09		AccessControl 클래스 초기 모델 
#

# 내장 라이브러리
from os import access
import time
import typing
import re
import traceback

# 서드파티 라이브러리
from fastapi.params import Header
from starlette import requests
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

import jwt

# 자체 라이브러리
from main.common import consts
from utils.date_utils import D

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.2"


class AccessControl:
	def __init__(self, app: ASGIApp, except_path_list: typing.Sequence[str] = [], except_path_regex: str = None) -> None:
		self.app = app
		self.except_path_list = except_path_list
		self.except_path_regex = except_path_regex

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		request = Request(scope=scope)		
		header = Header(scope=scope)

		request.state.start = time.time()
		request.state.inspect = None
		request.state.user = None
		request.state.is_admin_access = None
		ip_from = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.key() else None

		if (await self.url_pattern_check(request.url.path, self.except_path_regex)) or (request.url.path in self.except_path_list):
			return await self.app(scope, receive, send)

		if request.url.path.startswith("/api"):
			# API 호출인 경우
			# 헤더 내 토큰 검사

			# - 헤더 내 토큰이 있는 경우
			if "Authorization" in request.headers.keys():
				request.state.user = await self.token_decode(access_token=request.headers.get("Authorization"))

			# - 헤더 내 토큰이 없는 경우 
			else:
				response = JSONResponse(status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED"))
				return await response(scope, receive, send)

		else:
			# 템플릿 렌더링의 경우
			# 쿠키에서 토큰 검사 

			# - 쿠키 내 토큰이 있는 경우 
			if "Authorization" in request.cookies.keys():
				request.state.user = await self.token_decode(access_token=request.cookies.get("Authorization"))

			# - 쿠키 내 토큰이 없는 경우 
			else:
				response = JSONResponse(status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED"))
				return await response(scope, receive, send)

		request.state.req_time = D.datetime()
		response = await self.app(scope, receive, send)
		return response


	@staticmethod
	def url_pattern_check(path, pattern):
		"""
		:param	path:
		:param	pattern:
		:return:
		"""
		result = re.match(pattern, path)
		if result:
			return True
		else:
			return False


	@staticmethod
	def token_decode(access_token):
		"""
		:param	access_token:
		:return:
		"""
		payload = None
		try:
			access_token = access_token.replace("Bearer ", "")
			payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithm=[consts.JWT_ALGORITHM])

		except:
			traceback.print_exc()

		finally:
			return payload

		
