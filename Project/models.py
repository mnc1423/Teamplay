from django.db import models

# Create your models here.
from django.db import models
from django.db.models import TextField


class Projects(models.Model):
    project_name = models.CharField(db_column='project_name', max_length=10, blank=True, null=True)
    project_password = models.CharField(db_column='project_password', max_length=30, blank=True, null=True)
    admin_password = models.CharField(db_column='admin_password', max_length=30, blank=True, null=True)
    project_root = models.CharField(db_column='project_root', max_length=20, blank=True, null=True)
    schedule = models.TextField(null=True)
    memo = models.TextField(null=True)

class ProjectUser(models.Model):
    project_name = models.CharField(db_column='project_name', max_length=10, blank=True, null=True)
    project_password = models.CharField(db_column='project_password', max_length=30, blank=True, null=True)
    user_name = models.CharField(db_column='user_name', max_length=10, blank=True, null=True)
   #auth_code = models.IntegerField(db_column='Auth_code', default=1) #관리자는 1, 사용자는 0

class ProjectFiles(models.Model):
    user_name = models.CharField(db_column='user_name', max_length=10, blank=True, null=True)
    project_name = models.CharField(db_column='project_name', max_length=10, blank=True, null=True)
    file_title = models.CharField(db_column='file_title', max_length=100, default="")
    file_id = models.CharField(db_column='file_id', max_length=20, blank=True, null=True)
    parent_file_id = models.CharField(db_column='parent_file_id', max_length=20, blank=True, null=True)
    file = models.FileField(upload_to='project/%Y/%m/%d/file', null=True, blank=True)
    content = models.TextField(null=True)
    origin_date = models.DateTimeField(db_column='Origin_date', blank=True, null=True)
    final_date = models.DateTimeField(db_column='Final_date', blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(ProjectFiles, self).delete(*args, **kwargs)
