# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021.12.07		서버 정상 동작 확인 함수
#

# 내장 라이브러리
import requests

# 서드파티 라이브러리

# 자체 라이브러리

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

# 환경 변수

resp = requests.get("http://127.0.0.1:8000")
print(resp.text)