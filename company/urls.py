from django.urls import path

from company import views

urlpatterns = [
    path('',views.company_home,name='company_home'),
    path('add', views.add_company, name="add_company"),
    path('view', views.view_company, name="view_company"),
    path('update/<int:id>', views.update_company, name="update_company"),
    path('delete/<int:id>', views.delete_company, name="delete_company"),
    path('view_applied_students/<int:company_id>/', views.view_applied_students, name='view_applied_students'),
]