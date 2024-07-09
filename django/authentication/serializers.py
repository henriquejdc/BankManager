# Third party imports
from rest_framework import serializers, status
from rest_framework.validators import ValidationError

# Project imports
from .models import User


class HealthSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=40, allow_blank=True)
    email = serializers.EmailField(max_length=80, allow_blank=False)
    password = serializers.CharField(allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, attrs):
        email = User.objects.filter(username=attrs.get('username')).exists()
        username = User.objects.filter(username=attrs.get('username')).exists()    

        if email:
            raise ValidationError(detail="User with email exists", code=status.HTTP_403_FORBIDDEN)

        if username:
            raise ValidationError(detail="User with username exists", code=status.HTTP_403_FORBIDDEN)

        return super().validate(attrs)

    def create(self, validated_data):

        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
            )

            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as e:
            raise ValidationError(detail=e, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
