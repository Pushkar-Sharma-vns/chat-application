import jwt
from datetime import datetime, timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from chat_application.settings import SECRET_KEY


class TimeStamped(models.Model):
    created_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)
    
    
class UserManager(BaseUserManager):
    def create_user(self, name, email, password, **extra_fields):
        if not name:
            raise TypeError("User must provide name.")
        if not email:
            raise TypeError("User  must provide email.")
        
        user = self.model(name=name, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, name, email, password, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(name=name, email=email, password=password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, TimeStamped):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=150, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def token(self):
        return self._generate_jwt_token()
        
    def _generate_jwt_token(self):
        """
            Generates a JSON Web Token that stores this user's ID and has an expiry
            date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=7)
        token = jwt.encode({
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'exp': dt
        }, SECRET_KEY, algorithm='HS256')
        
        return token