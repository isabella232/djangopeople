proj = djangopeople

makemessages:
	cd $(proj) && envdir ../env django-admin makemessages -a

compilemessages:
	cd $(proj) && envdir ../env django-admin compilemessages

txpush:
	tx push -s

txpull:
	tx pull -a --minimum-perc=100

initialdeploy:
	git push heroku master
	heroku run django-admin migrate --noinput
	heroku run django-admin fix_counts

deploy:
	git push heroku master
