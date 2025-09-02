from django.db import models
from uuid import uuid4

# Create your models here.
class Train(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    train_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    train_no = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.train_no

class Coach(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    coach_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    coach_no = models.CharField(max_length=20)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class MainActivity(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    main_activity_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class SubActivity(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    sub_activity_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    main_activity = models.ForeignKey(MainActivity, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
 
class SubSubActivity(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    sub_sub_activity_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    sub_activity = models.ForeignKey(SubActivity, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class ActivityDone(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    activity_done_id = models.UUIDField(default=uuid4, editable=False, null=True, blank=True)
    sub_activity = models.ForeignKey(SubActivity, on_delete=models.CASCADE, blank=True, null=True)
    sub_sub_activity = models.ForeignKey(SubSubActivity, on_delete=models.CASCADE, blank=True, null=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    route1 = models.CharField(max_length=50)
    route2 = models.CharField(max_length=50)
    route3 = models.CharField(max_length=50)
    route4 = models.CharField(max_length=50)
    remarks = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Report(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    report_id = models.UUIDField(unique=True, default=uuid4, editable=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    coordinator_remarks = models.CharField(max_length=250, blank=True)
    supervisor_remarks = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_created=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)


class ReportForActivity(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    activity_done = models.ForeignKey(ActivityDone, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)