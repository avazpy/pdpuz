from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db.models import CharField, TextField, IntegerField, BooleanField, PositiveIntegerField, \
    DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField


class CreatedBaseModel(Model):
    update_at = DateTimeField(auto_now=True, null=True)
    created_at = DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    phone_number = CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,13}$',
                message="Phone number must be entered in the format '+998'. Up to 13 digits allowed."
            ),
        ], unique=True
    )
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

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


class Video(CreatedBaseModel):
    lesson = ForeignKey('apps.Lesson', CASCADE)
    file = FileField(upload_to='videos/video')

    def __str__(self):
        return self.lesson.title


class Task(CreatedBaseModel):
    description = CharField(max_length=255)
    video = ForeignKey('apps.Video', CASCADE)
    task_number = PositiveIntegerField(default=0)
    last_time = DateTimeField()
    order = IntegerField()
    priority = PositiveIntegerField(default=0)
    title = CharField(max_length=255)
    must_complete = BooleanField()
    status = CharField()
    files = CharField(max_length=255)
    user_task_list = CharField(max_length=255)

    def __str__(self):
        return self.video.lesson.title


class UserTask(CreatedBaseModel):
    status = IntegerField()
    user = ForeignKey('apps.User', CASCADE)
    task = ForeignKey('apps.Task', CASCADE)
    is_open = BooleanField()
    finished = BooleanField()

    class Meta:
        unique_together = ('user', 'task')


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

    def __str__(self):
        return self.video.lesson.title + ' ' + f"{self.user.id}"


class Payment(CreatedBaseModel):
    balance = PositiveIntegerField()
    income = BooleanField(default=False)
    expend = CharField(max_length=255)
    processed_date = DateTimeField()
    reason = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)

    def __str__(self):
        return self.id


class Device(CreatedBaseModel):
    title = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)

    def __str__(self):
        return self.title


class Certificate(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    finished_at = DateField()
    qr_code = ImageField(upload_to='media/certificates_qr')

    def __str__(self):
        return self.id


class UserLesson(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    lesson = ForeignKey('apps.Lesson', CASCADE)
    is_open = BooleanField()
    is_finished = BooleanField()

    class Meta:
        unique_together = ('user', 'lesson')
