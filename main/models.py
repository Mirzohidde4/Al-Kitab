from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.
class Categorys(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Janr'
        verbose_name_plural = 'Janrlar'


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='Kitob nomi')
    author = models.CharField(max_length=100, verbose_name='Muallif')
    genre = models.ManyToManyField(Categorys, verbose_name='Janri', related_name='janrlar')
    price = models.DecimalField(verbose_name='Narxi', max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name='Tavsif')
    image = models.ImageField(upload_to='images/', verbose_name='Rasm', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name
    
    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class SelectedBooks(models.Model):  
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'book') #faqat 1 marta qo'shish uchun  
        verbose_name = 'Tanlangan kitob'
        verbose_name_plural = 'Tanlangan kitoblar'
