from django.shortcuts import render
from .models import MainUser
from .serializers import StudentSerializer, MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
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

class StudentLogin(APIView):
    def post(self, request, format=None):
        student = MainUser.objects.filter(is_student=True, matric_number=request.data.get("matric_number")).first()
        if not student:
            resp = {
                "code": 404,
                "message": "Incorrect Matric Number"
            }
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
        if student.check_password(raw_password=request.data["password"]):
            token = RefreshToken.for_user(student)
            resp = {
                "code": 200,
                "message": "Login Successful",
                "student_data":
            {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "username": student.username,
                "matric_number": student.matric_number,
                "password": student.password
            },
                "token": str(token.access_token)
            }
            return Response(resp, status=status.HTTP_200_OK)
        resp = {
            "code": 401,
            "message": "Incorrect Password"
        }
        return Response(resp, status=status.HTTP_401_UNAUTHORIZED)  