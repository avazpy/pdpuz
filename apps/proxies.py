from django.utils.translation import gettext_lazy as _

from apps.models import User


class AdminUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")


class TeacherUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")


class AssistantUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Assistant")
        verbose_name_plural = _("Assistants")


class StudentUserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
