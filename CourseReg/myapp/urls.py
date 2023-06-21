from django.urls import path, include
from rest_framework import routers
from .views import RegisterStudent

router = routers.DefaultRouter()
router.register(r'student', RegisterStudent, basename="students")

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

