# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.09		Model 추가
#

# 내장 라이브러리
from enum import Enum

# 서드파티 라이브러리
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

# 자체 라이브러리

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"


class UserRegister(BaseModel):
	email: EmailStr = None
	pw: str = None

class AuthType(str, Enum):
	email: str = "email"
	ldap: str = "ldap"
	sso: str = "sso"

class Token(BaseModel):
	Authorization: str = None

class UserToken(BaseModel):
	id: int
	pw: str = None
	email: str = None
	name: str = None
	auth_type: str = None

	class Config:
		orm_mode = True