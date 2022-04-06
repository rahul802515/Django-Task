from django.contrib import admin
from django.urls import path
from library.views import SignUpAPIView, LogInAPIView, CreateBooksAPIView, ListBooksAPIView,RUDBooksApiView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LogInAPIView.as_view()),
    path('books/create', CreateBooksAPIView.as_view()),
    path('books/list', ListBooksAPIView.as_view()),
    path('books/<str:id>', RUDBooksApiView.as_view()),
]