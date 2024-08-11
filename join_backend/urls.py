"""join_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from join.views import LoginView, RegisterView, ListTasks, TaskDetailView, ListUsers, CurrentUserView, ListContacts, ContactDetailView, ListSubTasks, SubTaskDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view()),
    path('api/v1/register/', RegisterView.as_view()),
    path('api/v1/tasks/', ListTasks.as_view()),
    path('api/v1/tasks/<int:pk>/', TaskDetailView.as_view()),
    path('api/v1/subtasks/', ListSubTasks.as_view()),
    path('api/v1/subtasks/<int:pk>/', SubTaskDetailView.as_view()),
    path('api/v1/contacts/', ListContacts.as_view()),
    path('api/v1/contacts/<int:pk>/', ContactDetailView.as_view()),
    path('api/v1/users/', ListUsers.as_view()),
    path('api/v1/current_user/', CurrentUserView.as_view()),
]
