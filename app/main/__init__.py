# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.3		2021.12.09		인증 로직 추가 
# 0.1.2		2021.12.08		Route 상태 체크용 경로 추가 ("/")
# 0.1.1		2021.12.08		DB 연결 설정
# 0.1.0		2021.12.07		App 생성 ProtoType 설계
#

# 내장 라이브러리

# 서드파티 라이브러리
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.cors import CORSMiddleware

# 자체 라이브러리
from main.common import config, consts
from main.database.conn import db
from main.routes import index, auth, users
from middlewares.token_validator import AccessControl
from middlewares.trusted_hosts import TrustedHostMiddleware

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.3"

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app():
	"""
	Application 실행
	:return:
	"""
	# App 초기화
	conf_dict = config.to_dict()
	print(conf_dict)
	app = FastAPI()
	db.init_app(app, **conf_dict)

	# 데이터베이스 초기화

	# 레지스 초기화

	# 미들웨어 정의
	app.add_middleware(AccessControl, except_path_list=consts.EXCEPT_PATH_LIST, except_path_regex=consts.EXCEPT_PATH_REGEX)
	app.add_middleware(CORSMiddleware, allow_origins=conf_dict.get("ALLOWED_HOSTS"), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
	app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf_dict.get("TRUSTED_HOSTS"), except_path_list=["/health"])

	# 라우터 정의
	app.include_router(index.router)
	app.include_router(auth.router, tags=["Authentication"], prefix="/api")
	app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])

	return app





