from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
