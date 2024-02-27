from django.contrib import admin

from apps.models import User, UserCourse, Course, Module, Task, TaskChat, Video, LessonQuestion, Lesson, \
    Device, Payment, Certificate, CreatedBaseModel


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCourse)
class UsersCoursesAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CoursesAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(Module)
class ModulesAdminAdmin(admin.ModelAdmin):
    pass


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
