from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group

# Custom User Manager to handle user creation and superuser creation
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

# Custom User model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='user_set_truedetect', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_truedetect',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.phone_number
    
# Model for storing user contacts (name and phone_number are user-specific)
class UserContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contacts")
    contact_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# Phone_Book or Contact_list of all users are stored via this model 
class PhoneNumber(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    spam_likelihood = models.IntegerField(default=0)

    def __str__(self):
        return self.number
    
        
# Model to track spam actions by users
class SpamAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_marked_as_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name