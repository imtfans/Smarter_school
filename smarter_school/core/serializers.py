from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Subject, Result, Attendance

User = get_user_model()


# --------------------------
# USER SERIALIZER
# --------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# --------------------------
# STUDENT SERIALIZER
# --------------------------
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# --------------------------
# TEACHER SERIALIZER
# --------------------------
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


# --------------------------
# SUBJECT SERIALIZER
# --------------------------
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


# --------------------------
# RESULT SERIALIZER
# --------------------------
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['total', 'grade']


# --------------------------
# ATTENDANCE SERIALIZER
# --------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
