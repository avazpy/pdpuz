from rest_framework.permissions import BasePermission

from apps.models import Lesson, UserCourse


class IsJoinedCoursePermission(BasePermission):

    def has_object_permission(self, request, view, obj: Lesson):
        return UserCourse.objects.filter(user=request.user, course_id=obj.module.course_id).exists()


class IsAdminsUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.type == "admin")
