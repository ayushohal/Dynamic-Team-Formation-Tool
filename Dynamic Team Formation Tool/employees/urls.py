from django.contrib import admin
from django.urls import path
from employees import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('register/', views.register_employee, name='register_employee'),
    path('form-teams/', views.form_teams, name='form_teams'),
    path('success/', views.success, name='success'),
    path('employees/', views.employee_list, name='employee_list'), 
]
