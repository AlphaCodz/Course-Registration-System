from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import MainUser

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['id', 'first_name', 'last_name', 'email', 'is_student', 'is_admin']
        
    def validate(self, attrs):
        if not attrs["last_name"]:
            return serializers.ValidationError({"error": "Provide a last name"})
        return attrs
    
    def create(self, validated_data):
        student = MainUser()
        student.first_name = validated_data["first_name"]
        student.last_name = validated_data["last_name"]
        student.email = validated_data["email"]
        student.is_student=True
        student.save()
        return student
        
        
        
# SIMPLEJWT SERIALIZER

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
        
    def validate(self, attrs):
        matric_number = attrs.get("matric_number")
        password = attrs.get("password")

        # Validate matric number and password
        if matric_number and password:
            try:
                user = MainUser.objects.get(matric_number=matric_number)
                if user.check_password(password):
                    if not user.is_active:
                        raise exceptions.AuthenticationFailed("Student account is disabled.")
                    refresh = self.get_token(user)
                    data = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return data
            except MainUser.DoesNotExist:
                pass

            raise exceptions.AuthenticationFailed("Invalid matric number or password.")
        else:
            raise exceptions.AuthenticationFailed("Matric number and password are required.")