from rest_framework import serializers
from .models import CustomUser


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['preferences']
