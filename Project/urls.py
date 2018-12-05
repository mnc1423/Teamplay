from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.moduMain, name='moduMain'),
    url(r'^makeProject/$', views.projectMake, name='projectMake'),
    url(r'^makeAdmin/$', views.makeAdmin, name='makeAdmin'),
    url(r'^join/$', views.join, name='join'),
    url(r'^project/(?P<project_name>\w+)/$', views.mainProject, name='mainProject'),
    url(r'^project/(?P<project_name>\w+)/all/$', views.allMainProject, name='allMainProject'),
    url(r'^project/(?P<project_name>\w+)/schedule/$', views.schedule, name='schedule'),
    url(r'^project/(?P<project_name>\w+)/memo//$', views.memo, name='memo'),
    url(r'^project/(?P<project_name>\w+)/adminCertification/$', views.adminCertificate, name='adminCertification'),
    url(r'^project/(?P<project_name>\w+)/members/$', views.members, name='members'),
    url(r'^project/(?P<project_name>\w+)/newFile/$', views.newFile, name='newFile'),
    url(r'^project/(?P<project_name>\w+)/setBranch/$', views.setBranch, name='setBranch'),
    url(r'^project/(?P<project_name>\w+)/branchAdminCertification/$', views.branchAdminCertificate, name='branchAdminCertification'),
    url(r'^project/(?P<project_name>\w+)/(?P<file_title>\w+)/$', views.fileDetail, name='fileDetail'),
    url(r'^project/(?P<project_name>\w+)/(?P<file_title>\w+)/editFile/$', views.editFile, name='editFile'),
    url(r'^project/(?P<project_name>\w+)/(?P<file_title>\w+)/removeFile/$', views.fileRemove, name='fileRemove'),
 ]