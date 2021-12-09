# -*- coding:utf-8 -*-
#
# 모듈 : DB Schema
# 설명 : DB 테이블 Schema
#
# [개발 로그]
# 0.1.1		2021.12.09		User 클래스 커스텀
# 0.1.0		2021.12.08		공통 DB 테이블 & User 클래스
#

# 내장 라이브러리
from datetime import datetime, timedelta

# 서드파티 라이브러리
from sqlalchemy import (
	Column, 
	Integer, 
	String, 
	DateTime, 
	Enum, 
	Boolean,
	func
)
from sqlalchemy.orm import Session

# 자체 라이브러리
from main.database.conn import Base

# 환경 변수

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.1"


class BaseMixin:
	id = Column(Integer, primary_key=True, index=True)
	created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
	updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def all_columns(self):
		return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

	def __hash__(self):
		return hash(self.id)

	def create(self, session: Session, auto_commit=False, **kwargs):
		"""
		테이블 데이터 적재 전용 함수
		:param session: 세션 인스턴스
		:param auto_commit: 자동 커밋 여부
		:param kwargs: 적재 할 데이터
		:return:
		"""
		for col in self.all_columns():
			col_name = col.name
			if col_name in kwargs:
				setattr(self, col_name, kwargs.get(col_name))
		session.add(self)
		session.flush()
		if auto_commit:
			session.commit()

		return self


class Users(Base, BaseMixin):
	__tablename__ = "users"
	status = Column(Enum("active", "deleted", "blocked"), default="active")
	email = Column(String(length=255), nullable=True)
	pw = Column(String(length=2000), nullable=True)
	name = Column(String(length=255), nullable=True)
	auth_type = Column(Enum("LDAP", "SSO"), nullable=True)