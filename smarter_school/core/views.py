from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Subject, Result, Attendance
from .serializers import (
    UserSerializer, StudentSerializer, TeacherSerializer, SubjectSerializer,
    ResultSerializer, AttendanceSerializer
)
from .permissions import IsAdmin, IsTeacher, IsParent, IsAdminOrReadOnly

User = get_user_model()


# --------------------------
# USER VIEWSET (Admin only)
# --------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


# --------------------------
# STUDENT VIEWSET
# --------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]


# --------------------------
# TEACHER VIEWSET
# --------------------------
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]


# --------------------------
# SUBJECT VIEWSET
# --------------------------
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]


# --------------------------
# RESULT VIEWSET
# --------------------------
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsTeacher]


# --------------------------
# ATTENDANCE VIEWSET
# --------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher]
