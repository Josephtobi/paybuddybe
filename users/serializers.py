from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField(max_length=100)
    dob = serializers.DateField()
    country = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(default=True)
    password = serializers.CharField()
    email_verified = serializers.BooleanField(default=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
