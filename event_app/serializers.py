from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'creator', 'title', 'description', 'date', 'type', 'status', 'capacity', 'attendees']
        extra_kwargs = {
            'id': {'help_text': 'Unique identifier for the event.'},
            'creator': {'help_text': 'User who created the event.'},
            'title': {'help_text': 'Title of the event.'},
            'description': {'help_text': 'Description of the event.'},
            'date': {'help_text': 'Date and time of the event.'},
            'type': {'help_text': 'Type of the event.'},
            'status': {'help_text': 'Current status of the event.'},
            'capacity': {'help_text': 'Number of people who can attend the event.'},
            'attendees': {'help_text': 'List of users attending the event.'},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'help_text': 'Username to login.'},
            'password': {'help_text': 'Password.'}
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
