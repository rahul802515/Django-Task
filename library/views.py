from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication

from django.core.exceptions import ObjectDoesNotExist

from .serializers import BooksSerializer, SignInSerializer, UserSerializer
from .models import User, Books


###############
# Sign UP View
###############
class SignUpAPIView(CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[AllowAny]

    def get_serializer_context(self):
        return {'view':self}

    def perform_create(self,serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()


##############
# Log In View
##############
class  LogInAPIView(CreateAPIView):
    serializer_class=SignInSerializer
    permission_classes=[AllowAny]

    def get_serializer_context(self):
        return {'view':self}

    def perform_create(self, serializer):

        if serializer.is_valid(raise_exception=True):
            serializer.save()


################
# View OF BOOKS
###############
class CreateBooksAPIView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BooksSerializer
    authentication_class=[TokenAuthentication]

    def get_serializer_context(self):
        return {'view':self}

    def perform_create(self,serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()


class ListBooksAPIView(ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=BooksSerializer

    def get_queryset(self):
        return Books.objects.all()


class RUDBooksApiView(RetrieveUpdateDestroyAPIView):
    permissions_classes=[IsAuthenticated]
    serializer_class=BooksSerializer
    authentication_class=[TokenAuthentication]

    def get_serializer_context(self):
        return {'view':self}

    def get_object(self,**kwargs):

        try:

            return Books.objects.get(id=self.kwargs['id'])

        except ObjectDoesNotExist as exc:
            raise APIException("Object Not Found.")

        except Exception as exc:
            raise APIException(exc)

    def perform_update(self,serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
