from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Author
from .serializers import AuthorSerializer

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

from rest_framework.decorators import permission_classes
from django.core.mail import send_mail


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def list_authors(request):
    queryset = Author.objects.all()
    serializer = AuthorSerializer(queryset, many=True)
    print(serializer.data)
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
