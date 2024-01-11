from .views import list_authors, author_info, add_author
from django.urls import path


urlpatterns = [
    path('', list_authors),
    path('authors/<str:name>/', author_info, name='author_info'),
    path('add_author/', add_author),
]