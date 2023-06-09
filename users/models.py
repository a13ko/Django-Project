from django.db import models

from services.choiches import account
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from services.generator import CodeGenerator


class MyUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_active=True, is_staff=False, is_superuser=False
    ):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_staff = True
        user.is_superuser = True
        user.user_type = "owner"
        user.save(using=self._db)
        return user

    


def upload_to(instance, filename):
    return f"users/{instance.email}/{filename}"


class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=120)
    full_name = models.CharField(max_length=40, blank=True, null=True)
    logo = models.ImageField(upload_to='posters/', default='logo1.jpg' )
    username = models.CharField(max_length=40, blank=True, null=True)
    account = models.CharField(max_length=30,choices=account,default='Basic')

    slug = models.SlugField(unique=True)
    hash_key = models.CharField(max_length=200, blank=True, null=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code = models.CharField(max_length=50, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = CodeGenerator.create_slug_shortcode_profile(size=20, model_=MyUser)

       
    #     if self.logo and hasattr(self.logo, 'name'):
    #         from django.core.files.storage import default_storage as storage
    #         from django.core.files.base import ContentFile

            
    #         filename = f'users/logos/{self.slug}.jpg'
    #         if self.logo:
    #             storage.delete(self.logo.name)
    #             storage.save(filename, ContentFile(self.logo.read()))
    #             self.logo.name = filename

    #     return super(MyUser, self).save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = CodeGenerator.create_slug_shortcode_profile(size=20, model_=MyUser)

        if self.logo and hasattr(self.logo, 'name'):
            from django.core.files.storage import default_storage as storage
            from django.core.files.base import ContentFile

            filename = f'users/logos/{self.slug}.jpg'
            if self.logo:
                if self.logo.name != filename:
                    storage.delete(filename)
                    storage.save(filename, ContentFile(self.logo.read()))
                    self.logo.name = filename

        return super(MyUser, self).save(*args, **kwargs)