from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission
import logging

logger = logging.getLogger("signals")


@receiver(post_save, sender=Submission)
def file_saved(sender, instance, created, **kwargs):
    if created:
        message = f"Студент {instance.student} надіслав файл: {instance.file}"
        message_for_log = f"Student {instance.student} sent file: {instance.file}"
    else:
        message = f"Для студента {instance.student} виставили оцінку до файлу: {instance.file}"
        message_for_log = f"For student {instance.student} was sent a grade to file: {instance.file}"

    logger.info(message_for_log)
    print(f"[SIGNAL] {message}")
