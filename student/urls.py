from django.urls import path

from student import views

urlpatterns = [
    path('',views.student_home,name='student_home'),
    path('add',views.add_student,name='add_student'),
    path('view',views.view_students,name='view_students'),
    path('update/<int:id>',views.update_student,name='update_student'),
    path('delete/<int:id>',views.delete_student,name='delete_student'),
    path('profile',views.student_profile,name='student_profile'),
    path('available_drives',views.available_drives,name='available_drives'),
    path('applied_drives',views.applied_drives,name='applied_drives'),
    path('change_password',views.change_password,name='change_password'),
    path('apply/<int:company_id>', views.apply_drive, name='apply_drive'),
]