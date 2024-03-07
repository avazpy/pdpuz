from unittest import TestCase

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, EmailField, IntegerField, BooleanField, PositiveIntegerField, \
    DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField
from django.db import models

class CreatedBaseModel(Model):
    update_at = DateTimeField(auto_now=True, null=True)
    created_at = DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = CharField(default='', max_length=255, null=False, unique=True)
    password = CharField(default='', max_length=255, null=False)
    phone_number = CharField(max_length=13, null=True, blank=True)
    balance = PositiveIntegerField(default=0)
    bot_options = CharField(max_length=255, null=True, blank=True)
    country_model = BooleanField(default=False)
    has_registered_bot = BooleanField(default=False)
    not_read_message_count = PositiveIntegerField(default=0)
    payme_balance = PositiveIntegerField(default=0)
    photo = ImageField(upload_to='users/images', default='users/default.jpg')
    ticket_role = CharField(max_length=255, blank=True, null=True)
    voucher_balance = PositiveIntegerField(default=0)



class Course(CreatedBaseModel):
    title = CharField(max_length=255)
    lesson_count = PositiveIntegerField(default=0)
    modul_count = PositiveIntegerField(default=0)
    order = IntegerField()
    task_count = PositiveIntegerField(default=0)
    type = CharField(max_length=255)
    url = URLField(max_length=255)


class UserCourse(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    status = CharField(default='', max_length=255)

    class Meta:
        unique_together = ('user', 'course')

class Module(CreatedBaseModel):
    has_in_tg = CharField(max_length=255)
    learning_type = CharField(max_length=255)
    lesson_count = PositiveIntegerField(default=0)
    order = IntegerField()
    row_num = PositiveIntegerField(default=0)
    status = CharField(max_length=255)
    support_day = DateField()
    task_count = PositiveIntegerField(default=0)
    title = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)



class Lesson(CreatedBaseModel):
    STATUS_CHOICES = [
        ('blocked', 'BLOCKED'),
        ('inprog', 'INPROG'),
        ('finished', 'FINISHED'),
    ]

    order = IntegerField()
    status = CharField(choices=STATUS_CHOICES, default='BLOCKED')
    title = CharField(max_length=255)
    url = URLField(max_length=255)
    video_count = PositiveIntegerField(default=0)
    module = ForeignKey('apps.Module', CASCADE)
    finished = BooleanField()
    is_open = BooleanField()
    is_deleted = BooleanField()


class Video(CreatedBaseModel):
    lesson = ForeignKey('apps.Lesson', CASCADE)
    file = FileField(upload_to='videos/video')


class Task(CreatedBaseModel):
    description = CharField(max_length=255)
    video = ForeignKey('apps.Video', CASCADE)
    task_number = PositiveIntegerField(default=0)


class TaskChat(CreatedBaseModel):
    description = CharField(max_length=255)
    video = ForeignKey('apps.Video', CASCADE)
    user = ForeignKey('apps.User', CASCADE)
    task = ForeignKey('apps.Task', CASCADE)
    file = FileField(max_length=255)
    voice = FileField(max_length=255)
    text = CharField(max_length=255)


class LessonQuestion(CreatedBaseModel):
    video = ForeignKey('apps.Video', CASCADE)
    user = ForeignKey('apps.User', CASCADE)
    text = TextField()
    file = FileField()
    voice_message = FileField()


class Payment(CreatedBaseModel):
    balance = PositiveIntegerField()
    income = BooleanField(default=False)
    expend = CharField(max_length=255)
    processed_date = DateTimeField()
    reason = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)



class Device(CreatedBaseModel):
    title = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)



class Certificate(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    finished_at = DateField()
    qr_code = ImageField(upload_to='media/certificates_qr')



class UserLesson(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    lesson = ForeignKey('apps.Lesson', CASCADE)
    is_open = BooleanField()
    is_finished = BooleanField()

    class Meta:
        unique_together = ('user', 'lesson')


class MyModel(models.Model):
    userId = models.IntegerField()
    title = models.CharField(max_length=255)




