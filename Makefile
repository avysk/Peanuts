# Mac OS X application
# You need problems in problems/ for this to work
app:
	python setup.py py2app
	cp -r problems dist/Peanuts.app/Contents/Resources/
