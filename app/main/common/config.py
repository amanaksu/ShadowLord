# -*- coding:utf-8 -*-
#
# 모듈 : 
# 설명 : 
#
# [개발 로그]
# 0.1.0		2021-12-17		동작 설정 클래스 추가, 환경 변수 반환 함수 추가 
#

# 내장 라이브러리
from dataclasses import dataclass, asdict, field
from typing import List
import os


# 서드파티 라이브러리

# 자체 라이브러리

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.0"


# 환경 변수

basedir = os.path.abspath(os.path.dirname(__file__))

@dataclass
class Config:
	"""
	공통 설정
	"""
	# 공통 적용
	BASE_DIR = basedir
	DB_POOL_RECYCLE: int = 900		# Seconds
	DB_ECHO: bool = True

	# TRUSTED_HOSTS: List[str] = field(default_factory=list)
	# ALLOWED_HOSTS: List[str] = field(default_factory=list)

@dataclass
class DevelopmentConfig(Config):
	"""
	개발 환경 설정
	"""
	API_ENV_SERVER: str = "127.0.0.1"
	API_ENV_PORT: int = 8000
	DB_URL: str = "mysql+pymysql://travis:3584ksu!Q@localhost/shadowLord?charset=utf8mb4"
	PROJ_RELOAD: bool = True
	
	TRUSTED_HOSTS: List[str] = ["*"]

	

@dataclass
class ProductionConfig(Config):
	"""
	운영 환경 설정
	"""
	PROJ_RELOAD: bool = False
	

def to_instance():
	"""
	환경 변수 (instance) 불러오기
	:return:
	"""
	config = dict(
		dev=DevelopmentConfig,
		prod=ProductionConfig
	)
	return config.get(os.getenv("RUN_ENV", "dev"))()

def to_dict():
	"""
	환경 변수 (dict) 불러오기 (convert instance to dict)
	:return:
	"""
	return asdict(to_instance())