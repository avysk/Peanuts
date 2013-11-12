# Mac OS X application
# You need problems in problems/ for this to work
RES_DIRS=problems,images
app:
	rm -rf build/ dist/
	python setup.py py2app -r $(RES_DIRS) --no-strip
