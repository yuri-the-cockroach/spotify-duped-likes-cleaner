##
# Project Title
#
# @file
# @version 0.1

all:
	python main.py

requirements.txt:
	pip freeze > requirements.txt

# end
