from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import User, UserCourse, Course, Module, Task, TaskChat, Video, LessonQuestion, Lesson, \
    Device, Payment, Certificate


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
class UsersCoursesAdmin(admin.ModelAdmin):
    pass


class ModuleStackedInline(admin.StackedInline):
    model = Module
    exclude = ()
    extra = 1
    min_num = 1


@admin.register(Course)
class CoursesAdminAdmin(admin.ModelAdmin):
    inlines = [ModuleStackedInline]


@admin.register(Task)
class TasksAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskChat)
class TasksChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideosAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonQuestion)
class LessonQuestionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonsAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DevicesAdmin(admin.ModelAdmin):
    pass


@admin.register(Certificate)
class CertificatesAdmin(admin.ModelAdmin):
    pass
