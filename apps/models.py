from tkinter import PhotoImage

from django.db.models import CharField, Model, EmailField, IntegerField, BooleanField, PositiveIntegerField, DateField, \
    FileField, URLField, ImageField, TextField


class Users(Model):
    firstname = CharField(max_length=255)
    lastname = CharField(max_length=255)
    email = EmailField(max_length=255)
    phone_number = IntegerField()
    balance = IntegerField()
    # bot_options = IntegerField()
    # country_model = IntegerField()
    has_registered_bot = BooleanField(default=False)
    not_read_message_count = IntegerField()
    payme_balance = PositiveIntegerField(default=0)
    photo = ImageField(upload_to='users/images')
    # ticket_role = CharField(max_length=255)
    vaucher_balans = IntegerField()


class UsersCourses(Model):
    user_id = IntegerField()
    course_id = IntegerField()


class Courses(Model):
    title = CharField(max_length=255)
    lesson_count = IntegerField()
    modul_count = IntegerField()
    order = IntegerField()
    # status = CharField(max_length=255)
    task_count = IntegerField()
    url = URLField(max_length=255)


class Modules(Model):
    has_in_tg = CharField(max_length=255)
    learning_type = CharField(max_length=255)
    lesson_count = IntegerField()
    order = IntegerField()
    row_num = IntegerField()
    # status = CharField(max_length=255)
    support_day = DateField()
    task_count = IntegerField()
    title = CharField(max_length=255)
    user_id = IntegerField()


class Tasks(Model):
    description = CharField(max_length=255)
    video_id = IntegerField()
    task_number = IntegerField()


class TasksCourses(Model):
    description = CharField(max_length=255)
    video_id = IntegerField()
    task_number = IntegerField()


class Video(Model):
    lesson_id = IntegerField()
    file = FileField(upload_to='videos/video')


class LessonQuestions(Model):
    video_id = IntegerField()
    user_id = IntegerField()
    text = TextField()
    file = FileField()
    voice_message = FileField()


class Lessons(Model):
    order = IntegerField()
    # status = CharField(max_length=255)
    title = CharField(max_length=255)
    url = URLField(max_length=255)
    video_count = IntegerField()
    module_id = IntegerField()
    finished = BooleanField()
    is_open = BooleanField()






