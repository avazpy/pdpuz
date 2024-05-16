from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from apps.models import (Certificate, Course, DeletedUser, Device, Lesson,
                         LessonQuestion, Module, Payment, Task, TaskChat, User,
                         UserCourse, UserLesson, UserModule, UserTask, Video, )


@admin.register(User)
class CustomUserAdmins(UserAdmin):
    list_display = ("phone_number", 'photo', "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", 'photo')}),
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

    def get_course_count(self, obj):
        return obj.course_set.count()


@admin.register(UserCourse)
class UsersCoursesAdmin(ModelAdmin):
    list_display = ("user", "course")
    pass


class TaskNestedStackedInline(NestedStackedInline):
    model = Task
    exclude = ('user_task_list',)
    extra = 0
    min_num = 0
    list_display = ("user", "course", "task")


class LessonNestedStackedInline(NestedStackedInline):
    model = Lesson
    exclude = ('is_deleted', 'video_count', 'url',)
    fk_name = 'module'
    inlines = [TaskNestedStackedInline]
    extra = 0
    min_num = 0
    list_display = ("user", "course", "lesson")


class ModuleStackedInline(NestedStackedInline):
    model = Module
    inlines = [LessonNestedStackedInline]
    fields = ('title', 'learning_type', 'support_day', 'course', 'order')
    fk_name = 'course'
    extra = 0
    min_num = 0
    list_display = ('title', 'learning_type', 'support_day', 'course', 'order')


@admin.register(Course)
class CoursesAdminAdmin(NestedModelAdmin):
    inlines = [ModuleStackedInline]
    readonly_fields = ['lesson_count', 'modul_count', 'task_count']
    list_display = ('title', 'modul_count', 'lesson_count', 'task_count')


@admin.register(TaskChat)
class TasksChatAdmin(ModelAdmin):
    pass


@admin.register(UserModule)
class CourseModuleAdmin(ModelAdmin):
    pass


@admin.register(UserLesson)
class UserLessonAdmin(ModelAdmin):
    list_display = ("user", "lesson")


@admin.register(Video)
class VideosAdmin(ModelAdmin):
    pass


@admin.register(LessonQuestion)
class LessonQuestionsAdmin(ModelAdmin):
    pass


@admin.register(UserTask)
class UserTaskAdmin(ModelAdmin):
    list_display = ("user", "task")
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


@admin.register(DeletedUser)
class DeletedUserAdmin(ModelAdmin):
    pass
