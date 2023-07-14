from drf_yasg import openapi
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from event_app.serializers import UserRegisterSerializer, UserLoginSerializer, EventSerializer
from event_app.models import Event


class EventListView(ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(creator=user)


class EventDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(creator=user)


class AllEventListView(ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
        },
    ))
    def post(self, request):
        event_id = request.data.get('event_id', None)
        if event_id is None:
            return Response({'error': 'No event_id provided'}, status=status.HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Event, id=event_id)

        if event.date < timezone.now():
            return Response({'error': 'Cannot register for past events'}, status=status.HTTP_400_BAD_REQUEST)

        if event.attendees.count() >= event.capacity:
            return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.add(request.user)
        event.save()

        return Response({'message': 'Registered successfully'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('event_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def delete(self, request):
        event_id = request.query_params.get('event_id', None)
        event = get_object_or_404(Event, id=event_id)

        if event.date < timezone.now():
            return Response({'error': 'Cannot unregister from past events'}, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.remove(request.user)
        event.save()

        return Response({'message': 'Unregistered successfully'}, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects.create_user(username=username, password=password)
            user.save()

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
