"""
URL configuration for voting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from apps.views import *

urlpatterns = [
    path('', login_page, name='home'),      
    path('login/', login_page, name='login'), 
    path('sign_up/'  , sign_up , name="sign_up"),
    path('admin_dashboard/' , admin_dashboard , name="admin_dashboard"),
    path('hr_dashboard/' , hr_dashboard  , name="hr_dashboard"),
    path('add_employee/' , add_employee , name="add_employee"),
    path('employee_list/' ,  employee_list , name="employee_list"),
    path('edit_employee/<int:id>/',edit_employee , name="edit_employee"),
    path('delete_employee/<int:id>/' , delete_employee , name="delete_employee"),
    path('employee_dashboard/' , employee_dashboard , name="employee_dashboard"),
    path('logout/' , user_logout , name="logout"),
    path('create_hr/',create_hr , name="create_hr"),
    path('employees/' , employee_list , name="employee_list"),
    path('activity_logs/' , activity_logs , name="activity_logs"),
    path('hr_management/', emp_management , name="hr_management"),
    path('edit_hr/<int:id>/' , edit , name="edit_hr"),
    path('delete_hr/<int:id>/' ,delete , name="delete_hr"),
    path('error/' , error , name="error"),
    path('admin_rewards/' , admin_rewards , name="admin_rewards"),
    path('admin_voting/' , admin_voting , name="admin_voting"),
    path('admin_performance/' , admin_performance , name="admin_performance"),
    path('reward_management/' , reward_management , name="reward_management"),
    path('performance/' , performance , name="performance")
]
