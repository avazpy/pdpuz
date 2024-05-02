from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
# from parler.admin import TranslatableAdmin


from apps.models import User, UserCourse, Course, Module, Task, TaskChat, Video, LessonQuestion, Lesson, \
    Device, Payment, Certificate, UserTask, UserLesson, UserModule


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", 'photo', "email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'photo', 'phone_number')}),
        (
            _("Permissions"),
            {
                'fields': (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.photo.url))

    custom_image.short_description = "Image"


@admin.register(UserCourse)
class UsersCoursesAdmin(ModelAdmin):
    pass


class TaskNestedStackedInline(NestedStackedInline):
    model = Task
    exclude = ('user_task_list',)
    extra = 0
    min_num = 1


class LessonNestedStackedInline(NestedStackedInline):
    model = Lesson
    exclude = ('is_deleted', 'video_count', 'url',)
    fk_name = 'module'
    inlines = [TaskNestedStackedInline]
    extra = 0
    min_num = 1


class ModuleStackedInline(NestedStackedInline):
    model = Module
    inlines = [LessonNestedStackedInline]
    fields = ('title', 'learning_type', 'support_day', 'user', 'course', 'order')
    fk_name = 'course'
    extra = 0
    min_num = 1


@admin.register(Course)
class CoursesAdminAdmin(NestedModelAdmin):
    inlines = [ModuleStackedInline]


@admin.register(TaskChat)
class TasksChatAdmin(ModelAdmin):
    pass


@admin.register(UserModule)
class UserModuleAdmin(ModelAdmin):
    pass


@admin.register(UserLesson)
class UserLessonAdmin(ModelAdmin):
    pass


@admin.register(Video)
class VideosAdmin(ModelAdmin):
    pass


@admin.register(LessonQuestion)
class LessonQuestionsAdmin(ModelAdmin):
    pass


@admin.register(UserTask)
class UserTaskAdmin(ModelAdmin):
    pass


@admin.register(Payment)
class PaymentsAdmin(ModelAdmin):
    pass


@admin.register(Device)
class DevicesAdmin(ModelAdmin):
    pass


@admin.register(Certificate)
class CertificatesAdmin(ModelAdmin):
    pass
