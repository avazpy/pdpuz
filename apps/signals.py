from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Lesson


@receiver(post_save, sender=Lesson)
def update_lesson_count(sender, instance, created, **kwargs):
    if created:
        instance.course.lesson_count += 1
    else:
        instance.course.lesson_count = models.F('lesson_count') - 1
    instance.course.save()

@receiver(post_delete, sender=Lesson)
def decrease_lesson_count(sender, instance, **kwargs):
    instance.course.lesson_count = models.F('lesson_count') - 1
    instance.course.save()
