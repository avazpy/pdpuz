from django.contrib import admin

from apps.models import Users, UsersCourses, Courses, Modules, Tasks, TasksChat, Videos, LessonQuestions, Lessons, \
    Devices, Payments, Certificates, CreatedBaseModel


@admin.register(CreatedBaseModel)
class CreatedBaseModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(UsersCourses)
class UsersCoursesAdmin(admin.ModelAdmin):
    pass


@admin.register(Courses)
class CoursesAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(Modules)
class ModulesAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(Tasks)
class TasksAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(TasksChat)
class TasksChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonQuestions)
class LessonQuestionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    pass


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    pass


@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    pass
