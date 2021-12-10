# -*- coding:utf-8 -*-
#
# 모듈 : 사용자 정보 API
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.11		사용자 정보 추출 API 
#

# 내장 라이브러리

# 서드파티 라이브러리
from fastapi import APIRouter
from starlette.requests import Request

# 자체 라이브러리
from main.database.schema import Users
from main.models import UserMe

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

router = APIRouter()



@router.get("/me", response_model=UserMe)
async def get_user(request: Request):
	"""
	get user info
	:param	request:
	:return:
	"""
	user = request.state.user
	user_info = Users.get(id=user.id)
	return user_info