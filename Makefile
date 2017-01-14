all: zip

zip: dependencies
	rm -rf unoffical_upper_room.zip
	zip -9 -r unoffical_upper_room.zip unoffical_upper_room.py
	(cd virtual-env/lib/python2.7/site-packages; zip -9 -r ../../../../unoffical_upper_room.zip *)

dependencies: virtual-env beautiful-soup

virtual-env:
	virtualenv virtual-env

beautiful-soup: ./virtual-env/lib/python2.7/site-packages/BeautifulSoup.py

virtual-env/lib/python2.7/site-packages/BeautifulSoup.py:
	./virtual-env/bin/pip install BeautifulSoup

update: dependencies
	zip -9 -r unoffical_upper_room.zip unoffical_upper_room.py

clean:
	rm -rf *.zip virtual-env
