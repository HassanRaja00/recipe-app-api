from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                    PermissionsMixin
'''
^ is required to extend the default django user model to make your own
'''


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('User email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # makes pwd encrypted
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''Creates new superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


'''NOTE: everytime you make changes to models you must run makemigrations'''


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that supports using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'