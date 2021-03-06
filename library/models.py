from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

from uuid import UUID, uuid4


class LibraryManager(BaseUserManager):

    def create(self, **validated_data):

        # check required fields
        if not validated_data['email_id']:
            raise ValueError('User must have an email id')

        if not validated_data['password']:
            raise ValueError('User must have an password')

        # Normalize email and save password in encrypted form
        employee = self.model(email_id=self.normalize_email(validated_data['email_id'].lower()))
        employee.set_password(validated_data['password'])

        #save employee details
        employee.id         = validated_data['id']
        employee.first_name =  validated_data['first_name']
        employee.last_name  = validated_data['last_name']

        # save django employee role

        employee.staff        = validated_data.get('staff', 'False')
        employee.admin        = validated_data.get('admin', 'False')
        employee.is_active    = validated_data.get('is_active', 'True')

        employee.last_login = timezone.now()

        employee.save(using=self._db)

        return employee


class User(AbstractBaseUser):

    id                  = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email_id:str        = models.EmailField(unique=True)
    first_name          = models.CharField(max_length=20)
    last_name           = models.CharField(max_length=20)
    is_active:bool      = models.BooleanField(default=True)
    admin:bool          = models.BooleanField(default=False)
    staff:bool          = models.BooleanField(default=False)
    last_login          = models.DateTimeField(null=True)

    USERNAME_FIELD='email_id'
    REQUIRED_FIELDS=[]

    objects             = LibraryManager()


    def __str__(self)->str:
        return self.email_id

    def has_perm(self,perm,obj=None)->bool:
        return True

    def has_module_perms(self,app_label)->bool:
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Books(models.Model):

    id                    = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    isbn:int              = models.IntegerField(unique=True)
    title:str             = models.CharField(max_length=100)
    author:str            = models.CharField(max_length=100)
    publication:str       = models.CharField(max_length=50)

    objects               = models.Manager()

    def __str__(self):
        return "{}".format(self.title)


