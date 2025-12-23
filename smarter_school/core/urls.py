from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, StudentViewSet, TeacherViewSet,
    SubjectViewSet, ResultViewSet, AttendanceViewSet,
    healthz_check,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('healthz/', healthz_check, name='health-check'),
]
