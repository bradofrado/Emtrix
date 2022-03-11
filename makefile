
# makefile for project 3 example tests

numbers:=1

tests:=tests

.SILENT: all run

all: run
	@rm $(tests)/out.txt

run:
	for number in $(numbers) ; \
	do \
		echo "Running input $$number" ; \
		python main.py $(tests)/in$$number.txt > $(tests)/out.txt ; \
		diff $(tests)/out$$number.txt $(tests)/out.txt || (echo "diff failed on test $$number \n") ; \
	done