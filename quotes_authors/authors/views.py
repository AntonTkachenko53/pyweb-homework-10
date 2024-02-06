from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Author, PasswordResetToken
from .serializers import AuthorSerializer, PasswordResetSerializer

from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView
from django.conf import settings


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = PasswordResetToken.objects.create(user=user)
                reset_link = request.build_absolute_uri('/') + f"reset-password/{token.token}/"
                subject = 'Reset your password'
                message = {
                    'user': user,
                    'reset_link': reset_link,
                }
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request, token):
        token_obj = PasswordResetToken.objects.filter(token=token).first()
        if token_obj:
            user = token_obj.user
            password = request.data.get('password')
            user.set_password(password)
            user.save()
            token_obj.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_authors(request):
    queryset = Author.objects.all()
    serializer = AuthorSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def author_info(request):
    author_name = request.GET.get('name')
    if author_name:
        queryset = Author.objects.filter(name=author_name)
    else:
        queryset = 'No authors found'

    serializer = AuthorSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@login_required
def add_author(request):
    serializer = AuthorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
