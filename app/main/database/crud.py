# -*- coding:utf-8 -*-
#
# 모듈 : DB CURD 모듈
# 설명 : 데이터베이스에 접근해 CRUD (Create, Read, Update, Delete) 동작을 수행하는 함수 모음
#
# [개발 로그]
# 0.1.0		2021.12.08		DB CRUD 함수 생성 (Create)
#

# 내장 라이브러리

# 서드파티 라이브러리
from sqlalchemy.orm import Session

# 자체 라이브러리
from main.database.conn import Base

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"


async def create(session: Session, obj: Base, auto_commit=False, **kwargs):
	"""
	테이블 데이터 적재 전용 함수
	:param	session: 세션 인스턴스
	:param	obj: 데이터 모델 인스턴스 (ex: User())
	:param	auto_commit: 자동 커밋 여부
	:param	kwargs: 적재할 데이터
	:return	obj:
	"""
	for col in obj.all_columns():
		col_name = col.name
		if col_name in kwargs:
			setattr(obj, col_name, kwargs.get(col_name))

	session.add(obj)
	session.flush()
	if auto_commit:
		session.commit()

	return obj