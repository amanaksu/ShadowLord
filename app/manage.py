# -*- coding:utf-8 -*-
#
# 모듈 : 메일 실행 모듈
# 설명 : 개발|제품 모드 또는 unittest 모드를 선택해 실행
#
# [개발 로그]
# 0.1.2		2021.12.08		help 별도 함수로 분리
# 0.1.1		2021.12.08		오류 출력 방식 변경 (traceback -> logging)
# 0.1.0		2021.12.07		동작별 실행 함수 생성 (run, test)
#

# 내장 라이브러리
import logging
import sys
import unittest

# 서드파티 라이브러리
import uvicorn

# 자체 라이브러리
from main import create_app
from main.common import config

# 전역 변수
__author__ = "amanaksu@gmail.com"
__version__ = "0.1.2"

# 환경 변수

app = create_app()

def run():
	try:
		conf_dict = config.to_dict()
		uvicorn.run(
			"manage:app",
			host=conf_dict.get("API_ENV_SERVER"),
			port=conf_dict.get("API_ENV_PORT"),
			reload=conf_dict.get("PROJ_RELOAD")
		)
	except:
		logging.error("'run' mode is Failed.")

	finally:
		pass

def test():
	"""
	unittest 실행행
	"""
	retVal = 1
	try:
		tests = unittest.TestLoader().discover("test", pattern="test*.py")
		result = unittest.TextTestRunner(verbosity=2).run(tests)
		if result.wasSuccessful():
			retVal = 0

	except:
		logging.error("'test' mode is failed.")

	finally:
		return retVal

def help():
	print("""
[Usage] 
python {FILE} [run|test]
    run     Run in 'Dev'elopment or 'Prod'uction mode.
    test    Run in unittest mode.
""".format(FILE=__file__))


if __name__ == "__main__":
	try:
		args = sys.argv[1].lower()
		if args == "run":		run()
		elif args == "test":	test()
		else:					help()
	finally:
		pass
