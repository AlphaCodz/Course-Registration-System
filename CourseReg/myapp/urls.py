from django.urls import path
from .views import RegisterStudent

urlpatterns = [
    path("reg/student", RegisterStudent.as_view(), name="register-student")
]
