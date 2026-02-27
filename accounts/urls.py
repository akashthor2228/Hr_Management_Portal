from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/',auth_views.LogoutView.as_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
#     employee urls
    path('employee/',views.employee_home,name="employee_home"),
    path('employee/add',views.add_employee,name="add_employee"),
    path('employee/view',views.view_employee,name="view_employee"),
    path('employee/update/<int:id>',views.update_employee,name="update_employee"),
    path('employee/delete/<int:id>',views.delete_employee,name="delete_employee"),


]