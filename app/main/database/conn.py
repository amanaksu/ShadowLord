# -*- coding:utf-8 -*-
#
# 모듈 : DB 연동 모듈듈
# 설명 : SQLAlchemy 을 통해 연결 DB 에 대한 공통 ORM 을 생성합니다. 
#
# [개발 로그]
# 0.1.0		2021.12.08		공통 ORM 클래스 생성 (SQLAlchemy)
#

# 내장 라이브러리
import logging

# 서드파티 라이브러리
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 자체 라이브러리

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"

# 환경 변수


class SQLAlchemy:
	def __init__(self, app: FastAPI=None, **kwargs):
		self._engine = None
		self._session = None
		if app is not None:
			self.init_app(app=app, **kwargs)


	def init_app(self, app: FastAPI, **kwargs):
		"""
		DB 초기화 함수
		:param app: FastAPI 인스턴스
		:param kwargs:
		:return:
		"""
		try:
			database_url = kwargs.get("DB_URL")
			pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
			echo = kwargs.setdefault("DB_ECHO", True)

			self._engine = create_engine(
				database_url,
				echo=echo,
				pool_recycle=pool_recycle,
				pool_pre_ping=True
			)
			self._session = sessionmaker(
				autocommit=False,
				autoflush=False,
				bind=self._engine
			)

			@app.on_event("startup")
			def startup():
				self._engine.connect()
				logging.info("DB Connected.")

			@app.on_event("shutdown")
			def shutdown():
				self._session.close_all()
				self._engine.dispose()
				logging.info("DB Disconnected.")
		except:
			logging.error("DB initialization is Failed.")

		finally:
			pass

	def get_db(self):
		"""
		요청마다 DB 세션 유지 함수
		:return:
		"""
		if self._session is None:
			raise Exception("must be called. 'init_app'")

		db_session = None
		try:
			db_session = self._session()
			yield db_session
		finally:
			db_session.close()

	@property
	def session(self):
		return self.get_db

	@property
	def engine(self):
		return self._engine


db = SQLAlchemy()
Base = declarative_base()

