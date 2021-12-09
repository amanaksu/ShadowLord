# -*- coding:utf-8 -*-
#
# 모듈 : 실행 환경변수 모듈
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.17		환경변수 추가 (RUN_ENV)
#

# 내장 라이브러리

# 서드파티 라이브러리

# 자체 라이브러리

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

# 환경 변수

# 실행모드
# - dev : 개발모드  (development mode)
# - prod : 제품모드 (release mode)
RUN_ENV			= "dev"		

# JWT
JWT_EXPIRES_DELTA_DAYS=30
JWT_SECRET="!Qhdks00!"
JWT_ALGORITHM="HS256"