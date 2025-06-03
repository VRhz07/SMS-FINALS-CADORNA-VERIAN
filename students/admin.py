from django.contrib import admin
from .models import Student, Subject, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'date_joined')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    list_filter = ('date_joined',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    filter_horizontal = ('students',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade_type', 'title', 'score', 'max_score', 'date_recorded')
    list_filter = ('grade_type', 'subject', 'date_recorded')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name', 'title')
