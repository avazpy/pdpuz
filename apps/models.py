from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db.models import CharField, TextField, IntegerField, BooleanField, PositiveIntegerField, DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField, TextChoices
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel


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
        ], unique=True,
    )
    tg_id = CharField(max_length=255, blank=False, null=False, unique=True)
    balance = PositiveIntegerField(default=0, verbose_name=_('balance'))
    bot_options = CharField(max_length=255, null=True, blank=True, verbose_name=_('bot options'))
    country_model = BooleanField(default=False, verbose_name=_('country model'))
    has_registered_bot = BooleanField(default=False)
    not_read_message_count = PositiveIntegerField(default=0)
    payme_balance = PositiveIntegerField(default=0)
    photo = ImageField(upload_to='users/images', default='users/default.jpg', verbose_name=_('Photo'))
    ticket_role = CharField(max_length=255, blank=True, null=True)
    voucher_balance = PositiveIntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def delete(self, using=None, keep_parents=False):
        self.photo.delete(save=False)
        return super().delete(using, keep_parents)


class Course(CreatedBaseModel):
    title = CharField(verbose_name=_('courses_title'), max_length=255),
    type = CharField(max_length=255, verbose_name=_('courses_type')),
    lesson_count = PositiveIntegerField(default=0, verbose_name=_('lesson_count')),
    modul_count = PositiveIntegerField(default=0, verbose_name=_('modul_count')),
    order = IntegerField(verbose_name=_('order')),
    task_count = PositiveIntegerField(default=0, verbose_name=_('task_count')),
    url = URLField(max_length=255, verbose_name=_('url')),

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")


def __str__(self):
    return self.title


class UserCourse(CreatedBaseModel):
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', _('BLOCKED')
        IN_PROG = 'in_prog', _('IN_PROG')
        FINISHED = 'finished', _('FINISHED')

    user = ForeignKey('apps.UserCourse', CASCADE)
    module = ForeignKey('apps.CourseModule', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
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


class Module(CreatedBaseModel):
    learning_type = CharField(max_length=255, verbose_name=_('learning_type'))
    title = CharField(max_length=255, verbose_name=_('title')),
    has_in_tg = CharField(max_length=255, verbose_name=_('has_in_tg')),
    lesson_count = PositiveIntegerField(default=0, verbose_name=_('lesson_count'))
    order = IntegerField(verbose_name=_('order'))
    row_num = PositiveIntegerField(default=0, verbose_name=_('row_num'))
    support_day = DateField()
    task_count = PositiveIntegerField(default=0, verbose_name=_('task_count'))
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")

    def __str__(self):
        return self.title


class CourseModule(CreatedBaseModel):
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', _('BLOCKED')
        IN_PROG = 'in_prog', _('IN_PROG')
        FINISHED = 'finished', _('FINISHED')

    status = CharField(choices=StatusChoices.choices, default=StatusChoices.BLOCKED,
                       verbose_name=_('status_CourseModule'))
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.UserCourse', CASCADE)
    module = ForeignKey('apps.Module', CASCADE)

    class Meta:
        verbose_name = _("Course Module")
        verbose_name_plural = _("User Modules")
        unique_together = ('user', 'course', 'module')


class Lesson(CreatedBaseModel):
    title = CharField(verbose_name=_('title_Lesson'), max_length=255)
    order = IntegerField(verbose_name=_('order_Lesson'))
    url = URLField(max_length=255, verbose_name=_('url_Lesson'))
    video_count = PositiveIntegerField(default=0, verbose_name=_('video_count'))
    module = ForeignKey('apps.Module', CASCADE)
    materials = FileField(null=True, blank=True, validators=[FileExtensionValidator(['pdf', 'pptx', 'ppt'])],
                          verbose_name=_('materials_Lesson'))
    is_deleted = BooleanField(verbose_name=_('is_deleted_Lesson'))

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.avi', '.mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ModuleLesson(CreatedBaseModel):
    class StatusChoices(TextChoices):
        BLOCKED = 'blocked', _('BLOCKED')
        IN_PROG = 'in_prog', _('IN_PROG')
        FINISHED = 'finished', _('FINISHED')

    status = CharField(verbose_name=_('status_UserLesson'), choices=StatusChoices.choices,
                       default=StatusChoices.BLOCKED)

    user = ForeignKey('apps.User', CASCADE, related_name='user')
    lesson = ForeignKey('apps.Lesson', CASCADE, related_name='lesson')


class Meta:
    unique_together = ('user', 'lesson')
    verbose_name = _('ModuleLesson')
    verbose_name_plural = _('ModuleLessons')


class LessonQuestion(CreatedBaseModel):
    lesson = ForeignKey('apps.ModuleLesson', CASCADE)
    user = ForeignKey('apps.UserCourse', CASCADE)
    text = TextField(verbose_name='text_LessonQuestion', null=True, blank=True)
    file = FileField(verbose_name=_('file_LessonQuestion'), null=True, blank=True)
    voice_message = FileField(verbose_name=_('voice_mes_LessonQuestion'), null=True, blank=True)

    def __str__(self):
        return self.lesson.title + ' ' + f"{self.user.id}"

    class Meta:
        verbose_name = _('LessonQuestion')
        verbose_name_plural = _('LessonQuestions')


class Video(CreatedBaseModel):
    title = CharField(verbose_name=_('title'), max_length=255),
    description = CharField(verbose_name=_('description'), max_length=255),
    media_code = CharField(verbose_name=_('media code'), max_length=255)

    lesson = ForeignKey('apps.Lesson', CASCADE)
    file = FileField(verbose_name=_('file_video'), upload_to='videos/video')
    is_youtube = BooleanField(verbose_name=_('is_youtube'), default=False)
    media_url = CharField(verbose_name=_('media_url'), max_length=255)
    order = PositiveIntegerField(verbose_name=_('order'))

    def __str__(self):
        return self.lesson.title


class Task(CreatedBaseModel):
    title = CharField(verbose_name=_('title'), max_length=255),
    description = CharField(verbose_name=_('description'), max_length=255),
    status = CharField(verbose_name=_('status'), max_length=255),
    user_task_list = CharField(verbose_name=_('user_task_list'), max_length=255)
    lesson = ForeignKey('apps.Lesson', CASCADE)
    task_number = PositiveIntegerField(verbose_name=_('task number'), default=0)
    lastTime = DateTimeField(verbose_name=_('lastTime'))
    order = IntegerField(verbose_name=_('order'))
    priority = PositiveIntegerField(verbose_name=_('priority'), default=0)
    mustComplete = BooleanField()
    files = CharField(verbose_name=_('files'), max_length=255)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Task')

    def __str__(self):
        return self.lesson.title


class UserTask(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    task = ForeignKey('apps.Task', CASCADE)
    finished = BooleanField(verbose_name=_('finished'), default=False)

    class Meta:
        unique_together = ('user', 'task')
        verbose_name = _('UserTask')
        verbose_name_plural = _('UserTasks')


class TaskChat(CreatedBaseModel):
    text = CharField(verbose_name=_('text'), max_length=255),
    user = ForeignKey('apps.User', CASCADE)
    task = ForeignKey('apps.Task', CASCADE)
    file = FileField(verbose_name=_('file'), max_length=255)
    voice = FileField(verbose_name=_('voice'), max_length=255)

    class Meta:
        verbose_name = _('TaskChat')
        verbose_name_plural = _('TaskChat')


class Payment(CreatedBaseModel):
    reason = CharField(verbose_name=_('reason'), max_length=255)
    expend = CharField(verbose_name=_('expend'), max_length=255)
    balance = PositiveIntegerField(verbose_name=_('balance'))
    income = BooleanField(verbose_name=_('income'), default=False)
    processed_date = DateTimeField(verbose_name=_("processed date"))
    user = ForeignKey('apps.User', CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Device(CreatedBaseModel):
    title = CharField(verbose_name=_('title_devise'), max_length=255),
    user = ForeignKey('apps.User', CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')


class Certificate(CreatedBaseModel):
    user = ForeignKey('apps.User', CASCADE)
    course = ForeignKey('apps.Course', CASCADE)
    finished_at = DateField(verbose_name=_('finished_at'))
    qr_code = ImageField(verbose_name=_('qr_code'), upload_to='media/certificates_qr')

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')


class DeletedUser(CreatedBaseModel):
    phone_number = CharField(max_length=13)
    username = CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Deleted User : {self.phone_number}"
