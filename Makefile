make:
	python3 manage.py makemigrations
	python3 manage.py migrate
file:
	python3 manage.py loaddata user.json
	python3 manage.py loaddata course.json
	python3 manage.py loaddata usercourse.json
	python3 manage.py loaddata module.json
	python3 manage.py loaddata lesson.json
	python3 manage.py loaddata video.json
	python3 manage.py loaddata lessonquestion.json
	python3 manage.py loaddata payment.json
	python3 manage.py loaddata task.json
	python3 manage.py loaddata taskchat.json
	python3 manage.py loaddata userlesson.json
	python3 manage.py loaddata device.json
	python3 manage.py loaddata certificate.json
	python3 manage.py loaddata usertask.json
celery:
	celery -A root worker -l info
docker:
	sudo chmod 666 /var/run/docker.sock
	docker start 90
isort_flake8:
	pip install isort
	pip install flake8

#user:
#	python3 manage.py createsuperuser
#	phone_number admin
#	password admin
