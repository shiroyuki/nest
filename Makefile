PYI=python
SERVICE_FLAG=

compile:
	@$(PYI) compiler.py $(SERVICE_FLAG)

install:
	mv nest /usr/local/bin
