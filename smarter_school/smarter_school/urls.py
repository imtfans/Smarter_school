from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    UserViewSet, StudentViewSet, TeacherViewSet,
    SubjectViewSet, ResultViewSet, AttendanceViewSet,
    healthz
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('healthz/', healthz),  # ✅ THIS IS THE FIX
]
