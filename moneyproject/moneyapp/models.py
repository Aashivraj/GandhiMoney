from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


    



class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, mobile_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not user_name:
            raise ValueError('The User Name field must be set')
        if not mobile_number:
            raise ValueError('The Mobile Number field must be set')

        email = self.normalize_email(email)
        user = self.model(
            user_name=user_name,
            email=email,
            mobile_number=mobile_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, email, mobile_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(_("user name"), max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    mobile_number = models.CharField(_("mobile number"), max_length=15, unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set'  # Add unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set'  # Add unique related_name
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email", "mobile_number"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def toggle_active_status(self):
        self.is_active = not self.is_active
        self.save()

    def get_full_name(self):
        """Return the full name of the user."""
        return self.user_name

    def get_short_name(self):
        """Return the short name of the user."""
        return self.user_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class PaymentType(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    money = models.IntegerField()
 
    def __str__(self):
        return self.title


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(PaymentType,on_delete=models.CASCADE)
    money=models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)


 
    
class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(PaymentType,on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    money=models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    
