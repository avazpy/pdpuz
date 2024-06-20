from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from apps.models import (Certificate, Course, DeletedUser, Device, Lesson,
                         LessonQuestion, Module, Payment, Task, TaskChat, User,
                         UserCourse, UserLesson, UserModule, UserTask, Video, )
from apps.proxies import (AdminUserProxy, AssistantUserProxy, StudentUserProxy,
                          TeacherUserProxy, )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("phone_number", "image_tag", "first_name", "last_name", "is_staff", 'type')
    fieldsets = (
        (None, {"fields": ("type", "phone_number", "password")}),
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

    def image_tag(self, obj):
        if obj.photo:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.photo.url))
        return '-'

    image_tag.short_description = 'Image'

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.photo.url))

    custom_image.short_description = "Image"

    def get_course_count(self, obj):
        return obj.course_set.count()

    # def small_image(self, obj):
    #     return '<img src="%s" style="max-width:100px; max-height:100px" />' % obj.image.url
    #
    # small_image.allow_tags = True


@admin.register(AdminUserProxy)
class CustomAdminUserProxyAdmin(UserAdmin):
    list_display = ("phone_number", 'photo', "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("type", "phone_number", "password")}),
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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.UserType.ADMIN)

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))
        return '-'

    image_tag.short_description = 'Image'

    def get_course_count(self, obj):
        return obj.course_set.count()


@admin.register(TeacherUserProxy)
class CustomTeacherProxyAdmin(UserAdmin):
    list_display = ("phone_number", 'photo', "first_name", "last_name", 'is_staff')
    fieldsets = (
        (None, {"fields": ("type", "phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", 'photo')}),
        (
            _("Permissions"),
            {
                'fields': (
                    'filter',
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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.UserType.TEACHER)

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.photo.url))

    custom_image.short_description = "Image"

    def get_course_count(self, obj):
        return obj.course_set.count()


@admin.register(AssistantUserProxy)
class CustomAssistantUserProxyAdmin(UserAdmin):
    list_display = ("phone_number", 'photo', "first_name", "last_name", 'is_staff',)
    fieldsets = (
        (None, {"fields": ("type", "phone_number", "password")}),
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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.UserType.ASSISTANT)

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.photo.url))

    custom_image.short_description = "Image"

    def get_course_count(self, obj):
        return obj.course_set.count()


@admin.register(StudentUserProxy)
class CustomStudentUserProxyAdmin(UserAdmin):
    search_fields = ['first_name', 'phone_number']
    list_display = ("phone_number", 'photo', "first_name", "last_name", "balance")
    fieldsets = (
        (None, {"fields": ("type", "phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", 'photo')}),
        (
            _("Permissions"),
            {
                'fields': (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.UserType.STUDENT)

    def custom_image(self, obj: User):
        return mark_safe('<img src="{}"/>'.format(obj.photo.url))

    custom_image.short_description = "Image"

    def get_course_count(self, obj):
        return obj.course_set.count()


@admin.register(UserCourse)
class UsersCoursesAdmin(ModelAdmin):
    list_display = ("user", "course")
    list_filter = ['course']
    search_fields = ['user__phone_number', 'course__title']
    pass


class TaskNestedStackedInline(NestedStackedInline):
    model = Task
    exclude = ('user_task_list',)
    extra = 0
    min_num = 0
    list_display = ("user", "course", "task")
    pass


class LessonNestedStackedInline(NestedStackedInline):
    model = Lesson
    exclude = ('is_deleted', 'video_count', 'url',)
    fk_name = 'module'
    inlines = [TaskNestedStackedInline]
    extra = 0
    min_num = 0
    list_display = ("user", "course", "lesson")
    pass


class ModuleStackedInline(NestedStackedInline):
    model = Module
    inlines = [LessonNestedStackedInline]
    fields = ('title', 'learning_type', 'support_day', 'course', 'order')
    fk_name = 'course'
    extra = 0
    min_num = 0
    list_display = ('title', 'learning_type', 'support_day', 'course', 'order')
    pass


@admin.register(Course)
class CoursesAdminAdmin(NestedModelAdmin):
    inlines = [ModuleStackedInline]
    readonly_fields = ['lesson_count', 'modul_count', 'task_count']
    list_display = ('title', 'modul_count', 'lesson_count', 'task_count')


@admin.register(TaskChat)
class TasksChatAdmin(ModelAdmin):
    list_display = ('user', 'task')
    pass


@admin.register(UserModule)
class UserModuleAdmin(ModelAdmin):
    list_display = ('user', 'module')
    pass


@admin.register(UserLesson)
class UserLessonAdmin(ModelAdmin):
    list_display = ("user", "lesson")
    pass


@admin.register(Video)
class VideosAdmin(ModelAdmin):
    list_display = ("lesson",)
    pass


@admin.register(LessonQuestion)
class LessonQuestionsAdmin(ModelAdmin):
    list_display = ("lesson", "text")
    pass


@admin.register(UserTask)
class UserTaskAdmin(ModelAdmin):
    list_display = ('user', 'task')
    pass


@admin.register(Payment)
class PaymentsAdmin(ModelAdmin):
    list_display = ("user",)
    pass


@admin.register(Device)
class DevicesAdmin(ModelAdmin):
    pass


@admin.register(Certificate)
class CertificatesAdmin(ModelAdmin):
    list_display = 'user', 'course'
    pass


@admin.register(DeletedUser)
class DeletedUserAdmin(ModelAdmin):
    pass
