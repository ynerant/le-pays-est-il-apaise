generate:
	python3 generate.py
	cp static/* output/

clean:
	rm -r output/*

install:
	rsync -arvP --delete-after output/ proxy.adm.ynerant.fr:/var/www/apaisement/

all: clean generate install
