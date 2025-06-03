from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/add/', views.student_form, name='add_student'),
    path('students/edit/<int:pk>/', views.student_form, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_form, name='add_subject'),
    path('subjects/edit/<int:pk>/', views.subject_form, name='edit_subject'),
    path('subjects/delete/<int:pk>/', views.delete_subject, name='delete_subject'),
    path('grades/add/', views.grade_form, name='add_grade'),
    path('grades/edit/<int:pk>/', views.grade_form, name='edit_grade'),
    path('grades/delete/<int:pk>/', views.delete_grade, name='delete_grade'),
]
