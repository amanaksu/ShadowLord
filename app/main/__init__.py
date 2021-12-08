# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.2		2021.12.08		Route 상태 체크용 경로 추가 ("/")
# 0.1.1		2021.12.08		DB 연결 설정
# 0.1.0		2021.12.07		App 생성 ProtoType 설계
#

# 내장 라이브러리

# 서드파티 라이브러리
from fastapi import FastAPI

# 자체 라이브러리
from main.common import config
from main.database.conn import db
from main.routes import index

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.2"

# 환경 변수


def create_app():
	"""
	Application 실행
	:return:
	"""
	# App 초기화
	conf_dict = config.to_dict()
	app = FastAPI()
	db.init_app(app, **conf_dict)

	# 데이터베이스 초기화

	# 레지스 초기화

	# 미들웨어 정의

	# 라우터 정의
	app.include_router(index.router)

	return app





