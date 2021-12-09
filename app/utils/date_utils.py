# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		XXXX.XX.XX		ProtoType
#

# 내장 라이브러리
from datetime import datetime, date, timedelta

# 서드파티 라이브러리

# 자체 라이브러리

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"


class D:
	def __init__(self, *args):
		self.utc_now = datetime.utcnow()	
		self.timedelta = 0

	@classmethod
	def datetime(cls, diff: int=0) -> datetime:
		return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

	@classmethod
	def date(cls, diff: int=0) -> date:
		return cls.datetime(diff=diff).date()

	@classmethod
	def date_num(cls, diff: int=0) -> int:
		return int(cls.date(diff=diff).strftime("%Y%m%d"))