from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Create's an account
        """
        if not email:       raise ValueError("An email must be provided")
        if not username:    raise ValueError("A username must be provided")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None):
        """
        Create's an admin user
        """
        user = self.create_user(email, username, password)
        
        # Give admin priviledges
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        
        user.save()
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(verbose_name='email', max_length=256, unique=True, editable=False, null=False)
    username    = models.CharField(verbose_name='username', max_length=128, unique=True, editable=False, null=False)

    # Account information
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True, editable=False)
    last_login  = models.DateField(verbose_name='last login', auto_now=True, editable=False)
    blog_count  = models.IntegerField(verbose_name='blog count', editable=False, default=0)

    # Permissions
    is_active   = models.BooleanField(verbose_name='is active', default=False)
    is_staff    = models.BooleanField(verbose_name='is staff', default=False)
    is_admin    = models.BooleanField(verbose_name='is admin', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.username} | {self.email}'

    # Queries
    def fetchAll(self):
        return self.objects.all()
    
    def fetchUserById(self, id: int):
        return self.objects.get(id=id)
    
    def fetchUserByEmail(self, email: str):
        return self.objects.get(email=email)
    
    def fetchUserByUsername(self, username:str):
        return self.objects.get(username=username)
    