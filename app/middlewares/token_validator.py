# -*- coding:utf-8 -*-
#
# 모듈 : 토큰 인증 모듈
# 설명 : 토큰 기반으로 인증을 수행하는 모듈
#
# [개발 로그]
# 0.1.3		2021.12.11		예외처리 수정 
# 0.1.2		2021.12.11		정규표현식 함수 추가 
# 0.1.1		2021.12.11		토큰 인증로직 추가 
# 0.1.0		2021.12.09		AccessControl 클래스 초기 모델 
#

# 내장 라이브러리
import time
import typing
import re

# 서드파티 라이브러리
from fastapi.params import Header
from starlette import requests
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

# 자체 라이브러리
from errors import exceptions as ex
from errors.exceptions import APIException
from main.common import consts
from main.models import UserToken
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

		response = None
		try:
			if request.url.path.startswith("/api"):
				# API 호출인 경우
				# 헤더 내 토큰 검사

				# - 헤더 내 토큰이 있는 경우
				if "Authorization" in request.headers.keys():
					token_info = await self.token_decode(access_token=request.headers.get("Authorization"))
					request.state.user = UserToken(**token_info)

				# - 헤더 내 토큰이 없는 경우 
				else:
					raise ex.NotAuthorized()

			else:
				# 템플릿 렌더링의 경우
				# 쿠키에서 토큰 검사 

				# - 쿠키 내 토큰이 있는 경우 
				if "Authorization" in request.cookies.keys():
					token_info = await self.token_decode(access_token=request.cookies.get("Authorization"))
					request.state.user = UserToken(**token_info)

				# - 쿠키 내 토큰이 없는 경우 
				else:
					raise ex.NotAuthorized()

			request.state.req_time = D.datetime()
			response = await self.app(scope, receive, send)

		except APIException as e:
			response = await self.exception_handler(e)
			response = await response(scope, receive, send)

		finally:
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

		except ExpiredSignatureError:
			raise ex.TokenExpiredEx()
		except DecodeError:
			raise ex.TokenDecodeEx()

		finally:
			return payload


	async def exception_handler(error: APIException):
		error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
		response = JSONResponse(status_code=error.status_code, content=error_dict)
		return response

		
