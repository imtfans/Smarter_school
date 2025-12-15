from django.core.management.base import BaseCommand
from core.models import Student

# Mapping for promotion
PROMOTION_ORDER = {
    'JSS1': 'JSS2',
    'JSS2': 'JSS3',
    'JSS3': 'SS1',
    'SS1': 'SS2',
    'SS2': 'SS3',
    'SS3': None  # Graduated
}

class Command(BaseCommand):
    help = 'Promote students to the next class'

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        promoted_count = 0
        graduated_count = 0

        for student in students:
            next_class = PROMOTION_ORDER.get(student.current_class)
            if next_class:
                student.current_class = next_class
                student.save()
                promoted_count += 1
            else:
                graduated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Promotion completed: {promoted_count} students promoted, {graduated_count} graduated.'
        ))


class Command(BaseCommand):
    help = 'Promote all eligible students to the next class'

    def handle(self, *args, **options):
        students = Student.objects.filter(is_graduated=False)
        count = 0

        for student in students:
            student.promote()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'{count} students processed successfully.')
        )
