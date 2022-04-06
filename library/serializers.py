from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .models import User, Books

from uuid import uuid4


###################
# User Serializer #
###################
class UserSerializer(serializers.ModelSerializer):

    id          = serializers.UUIDField(format="hex_verbose", read_only=True)
    email_id    = serializers.EmailField()
    first_name  = serializers.CharField(max_length=20)
    last_name   = serializers.CharField(max_length=20)
    password    = serializers.CharField(max_length=50,write_only=True)
    is_active   = serializers.BooleanField()
    admin       = serializers.BooleanField()
    staff       = serializers.BooleanField()

    class Meta:
        model=User
        fields=[

            'id',
            'email_id',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'admin',
            'staff'
        ]

    #######################
    # Validation of Email #
    #######################
    def validate_email_id(self,value:str)->str:
        queryset=None

        if self.context.get('view').request.method =="POST":

            queryset=User.objects.filter(email_id=value)

        if queryset.exists():
            raise serializers.ValidationError("User With this Email already exists")

        return value

    def create(self, validated_data):
        validated_data['id']=uuid4()
        return User.objects.create(**validated_data)


#####################
# SignIn Serializer #
#####################
class SignInSerializer(serializers.ModelSerializer):

    id         = serializers.UUIDField(read_only=True,format="hex_verbose")
    email_id   = serializers.EmailField(max_length=255)
    password   = serializers.CharField(max_length=50, write_only=True)
    token      = serializers.SerializerMethodField()
    message    = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=['id','email_id','password','token','message']

    ###############################
    # Authenticating User #
    ###############################
    def validate(self,data):
        request=self.context.get('view').request

        self.user=authenticate(request,email_id=data.get('email_id').lower(),password=data.get('password'))

        if self.user is None:
            raise serializers.ValidationError("Please Enter Valid Credentials")

        return data

    def get_token(self, instance:User)->str:
        return instance.auth_token.key

    def get_message(self, instance)->str:
        return 'Singin Successfully'

    def create(self, validated_data):

        if hasattr(self.user, 'auth_token'):

            self.user.auth_token.delete()
        
        Token.objects.create(user=self.user)

        return self.user


##########################
# Serializer For BOOK #
##########################
class BooksSerializer(serializers.ModelSerializer):

    id                = serializers.UUIDField(read_only=True, format="hex_verbose")
    isbn:int          = serializers.IntegerField()
    title:str         = serializers.CharField(max_length=100)
    author:str        = serializers.CharField(max_length=100)
    publication:str   = serializers.CharField(max_length=50)

    class Meta:
        model=Books
        fields=['id','isbn','title','author','publication']

    ###########################
    # Validation of Book ISBN #
    ###########################
    def validate_isbn(self,value:int)->int:
        queryset=None

        if self.context.get('view').request.method =="POST":
            queryset=Books.objects.filter(isbn=value)

        elif self.context.get('view').request.method =="PUT":
            queryset=Books.objects.filter(isbn=value).exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("ISBN already exists")

        return value

    ############################
    # Validation of Book title #
    ############################
    def validate_title(self,value:str)->str:
        queryset=None

        if self.context.get('view').request.method =="POST":
            queryset=Books.objects.filter(title__icontains=value)

        elif self.context.get('view').request.method=="PUT":
            queryset=Books.objects.filter(title__icontains=value).exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("Title already exists")

        return value

    def create(self,validated_data):
        validated_data['id']=uuid4()
        return Books.objects.create(**validated_data)


    def update(self, instance, validated_data):

        instance.isbn         = validated_data.get('isbn', instance.isbn)
        instance.title        = validated_data.get('title',instance.title)
        instance.author       = validated_data.get('author',instance.author)
        instance.publication  = validated_data.get('publication',instance.publication)
        instance.save()

        return instance
