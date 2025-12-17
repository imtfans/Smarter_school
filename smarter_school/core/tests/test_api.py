from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            role='admin'
        )

    def test_student_list_requires_auth(self):
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
