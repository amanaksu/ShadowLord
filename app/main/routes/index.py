# -*- coding:utf-8 -*-
#
# 모듈 : Router 경로 모듈
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.08		Route 상태 체크용 함수 추가 (index)
#

# 내장 라이브러리
from datetime import datetime

# 서드파티 라이브러리
from fastapi import APIRouter
from starlette.responses import Response
from starlette.requests import Request

# 자체 라이브러리

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

router = APIRouter()


@router.get("/")
async def index():
	"""
	ELB 상태 체크용 API
	:return:
	"""
	current_time = datetime.utcnow()
	return Response(f"ShadowLord API (UTC : {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


@router.get("/test")
async def index(request: Request):
	"""
	ELB 상태체크용 API
	:return:
	"""
	current_time = datetime.utcnow()
	return Response(f"ShadowLord API (UTC : {current_time.strftime('%Y.%m.%d %H:%M:%S')})")
