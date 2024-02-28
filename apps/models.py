from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, EmailField, IntegerField, BooleanField, PositiveIntegerField, \
    DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField


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

    def __str__(self):
        return self.get_full_name()


class Course(CreatedBaseModel):
    title = CharField(max_length=255)
    lesson_count = PositiveIntegerField(default=0)
    modul_count = PositiveIntegerField(default=0)
    order = IntegerField()
    task_count = PositiveIntegerField(default=0)
    type = CharField(max_length=255)
    url = URLField(max_length=255)

    def __str__(self):
        return self.title


class UserCourse(CreatedBaseModel):
    user_id = ForeignKey('apps.User', CASCADE)
    course_id = ForeignKey('apps.Course', CASCADE)
    status = CharField(default='', max_length=255)


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
    user_id = ForeignKey('apps.User', on_delete=CASCADE)

    def __str__(self):
        return self.title


class Lesson(CreatedBaseModel):
    STATUS_CHOICES = (
        ('BLOCKED', 'Blocked'),
        ('INPROG', 'In Progress'),
        ('FINISHED', 'Finished'),
    )

    order = IntegerField()
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='BLOCKED')
    title = CharField(max_length=255)
    url = URLField(max_length=255)
    video_count = PositiveIntegerField(default=0)
    module_id = ForeignKey('apps.Module', on_delete=CASCADE)
    finished = BooleanField()
    is_open = BooleanField()
    is_deleted = BooleanField()

    def __str__(self):
        return self.title


class Video(CreatedBaseModel):
    lesson_id = ForeignKey('apps.Lesson', on_delete=CASCADE)
    file = FileField(upload_to='videos/video')

    def __str__(self):
        return self.lesson_id.title


class Task(CreatedBaseModel):
    description = CharField(max_length=255)
    video_id = ForeignKey('apps.Video', on_delete=CASCADE)
    task_number = PositiveIntegerField(default=0)

    def __str__(self):
        return self.video_id.lesson_id.title


class TaskChat(CreatedBaseModel):
    description = CharField(max_length=255)
    video_id = ForeignKey('apps.Video', on_delete=CASCADE)
    user_id = ForeignKey('apps.User', on_delete=CASCADE)
    task_id = ForeignKey('apps.Task', on_delete=CASCADE)
    file = FileField(max_length=255)
    voice = FileField(max_length=255)
    text = CharField(max_length=255)


class LessonQuestion(CreatedBaseModel):
    video_id = ForeignKey('apps.Video', on_delete=CASCADE)
    user_id = ForeignKey('apps.User', on_delete=CASCADE)
    text = TextField()
    file = FileField()
    voice_message = FileField()

    def __str__(self):
        return self.video_id.lesson_id.title + ' ' + f"{self.user_id.id}"


class Payment(CreatedBaseModel):
    balance = PositiveIntegerField()
    income = BooleanField(default=False)
    expend = CharField(max_length=255)
    processed_date = DateTimeField()
    reason = CharField(max_length=255)
    user_id = ForeignKey('apps.User', on_delete=CASCADE)

    def __str__(self):
        return self.id


class Device(CreatedBaseModel):
    title = CharField(max_length=255)
    user_id = ForeignKey('apps.User', on_delete=CASCADE)

    def __str__(self):
        return self.title


class Certificate(CreatedBaseModel):
    user_id = ForeignKey('apps.User', on_delete=CASCADE)
    course_id = ForeignKey('apps.Course', on_delete=CASCADE)
    finished_at = DateField()
    qr_code = ImageField(upload_to='media/certificates_qr')

    def __str__(self):
        return self.id
