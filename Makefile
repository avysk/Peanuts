# Mac OS X application
# You need problems in problems/ for this to work
app:
	python setup.py py2app
	cp -r problems dist/Peanuts.app/Contents/Resources/
app-10.7:
	rm -rf build/ dist/
	python setup-10.7.py py2app
	cp -r problems dist/Peanuts.app/Contents/Resources/
