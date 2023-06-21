from django.shortcuts import render
from .models import MainUser
from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
# Create your views here.

class RegisterStudent(viewsets.ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = StudentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        students = self.queryset.filter(is_student=True)
        student_data = [
            {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "username": student.username,
                "matric_number": student.matric_number,
                "password": student.password
            }
            for student in students
        ]
        return Response(student_data, status=status.HTTP_200_OK)