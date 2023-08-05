release-pypi:
	test -n "$(VERSION)"
	python setup.py sdist
	twine upload dist/python-telegram-client-$(VERSION).tar.gz
