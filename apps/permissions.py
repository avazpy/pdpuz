from rest_framework.permissions import BasePermission

from apps.models import Lesson, UserCourse


class IsJoinedCoursePermission(BasePermission):

    def has_object_permission(self, request, view, obj: Lesson):
        return UserCourse.objects.filter(user=request.user, course_id=obj.module.course_id).exists()
