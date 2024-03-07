from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, TextField, IntegerField, BooleanField, PositiveIntegerField, \
    DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField, TextChoices


class CreatedBaseModel(Model):
    update_at = DateTimeField(auto_now=True, null=True)
    created_at = DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    phone_number = CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,13}$',
                message="Phone number must be entered in the format '+998'. Up to 13 digits allowed."
            ),
        ],
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
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', 'BLOCKED'
        INPROG = 'inprog', 'INPROG'
        FINISHED = 'finished', 'FINISHED'

    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED)

    class Meta:
        unique_together = ('user', 'course')


class Module(CreatedBaseModel):
    has_in_tg = CharField(max_length=255)
    learning_type = CharField(max_length=255)
    lesson_count = PositiveIntegerField(default=0)
    order = IntegerField()
    row_num = PositiveIntegerField(default=0)
    support_day = DateField()
    task_count = PositiveIntegerField(default=0)
    title = CharField(max_length=255)
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)

    def __str__(self):
        return self.title


class UserModule(CreatedBaseModel):
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', 'BLOCKED'
        INPROG = 'inprog', 'INPROG'
        FINISHED = 'finished', 'FINISHED'

    user = ForeignKey('apps.User', CASCADE)
    module = ForeignKey('apps.Module', CASCADE)
    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED)

    class Meta:
        unique_together = ('user', 'module')


class Lesson(CreatedBaseModel):
    order = IntegerField()
    title = CharField(max_length=255)
    url = URLField(max_length=255)
    video_count = PositiveIntegerField(default=0)
    module = ForeignKey('apps.Module', CASCADE)
    is_deleted = BooleanField()

    def __str__(self):
        return self.title


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.avi', '.mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UserLesson(CreatedBaseModel):
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', 'BLOCKED'
        IN_PROG = 'inprog', 'INPROG'
        FINISHED = 'finished', 'FINISHED'

    user = ForeignKey('apps.User', CASCADE)
    lesson = ForeignKey('apps.Lesson', CASCADE)
    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED)

    class Meta:
        unique_together = ('user', 'lesson')


class LessonQuestion(CreatedBaseModel):
    video = ForeignKey('apps.Video', CASCADE)
    user = ForeignKey('apps.User', CASCADE)
    text = TextField()
    file = FileField()
    voice_message = FileField()

    def __str__(self):
        return self.video.lesson.title + ' ' + f"{self.user.id}"


class Video(CreatedBaseModel):
    lesson = ForeignKey('apps.Lesson', CASCADE)
    file = FileField(upload_to='videos/video', validators=[validate_file_extension])

    def __str__(self):
        return self.lesson.title


class Task(CreatedBaseModel):
    description = CharField(max_length=255)
    lesson = ForeignKey('apps.Lesson', CASCADE)
    task_number = PositiveIntegerField(default=0)
    lastTime = DateTimeField()
    order = IntegerField()
    priority = PositiveIntegerField(default=0)
    title = CharField(max_length=255)
    mustComplete = BooleanField()
    status = CharField()
    files = CharField(max_length=255)
    user_task_list = CharField(max_length=255)

    def __str__(self):
        return self.lesson.title


class UserTask(CreatedBaseModel):
    status = IntegerField()
    user = ForeignKey('apps.User', CASCADE)
    task = ForeignKey('apps.Task', CASCADE)
    is_open = BooleanField(default=True)
    finished = BooleanField(default=False)

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


# class LessonQuestion(CreatedBaseModel):
#     video = ForeignKey('apps.Video', CASCADE)
#     user = ForeignKey('apps.User', CASCADE)
#     text = TextField()
#     file = FileField(null=True,
#                      blank=True,
#                      validators=[FileExtensionValidator(['pdf'])])
#
#     voice_message = FileField()
#
#     def __str__(self):
#         return self.video.lesson.title + ' ' + f"{self.user.id}"


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

    def __str__(self):
        return self.title


class Certificate(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    finished_at = DateField()
    qr_code = ImageField(upload_to='certificate/certificates_qr')
