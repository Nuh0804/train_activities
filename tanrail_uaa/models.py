from datetime import datetime,timedelta
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProfileTypeChoice(models.TextChoices):
    SUPER_ADMIN = "Super Admin"
    ORGANIZATION = "Organization"

# Create your models here.
class UserRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    role_name = models.CharField(default='', max_length=9000)
    role_description = models.CharField(default='', max_length=9000)
    role_is_active = models.BooleanField(default=True)
    role_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "USER ROLES"

    def __str__(self):
        return "{}".format(self.role_name)
    def get_role_permissions(self):
        return self.user_role_with_permission_role.select_related('role_with_permission_permission').all()


class UserPermissionsGroup(models.Model):
    primary_key = models.AutoField(primary_key=True)
    permission_group_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    permission_group_name = models.CharField(default='', max_length=9000)
    permission_group_is_global = models.BooleanField(default=False)
    permission_group_description = models.CharField(default='', max_length=600, null=True)
    permission_group_createdby = models.ForeignKey(User, related_name='permission_group_creator',on_delete=models.CASCADE)
    permission_group_createddate = models.DateField(auto_now_add=True)


    class Meta:
        db_table = 'user_permissions_group'
        ordering = ['-primary_key']
        verbose_name_plural = "PERMISSIONS GROUP"
    
    def __str__(self):
        return "{} - {}".format(self.permission_group_name, self.permission_group_description)
    
    def get_group_permisions(self):
        return self.permission_group.all()


class UserPermissions(models.Model):
    primary_key = models.AutoField(primary_key=True)
    permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    permission_name = models.CharField(default='', max_length=9000)
    permission_code = models.CharField(default='', max_length=9000)
    permission_group = models.ForeignKey(UserPermissionsGroup, related_name='permission_group',on_delete=models.CASCADE, null=True)
    permission_createdby = models.ForeignKey(User, related_name='user_permission_creator', on_delete=models.CASCADE)
    permission_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_permissions'
        ordering = ['-primary_key']
        verbose_name_plural = "USER PERMISSIONS"

    def __str__(self):
        return "{} - {}".format(self.permission_name, self.permission_group)


class UserRolesWithPermissions(models.Model):
    primary_key = models.AutoField(primary_key=True)
    role_with_permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    role_with_permission_role = models.ForeignKey(UserRoles, related_name='user_role_with_permission_role',on_delete=models.CASCADE)
    role_with_permission_permission = models.ForeignKey(UserPermissions,related_name='user_role_with_permission_permission',on_delete=models.CASCADE)
    permission_read_only = models.BooleanField(default=True)
    role_with_permission_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_role_with_permissions'
        ordering = ['-primary_key']
        verbose_name_plural = "ROLES WITH PERMISSIONS"


class UsersWithRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    user_with_role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    user_with_role_role = models.ForeignKey(UserRoles, related_name='user_role_name', on_delete=models.CASCADE)
    user_with_role_user = models.ForeignKey(User, related_name='role_user', on_delete=models.CASCADE)
    user_with_role_createddate = models.DateField(auto_now_add=True)


    class Meta:
        db_table = 'user_with_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "USERS WITH ROLES"
        
class ForgotPasswordRequestUser(models.Model):
    primary_key = models.AutoField(primary_key=True)
    request_user = models.ForeignKey(User, related_name='request_profile', on_delete=models.CASCADE)
    request_token = models.CharField(max_length=300, editable=False, default=None)
    request_is_used = models.BooleanField(default=False)
    request_is_active = models.BooleanField(default=True)
    request_created_date = models.DateTimeField(auto_now_add=True)
    request_expiration_time = models.DateTimeField()
    class Meta:
        db_table = 'users_forgot_password_request'
        ordering = ['-primary_key']
        verbose_name_plural = "FORGOT PASSWORD REQUESTS"

    def __str__(self):
        return f"{self.request_user} - {self.request_token}"

    def has_expired(self):
        # Calculate the time difference between now and request_created_date
        current_time = datetime.now()
        time_difference = current_time - self.request_created_date

        # Check if the time difference is greater than 24 hours (86400 seconds)
        if time_difference.total_seconds() > 86400:
            return True
        
        return False


class ActivateAccountTokenUser(models.Model):
    primary_key = models.AutoField(primary_key=True)
    token_user = models.ForeignKey(User, related_name='token_user', on_delete=models.CASCADE)
    token_token = models.CharField(max_length=300, editable=False, default=None)
    token_is_used = models.BooleanField(default=False)
    token_is_active = models.BooleanField(default=True)
    token_created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users_activate_account_token'
        ordering = ['-primary_key']
        verbose_name_plural = "ACTIVATE ACCOUNT TOKEN"

    def __str__(self):
        return f"{self.token_user} - {self.token_token}"

    def has_expired(self):
        # Get the current time in UTC
        current_time = timezone.now()
        
        # Calculate the time difference between now and token_created_date
        time_difference = current_time - self.token_created_date

        # Define a timedelta of 24 hours
        expiration_period = timedelta(hours=24)

        # Check if the time difference is greater than the expiration period
        if time_difference > expiration_period:
            return True
        return False