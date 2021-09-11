from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.name


class EducationModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    started = models.DateField()
    end = models.DateField(null=True, blank=True)


class WorkExperienceModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_type = models.CharField(max_length=30)
    job_desc = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    started = models.DateField()
    left = models.DateField(null=True, blank=True)


class AwardModel(models.Model):
    user = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE)
    detail = models.CharField(max_length=255, null=True, blank=True)
