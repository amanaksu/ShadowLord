# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.07		App 생성 ProtoType 설계
#

# 내장 라이브러리

# 서드파티 라이브러리
from fastapi import FastAPI

# 자체 라이브러리
from main.common import config

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

# 환경 변수


def create_app():
	"""
	Application 실행
	:return:
	"""
	# App 초기화
	conf_dict = config.to_dict()
	app = FastAPI()

	# 데이터베이스 초기화

	# 레지스 초기화

	# 미들웨어 정의

	# 라우터 정의

	return app