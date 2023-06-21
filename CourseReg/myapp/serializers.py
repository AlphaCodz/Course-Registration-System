from rest_framework import serializers
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
        
        