from django.db import models
from django.contrib.auth.models import User
import uuid

class ProfileTypeChoice(models.TextChoices):
    SUPER_ADMIN = "Super Admin"
    ORGANIZATION_ADMIN = "Organization_Admin"

# Create your models here.
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, db_index=True)
    profile_phone = models.CharField(default='', max_length=9000, blank=True, null=True)
    profile_user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, db_index=True)
    profile_organization = models.CharField(default='', max_length=9000)
    profile_type = models.CharField(default='Organization_Admin', choices = ProfileTypeChoice.choices, max_length=9000)
    profile_is_active = models.BooleanField(default=True, db_index=True)
    profile_created_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profiles'
        ordering = ['-id']
        verbose_name_plural = "USER PROFILES"

    def __str__(self):
        return f"{self.profile_organization} : {self.profile_user.first_name} {self.profile_user.last_name}"

class SavePasswordRequestUsers(models.Model):
    primary_key = models.AutoField(primary_key=True)
    save_pswd_user = models.ForeignKey(User, related_name='password_profile', on_delete=models.CASCADE)
    save_pswd_token = models.CharField(max_length=300, editable=False, default=None)
    save_pswd_is_used = models.BooleanField(default=False)
    save_pswd_is_active = models.BooleanField(default=True)
    # save_pswd_expiration_time = models.DateTimeField()
    
    class Meta:
        db_table = 'save_password_request'
        ordering = ['-primary_key']
        verbose_name_plural = "SAVE PASSWORD REQUESTS"

    def __str__(self):
        return "{} - {}".format(self.save_pswd_user, self.save_pswd_token)
