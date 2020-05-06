from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class MCH(models.Model):
    name = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name


class staffType(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields) 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField( unique=True)
    name = models.CharField(max_length=200, null=True)
    staffType = models.ForeignKey(staffType, null=True, on_delete= models.SET_NULL)
    MCH = models.ForeignKey(MCH, null=True, on_delete= models.SET_NULL)
    date_joined = models.DateTimeField( auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField( default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)





class Comment(models.Model):
    created_by = models.CharField(max_length=200)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.created_by)




class staff(models.Model):
    user = models.OneToOneField(User,null=True, editable=False,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    staffType = models.ForeignKey(staffType, null=True, on_delete= models.SET_NULL)
    MCH = models.ForeignKey(MCH, null=True, on_delete= models.SET_NULL)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class service(models.Model):
    
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class servedPatients(models.Model):
            
    name = models.CharField(max_length=200, null=True)
    service = models.ForeignKey(service, null=True, on_delete= models.SET_NULL)
    User = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    MCH = models.ForeignKey(MCH, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   

    def __str__(self):
        return self.name
class bills(models.Model):
    
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class order(models.Model):
            
    name = models.ForeignKey(bills,max_length=200, null=True,on_delete= models.SET_NULL)
    description = models.CharField(max_length=300, null=True)
    created_by = models.CharField(max_length=200,null=True,blank=True)
    viewed_by = models.CharField(max_length=200,default=None,null=True,blank=True)
    done = models.BooleanField( default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    

