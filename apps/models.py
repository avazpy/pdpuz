from django.db.models import CharField, TextField, EmailField, IntegerField, BooleanField, PositiveIntegerField, \
    DateField, \
    FileField, URLField, ImageField, Model, ForeignKey, CASCADE, DateTimeField


class CreatedBaseModel(Model):
    update_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Users(CreatedBaseModel):
    firstname = CharField(max_length=255)
    lastname = CharField(max_length=255)
    email = EmailField(max_length=255, default=None)
    phone_number = IntegerField()
    balance = PositiveIntegerField()
    bot_options = CharField(max_length=255, default=None)
    country_model = BooleanField(default=False)
    has_registered_bot = BooleanField(default=False)
    not_read_message_count = IntegerField()
    payme_balance = PositiveIntegerField(default=0)
    photo = ImageField(upload_to='users/images', default='users/default.jpg')
    ticket_role = CharField(max_length=255, default=None)
    voucher_balance = IntegerField()


class Courses(CreatedBaseModel):
    title = CharField(max_length=255)
    lesson_count = IntegerField()
    modul_count = IntegerField()
    order = IntegerField()
    task_count = IntegerField()
    type = CharField(max_length=255)
    url = URLField(max_length=255)


class UsersCourses(CreatedBaseModel):
    user_id = ForeignKey('apps.Users', CASCADE)
    course_id = ForeignKey('apps.Courses', CASCADE)


class Modules(CreatedBaseModel):
    has_in_tg = CharField(max_length=255)
    learning_type = CharField(max_length=255)
    lesson_count = IntegerField()
    order = IntegerField()
    row_num = IntegerField()
    status = CharField(max_length=255)
    support_day = DateField()
    task_count = IntegerField()
    title = CharField(max_length=255)
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)


class Lessons(CreatedBaseModel):
    order = IntegerField()
    status = CharField(max_length=255)
    title = CharField(max_length=255)
    url = URLField(max_length=255)
    video_count = IntegerField()
    module_id = ForeignKey('apps.Modules', on_delete=CASCADE)
    finished = BooleanField()
    is_open = BooleanField()
    is_deleted = BooleanField()


class Videos(CreatedBaseModel):
    lesson_id = ForeignKey('apps.Lessons', on_delete=CASCADE)
    file = FileField(upload_to='videos/video')


class Tasks(CreatedBaseModel):
    description = CharField(max_length=255)
    video_id = ForeignKey('apps.Videos', on_delete=CASCADE)
    task_number = IntegerField()


class TasksChat(CreatedBaseModel):
    description = CharField(max_length=255)
    video_id = ForeignKey('apps.Videos', on_delete=CASCADE)
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)
    task_id = ForeignKey('apps.Tasks', on_delete=CASCADE)
    file = FileField(max_length=255)
    voice = FileField(max_length=255)
    text = CharField(max_length=255)


class LessonQuestions(CreatedBaseModel):
    video_id = ForeignKey('apps.Videos', on_delete=CASCADE)
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)
    text = TextField()
    file = FileField()
    voice_message = FileField()


class Payments(CreatedBaseModel):
    balance = PositiveIntegerField()
    income = BooleanField(default=False)
    expend = CharField(max_length=255)
    processed_date = DateField()
    reason = CharField(max_length=255)
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)


class Devices(CreatedBaseModel):
    title = CharField(max_length=255)
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)


class Certificates(CreatedBaseModel):
    user_id = ForeignKey('apps.Users', on_delete=CASCADE)
    course_id = ForeignKey('apps.Courses', on_delete=CASCADE)
    finished_at = DateField()
    qr_code = IntegerField()
