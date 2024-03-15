from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_user(self, login, password=None, is_active=False, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', is_active)

        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('role', None)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login, password, **extra_fields)


class UserRole(models.Model):
    role_name = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("This user role already exists."),
        },
    )

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = _("User Role")
        verbose_name_plural = _("User Roles")
        db_table = 'user_role'


class User(AbstractUser):
    role = models.ForeignKey(UserRole, null=True, on_delete=models.SET_NULL)
    login = models.CharField(
        _('login'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that login already exists.")
        },
    )
    full_name = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False)
    reason_for_deletion = models.CharField(max_length=100, null=True)

    username = None
    first_name = None
    last_name = None
    email = None
    groups = None
    user_permissions = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['role', 'full_name', 'password']

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = 'user'


class UserInfo(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name='user_info')
    photo_avatar = models.ImageField(upload_to='user/avatar/', null=True, blank=True)
    contacts = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

    def __str__(self):
        try:
            return self.user.full_name
        except AttributeError:
            return self.user.login

    class Meta:
        verbose_name = _("UserInfo")
        verbose_name_plural = _("UserInfo")
        db_table = 'user_info'
