make:
	python3 manage.py makemigrations
	python3 manage.py migrate
file:
	python3 manage.py loaddata apps/fixtures/user.json
	python3 manage.py loaddata apps/fixtures/course.json
	python3 manage.py loaddata apps/fixtures/usercourse.json
	python3 manage.py loaddata apps/fixtures/module.json
	python3 manage.py loaddata apps/fixtures/lesson.json
	python3 manage.py loaddata apps/fixtures/video.json

	python3 manage.py loaddata apps/fixtures/lessonquestion.json

	python3 manage.py loaddata apps/fixtures/payment.json
	python3 manage.py loaddata apps/fixtures/task.json
	python3 manage.py loaddata apps/fixtures/taskchat.json
	python3 manage.py loaddata apps/fixtures/userlesson.json
	python3 manage.py loaddata apps/fixtures/device.json
	python3 manage.py loaddata certificate.json
