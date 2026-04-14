"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView

import helloworld.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', helloworld.views.index),

    path('downfile1/', helloworld.views.download_file1),
    path('downfile2/', helloworld.views.download_file2),
    path('downfile3/', helloworld.views.download_file3),
    path('redirectTo',RedirectView.as_view(url='/')),
    path('blog/<int:id>', helloworld.views.blog),
    path('blog2/<int:year>/<int:month>/<int:day>', helloworld.views.blog2),

    re_path('blog3/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})', helloworld.views.blog2),

    path('to_login/',helloworld.views.to_login),
    path('login',helloworld.views.login),
    #path('index/', helloworld.views.index)
    path('toUpload/ ',helloworld.views.to_upload),
    path('Upload',helloworld.views.upload_file),
    #path('index/', helloworld.views.index)

    path('student/list',helloworld.views.List.as_view()),
    path('student/<int:id>', helloworld.views.Detail.as_view()),

    path('student/create', helloworld.views.Create.as_view()),

    path('student/update/<int:id>', helloworld.views.Update.as_view()),
    path('student/delete/<int:id>', helloworld.views.Delete.as_view()),

    path('toCourse/', helloworld.views.to_course),

    path('book/list/', helloworld.views.bookList),

    path('book/list2/', helloworld.views.bookList2),
    path('book/preAdd/', helloworld.views.preAdd),

    path('book/add/', helloworld.views.add),

    path('book/preUpdate/<int:id>'  , helloworld.views.preUpdate),
    path('book/update/', helloworld.views.update),

path('book/delete/<int:id>'  , helloworld.views.delete),
    path('transfer/',helloworld.views.transfer),
path('book/preAdd2/', helloworld.views.preAdd2),
path('book/preAdd3/', helloworld.views.preAdd3),

]
