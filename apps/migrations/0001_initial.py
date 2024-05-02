# Generated by Django 5.0.2 on 2024-05-02 12:46

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('title', models.CharField(max_length=255, verbose_name='title_Lesson')),
                ('order', models.IntegerField(verbose_name='order_Lesson')),
                ('url', models.URLField(max_length=255, verbose_name='url_Lesson')),
                ('video_count', models.PositiveIntegerField(default=0, verbose_name='video_count')),
                ('materials', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['pdf', 'pptx', 'ppt'])], verbose_name='materials_Lesson')),
                ('is_deleted', models.BooleanField(verbose_name='is_deleted_Lesson')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format '+998'. Up to 13 digits allowed.", regex='^\\+?1?\\d{9,13}$')])),
                ('balance', models.PositiveIntegerField(default=0, verbose_name='balance')),
                ('bot_options', models.CharField(blank=True, max_length=255, null=True, verbose_name='bot options')),
                ('country_model', models.BooleanField(default=False, verbose_name='country model')),
                ('has_registered_bot', models.BooleanField(default=False)),
                ('not_read_message_count', models.PositiveIntegerField(default=0)),
                ('payme_balance', models.PositiveIntegerField(default=0)),
                ('photo', models.ImageField(default='users/default.jpg', upload_to='users/images', verbose_name='Photo')),
                ('ticket_role', models.CharField(blank=True, max_length=255, null=True)),
                ('voucher_balance', models.PositiveIntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('finished_at', models.DateField(verbose_name='finished_at')),
                ('qr_code', models.ImageField(upload_to='media/certificates_qr', verbose_name='qr_code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.course')),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='LessonQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('text', models.TextField(blank=True, null=True, verbose_name='text_LessonQuestion')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='file_LessonQuestion')),
                ('voice_message', models.FileField(blank=True, null=True, upload_to='', verbose_name='voice_mes_LessonQuestion')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LessonQuestion',
                'verbose_name_plural': 'LessonQuestions',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('learning_type', models.CharField(max_length=255, verbose_name='learning_type')),
                ('lesson_count', models.PositiveIntegerField(default=0, verbose_name='lesson_count')),
                ('order', models.IntegerField(verbose_name='order')),
                ('row_num', models.PositiveIntegerField(default=0, verbose_name='row_num')),
                ('support_day', models.DateField()),
                ('task_count', models.PositiveIntegerField(default=0, verbose_name='task_count')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.module'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('reason', models.CharField(max_length=255, verbose_name='reason')),
                ('expend', models.CharField(max_length=255, verbose_name='expend')),
                ('balance', models.PositiveIntegerField(verbose_name='balance')),
                ('income', models.BooleanField(default=False, verbose_name='income')),
                ('processed_date', models.DateTimeField(verbose_name='processed date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_task_list', models.CharField(max_length=255, verbose_name='user_task_list')),
                ('task_number', models.PositiveIntegerField(default=0, verbose_name='task number')),
                ('lastTime', models.DateTimeField(verbose_name='lastTime')),
                ('order', models.IntegerField(verbose_name='order')),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='priority')),
                ('mustComplete', models.BooleanField()),
                ('files', models.CharField(max_length=255, verbose_name='files')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.lesson')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Task',
            },
        ),
        migrations.CreateModel(
            name='TaskChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('file', models.FileField(max_length=255, upload_to='', verbose_name='file')),
                ('voice', models.FileField(max_length=255, upload_to='', verbose_name='voice')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TaskChat',
                'verbose_name_plural': 'TaskChat',
            },
        ),
        migrations.CreateModel(
            name='UserLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('blocked', 'BLOCKED'), ('in_prog', 'IN_PROG'), ('finished', 'FINISHED')], default='blocked', verbose_name='status_UserLesson')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='apps.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('media_code', models.CharField(max_length=255, verbose_name='media code')),
                ('file', models.FileField(upload_to='videos/video', verbose_name='file_video')),
                ('is_youtube', models.BooleanField(default=False, verbose_name='is_youtube')),
                ('media_url', models.CharField(max_length=255, verbose_name='media_url')),
                ('order', models.PositiveIntegerField(verbose_name='order')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.lesson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('blocked', 'BLOCKED'), ('in_prog', 'IN_PROG'), ('finished', 'FINISHED')], default='blocked', verbose_name='status')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Course',
                'verbose_name_plural': 'User Courses',
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.CreateModel(
            name='UserModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('blocked', 'BLOCKED'), ('in_prog', 'IN_PROG'), ('finished', 'FINISHED')], default='blocked', verbose_name='status_UserModule')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Module',
                'verbose_name_plural': 'User Modules',
                'unique_together': {('user', 'module')},
            },
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('finished', models.BooleanField(default=False, verbose_name='finished')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserTask',
                'verbose_name_plural': 'UserTasks',
                'unique_together': {('user', 'task')},
            },
        ),
    ]
