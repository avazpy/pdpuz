import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db.models import (CASCADE, BooleanField, CharField, DateField,
                              DateTimeField, FileField, ForeignKey, ImageField,
                              IntegerField, ManyToManyField, Model,
                              PositiveIntegerField, SlugField, TextChoices,
                              TextField, URLField, UUIDField, )
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel

from apps.managers import CustomUserManager
from django.db import models


class CreatedBaseModel(Model):
    update_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class UserType(TextChoices):
        ADMIN = 'admin', _('Admin')
        TEACHER = 'teacher', _('Teacher')
        STUDENT = 'student', _('Student')
        ASSISTANT = 'assistant', _('Assistant')

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = CharField(verbose_name=_('user_type'), max_length=50, choices=UserType.choices, default=UserType.STUDENT)
    phone_number = CharField(validators=[RegexValidator(
        regex=r'^\d{9}$',
        message="Phone number must be entered in the format: '9999998'."        "Up to 12 digits allowed.")],
        max_length=20, unique=True)
    username = CharField(max_length=255, unique=False)
    tg_id = CharField(max_length=255, unique=True, blank=False, null=True)
    balance = PositiveIntegerField(default=0, verbose_name=_('balance'))
    bot_options = CharField(max_length=255, null=True, blank=True, verbose_name=_('bot options'))
    has_registered_bot = BooleanField(default=False)
    not_read_message_count = PositiveIntegerField(default=0)
    payme_balance = PositiveIntegerField(default=0)
    photo = ImageField(upload_to='users/images', default='users/default.jpg', verbose_name=_('Photo'))
    courses = ManyToManyField('apps.Course', through='apps.UserCourse', related_name='+', verbose_name=_('courses'))

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def delete(self, using=None, keep_parents=False):
        self.photo.delete(save=False)
        return super().delete(using, keep_parents)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Customer(Model):
    pass
    # def post(self, request):
    #     phone_number = request.data.get('phone_number')
    #     password = request.data.get('password')
    #
    #     user = User.objects.filter(phone_number=phone_number).first()
    #
    #     if user and user.check_password(password):
    #         user_agent = get_user_agent(request)
    #         title = (f"{user_agent.os.family}, {user_agent.browser.family}, {user_agent.browser.version_string}, "
    #                  f"{'Mobile' if user_agent.is_mobile else 'Desktop'}")
    #
    #         device, created = Device.objects.get_or_create(user_id=user.id, title=title)
    #         Device.objects.create(title=device,user=request.user)
    #         print(device)
    #
    #         return Response({"message": f"{user.phone_number} you have logged in successfully!"}
    #                         status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_400_BAD_REQUEST)


class Course(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(max_length=255, verbose_name=_('courses_title'))
    lesson_count = PositiveIntegerField(default=0, verbose_name=_('lesson_count'))
    modul_count = PositiveIntegerField(default=0, verbose_name=_('modul_count'))
    order = IntegerField(verbose_name=_('order'))
    task_count = PositiveIntegerField(default=0, verbose_name=_('task_count'))
    url = URLField(max_length=255, verbose_name=_('url'))

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title


class UserCourse(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class StatusChoices(TextChoices):
        BLOCKED = "blocked", _('Blocked')
        IN_PROG = "in_prog", _('In_prog')
        FINISHED = "finished", _('Finished')

    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_userCourse'))
    course = ForeignKey('apps.Course', CASCADE, verbose_name=_('course_userCourse'))
    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED, verbose_name=_('status'))

    class Meta:
        verbose_name = _("User Course")
        verbose_name_plural = _("User Courses")
        unique_together = ('user', 'course')

    @property
    def support_day(self):
        purchase_date = self.created_at

        if purchase_date:
            return purchase_date + timedelta(days=45)
        else:
            return None

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course.title)
        super(UserCourse, self).save(*args, **kwargs)


class Module(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_type = CharField(max_length=255, verbose_name=_('learning_type'))
    title = CharField(max_length=255, verbose_name=_('module_title'))
    has_in_tg = CharField(max_length=255, verbose_name=_('has_in_tg'))
    lesson_count = PositiveIntegerField(default=0, verbose_name=_('lesson_count'))
    order = IntegerField(verbose_name=_('order'))
    row_num = PositiveIntegerField(default=0, verbose_name=_('row_num'))
    support_day = DateField()
    task_count = PositiveIntegerField(default=0, verbose_name=_('task_count'))
    course = ForeignKey('apps.Course', CASCADE, verbose_name=_('course_module'))
    slug = SlugField(max_length=100, editable=False)  # add slug  in  fixture

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Module, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")

    def __str__(self):
        return self.title


class UserModule(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class StatusChoices(TextChoices):
        BLOCKED = "blocked", _('Blocked')
        IN_PROG = "in_prog", _('In_prog')
        FINISHED = "finished", _('Finished')

    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED,
                       verbose_name=_('User_Module'))
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_User_Module'))
    module = ForeignKey('apps.Module', CASCADE, verbose_name=_('module_Course_Module'))

    class Meta:
        verbose_name = _("Course Module")
        verbose_name_plural = _("User Modules")
        unique_together = ('user', 'module')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.module.title)
        super(UserModule, self).save(*args, **kwargs)


class Lesson(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(verbose_name=_('title_Lesson'), max_length=255)
    order = IntegerField(verbose_name=_('order_Lesson'))
    url = URLField(max_length=255, verbose_name=_('url_Lesson'))
    video_count = PositiveIntegerField(default=0, verbose_name=_('video_lesson'))
    module = ForeignKey('apps.Module', CASCADE, verbose_name=_('module_lesson'))
    materials = FileField(null=True, blank=True, validators=[FileExtensionValidator(['pdf', 'pptx', 'ppt'])],
                          verbose_name=_('materials_Lesson'))
    is_deleted = BooleanField(verbose_name=_('is_deleted_Lesson'))
    slug = SlugField(max_length=100, editable=False)  # add slug  in  fixture

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return self.title


def validate_file_extension(value):
    import os

    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.avi', '.mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UserLesson(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class StatusChoices(TextChoices):
        BLOCKED = "blocked", _('Blocked')
        IN_PROG = "in_prog", _('In_prog')
        FINISHED = "finished", _('Finished')

    status = CharField(verbose_name=_('status_UserLesson'), choices=StatusChoices.choices,
                       default=StatusChoices.BLOCKED)

    user = ForeignKey('apps.User', CASCADE, verbose_name='user_moduleLesson')
    lesson = ForeignKey('apps.Lesson', CASCADE, verbose_name='lesson_moduleLesson')

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = _('UserLesson')
        verbose_name_plural = _('UserLessons')


class LessonQuestion(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = ForeignKey('apps.Lesson', CASCADE, verbose_name=_('lesson_LessonQuestion'))
    text = TextField(verbose_name=_('text_LessonQuestion'), null=True, blank=True)
    file = FileField(verbose_name=_('file_LessonQuestion'), null=True, blank=True)
    voice_message = FileField(verbose_name=_('voice_mes_LessonQuestion'), null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('LessonQuestion')
        verbose_name_plural = _('LessonQuestions')


class Video(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(verbose_name=_('title'), max_length=255)
    description = CharField(verbose_name=_('description'), max_length=255)
    media_code = CharField(verbose_name=_('media code'), max_length=255)
    lesson = ForeignKey('apps.Lesson', CASCADE, verbose_name=_('lesson_video'))
    file = FileField(verbose_name=_('file_video'), upload_to='videos/video')
    is_youtube = BooleanField(verbose_name=_('is_youtube'), default=False)
    media_url = CharField(verbose_name=_('media_url'), max_length=255)
    order = PositiveIntegerField(verbose_name=_('order'))

    def __str__(self):
        return self.lesson.title

    def save(self, *args, **kwargs):
        # New video being added
        if not self.pk:
            self.lesson.video_count = models.F('video_count') + 1
            self.lesson.save(update_fields=['video_count'])
        super().save(*args, **kwargs)


class Task(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(verbose_name=_('title'), max_length=255)
    description = CharField(verbose_name=_('description'), max_length=255)
    status = CharField(verbose_name=_('status'), max_length=255)
    user_task_list = CharField(verbose_name=_('user_task_list'), max_length=255)
    lesson = ForeignKey('apps.Lesson', CASCADE, verbose_name=_('lesson_task'))
    task_number = PositiveIntegerField(verbose_name=_('task number'), default=0)
    last_time = DateTimeField(verbose_name=_('last_time'))
    order = IntegerField(verbose_name=_('order'))
    priority = PositiveIntegerField(verbose_name=_('priority'), default=0)
    must_complete = BooleanField(default=False, )
    files = FileField(verbose_name=_('files'), null=True, blank=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Task')

    def __str__(self):
        return self.title


class UserTask(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_userTask'))
    task = ForeignKey('apps.Task', CASCADE, verbose_name=_('task_user_task'))
    finished = BooleanField(verbose_name=_('finished'), default=False)

    class Meta:
        unique_together = ('user', 'task')
        verbose_name = _('UserTask')
        verbose_name_plural = _('UserTasks')


class TaskChat(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = CharField(verbose_name=_('text'), max_length=255)
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_taskChat'))
    task = ForeignKey('apps.Task', CASCADE, verbose_name=_('task_taskChat'))
    file = FileField(verbose_name=_('file'), max_length=255)
    voice = FileField(verbose_name=_('voice'), max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('TaskChat')
        verbose_name_plural = _('TaskChat')


class Payment(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason = CharField(verbose_name=_('reason'), max_length=255)
    expend = CharField(verbose_name=_('expend'), max_length=255)
    balance = PositiveIntegerField(verbose_name=_('balance'))
    income = BooleanField(verbose_name=_('income'), default=False)
    processed_date = DateTimeField(verbose_name=_("processed date"))
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_payment'))

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Device(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(verbose_name=_('title_device'), max_length=255)
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_device'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')


class Certificate(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey('apps.User', CASCADE, verbose_name=_('user_certificate'))
    course = ForeignKey('apps.Course', CASCADE, verbose_name=_('course_certificate'))
    finished_at = DateField(verbose_name=_('finished_at'))
    qr_code = ImageField(verbose_name=_('qr_code'), upload_to='media/certificates_qr')

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')


class DeletedUser(CreatedBaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = CharField(max_length=13, verbose_name=_('phone_number'))
    username = CharField(max_length=255, null=True, blank=True, verbose_name=_('username'))

    def __str__(self):
        return f"Deleted User : {self.phone_number}"

    class Meta:
        verbose_name = _('Deleted User')
        verbose_name_plural = _('Deleted Users')
