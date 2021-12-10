# -*- coding:utf-8 -*-
#
# 모듈 : 실행 환경변수 모듈
# 설명 : 
#
# [개발 로그]
# 0.1.1		2021.12.08		JWT 토큰 변수 추가
# 0.1.0		2021.12.07		환경변수 추가 (RUN_ENV)
#

# 내장 라이브러리

# 서드파티 라이브러리

# 자체 라이브러리

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.2"

# 환경 변수

# 실행모드
# - dev : 개발모드  (development mode)
# - prod : 제품모드 (release mode)
RUN_ENV			= "dev"		

# JWT
# - JWT_EXPIRES_DELTA_DAYS : 생성된 토큰 허용 시간 (Days)
# - JWT_SECRET : 토큰 생성용 비밀키
# - JWT_ALGORITHM : 토큰 생성 알고리즘
JWT_EXPIRES_DELTA_DAYS=30
JWT_SECRET="!Qhdks00!"
JWT_ALGORITHM="HS256"

# Except
# - EXCEPT_PATH_LIST : 
# - EXCEPT_PATH_REGEX : 
EXCEPT_PATH_LIST=["/", "/openapi.json"]
EXCEPT_PATH_REGEX="^(/docs|/redoc|/api/auth)"