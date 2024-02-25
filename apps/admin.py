from django.contrib import admin

from apps.models import Users, UsersCourses, Courses, Modules, Tasks, TasksCourses, Video, LessonQuestions, Lessons


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


@admin.register(TasksCourses)
class TasksCoursesAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonQuestions)
class LessonQuestionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    pass
