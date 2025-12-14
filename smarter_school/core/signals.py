from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Result, Student

# Auto calculate total and grade
@receiver(post_save, sender=Result)
def auto_calculate_result(sender, instance, **kwargs):
    instance.total = instance.ca1 + instance.ca2 + instance.exam
    instance.grade = instance.calculate_grade()
    instance.save(update_fields=['total', 'grade'])


# Example: signal for automatic promotion (optional)
@receiver(post_save, sender=Student)
def check_student_promotion(sender, instance, **kwargs):
    """
    Placeholder: logic to promote student automatically after term/session.
    Can also be handled in management command.
    """
    pass
