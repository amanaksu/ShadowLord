# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.09		사용자 인증
#

# 내장 라이브러리
from datetime import datetime, timedelta

# 서드파티 라이브러리
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import JSON
from starlette.responses import JSONResponse
import bcrypt
import jwt

# 자체 라이브러리
from main.common.consts import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_DELTA_DAYS
from main.models import AuthType, Token, UserToken, UserRegister
from main.database.schema import Users
from main.database.conn import db

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

router = APIRouter()

@router.post("/register/{auth_type}", status_code=200, response_model=Token)
async def register(auth_type: AuthType, reg_info: UserRegister, session: Session=Depends(db.session)):
	"""
	가입 API
	:param	auth_type: 가입 방식
	:param	reg_info: 가입 정보
	:param	session: 
	:return:
	"""
	if auth_type == AuthType.email:
		# 인증에 필요한 정보가 있는지 확인한다. 
		if not (reg_info.email or reg_info.pw):
			return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided."))

		# 기 가입 여부를 확인한다. 
		is_exist = await is_email_exist(reg_info.email)
		if is_exist:
			return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))

		# 신규 가입인 경우
		hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
		new_user = Users.create(session, auto_commit=True, pw=hash_pw, email=reg_info.email)
		token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw'}),)}")
		return token
	
	return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


@router.post("/login/{auth_type}", status_code=200)
async def login(auth_type: AuthType, user_info: UserRegister):
	"""
	로그인 API
	:param	auth_type: 로그인 방식
	:param	user_info: 로그인 정보
	:return:
	"""
	pass





async def is_email_exist(email: str):
	get_email = Users.get(email=email)
	if get_email:
		return True
	else:
		return False


def create_access_token(*, data: dict=None, expires_delta: int=None):
	to_encode = data.copy()
	if not expires_delta:
		expires_delta = JWT_EXPIRES_DELTA_DAYS 

	to_encode.update({"exp" : datetime.utcnow() + timedelta(days=expires_delta)})
	encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
	return encoded_jwt