from rest_framework import serializers
from .models import Voter

class VoterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'phone_number', 'password']

class VoterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['first_name', 'last_name', 'middle_name', 'phone_number', 'password']


