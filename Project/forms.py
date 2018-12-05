from django import forms
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name', 'project_password', 'admin_password']


class JoinForm(forms.ModelForm):
    class Meta:
        model = ProjectUser
        fields = ['user_name', 'project_name', 'project_password']

class InviteForm(forms.ModelForm):
    class Meta:
        model = ProjectUser
        fields = ['project_name','user_name']


class FileForm(forms.ModelForm):
    class Meta:
        model = ProjectFiles
        fields = ['file_title',
                  'content',
                  'file_id',
                  'parent_file_id',
                  'file',]


class MemoForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['memo']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['schedule']

class AdminCertificationForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['admin_password']


class BranchSetForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_root']