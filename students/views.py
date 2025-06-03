from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Count, Case, When, IntegerField, F, Q
from django.utils import timezone
from .models import Student, Subject, Grade

def index(request):
    """Home page view"""
    students_count = Student.objects.count()
    subjects_count = Subject.objects.count()
    grades_count = Grade.objects.count()
    
    context = {
        'students_count': students_count,
        'subjects_count': subjects_count,
        'grades_count': grades_count,
    }
    return render(request, 'students/index.html', context)

def student_list(request):
    """View to display all students with search functionality"""
    search_query = request.GET.get('search', '')
    students = Student.objects.all()
    
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    return render(request, 'students/student_list.html', {
        'students': students,
        'search_query': search_query
    })

def student_detail(request, pk):
    """View to display student details including subjects and grades"""
    student = get_object_or_404(Student, pk=pk)
    subjects = student.subjects.all()
    grades = Grade.objects.filter(student=student)
    
    # Group grades by subject
    grades_by_subject = {}
    for grade in grades:
        subject_name = grade.subject.name
        if subject_name not in grades_by_subject:
            grades_by_subject[subject_name] = []
        grades_by_subject[subject_name].append(grade)
    
    context = {
        'student': student,
        'subjects': subjects,
        'grades_by_subject': grades_by_subject,
    }
    return render(request, 'students/student_detail.html', context)

def subject_list(request):
    """View to display all subjects with search functionality"""
    search_query = request.GET.get('search', '')
    subjects = Subject.objects.all()
    
    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'students/subject_list.html', {
        'subjects': subjects,
        'search_query': search_query
    })

def grade_form(request, pk=None):
    """View to add or edit a grade"""
    grade = None
    if pk:
        grade = get_object_or_404(Grade, pk=pk)
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        grade_type = request.POST.get('grade_type')
        title = request.POST.get('title')
        score = request.POST.get('score')
        max_score = request.POST.get('max_score')
        comments = request.POST.get('comments', '')
        
        if all([student_id, subject_id, grade_type, title, score, max_score]):
            student = get_object_or_404(Student, pk=student_id)
            subject = get_object_or_404(Subject, pk=subject_id)
            
            if grade:  # Update existing grade
                grade.student = student
                grade.subject = subject
                grade.grade_type = grade_type
                grade.title = title
                grade.score = score
                grade.max_score = max_score
                grade.comments = comments
                grade.save()
                messages.success(request, 'Grade updated successfully!')
            else:  # Create new grade
                Grade.objects.create(
                    student=student,
                    subject=subject,
                    grade_type=grade_type,
                    title=title,
                    score=score,
                    max_score=max_score,
                    comments=comments
                )
                messages.success(request, 'Grade added successfully!')
            
            # Redirect to the student detail page
            return redirect('students:student_detail', pk=student_id)
        else:
            messages.error(request, 'Please fill all required fields!')
    
    students = Student.objects.all()
    subjects = Subject.objects.all()
    
    context = {
        'grade': grade,
        'students': students,
        'subjects': subjects,
        'grade_types': Grade.GRADE_TYPES,
    }
    return render(request, 'students/grade_form.html', context)

# AJAX Views for frontend interactivity
def get_student_subjects(request, student_id):
    """AJAX view to get subjects for a student"""
    student = get_object_or_404(Student, pk=student_id)
    subjects = student.subjects.all()
    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)

# Student Form Views
def student_form(request, pk=None):
    """View to add or edit a student"""
    student = None
    if pk:
        student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth') or None
        
        # Check if required fields are filled
        if all([student_id, first_name, last_name, email]):
            # Check if the email is unique (except for current student when editing)
            email_exists = Student.objects.filter(email=email).exclude(pk=pk if pk else None).exists()
            student_id_exists = Student.objects.filter(student_id=student_id).exclude(pk=pk if pk else None).exists()
            
            if email_exists:
                messages.error(request, 'Email already exists. Please use a different email.')
            elif student_id_exists:
                messages.error(request, 'Student ID already exists. Please use a different ID.')
            else:
                # Create or update student
                if student:  # Update existing student
                    student.student_id = student_id
                    student.first_name = first_name
                    student.last_name = last_name
                    student.email = email
                    student.date_of_birth = date_of_birth
                    
                    # Handle profile picture
                    if 'remove_picture' in request.POST and student.profile_picture:
                        student.profile_picture.delete()
                        student.profile_picture = None
                    
                    if 'profile_picture' in request.FILES:
                        if student.profile_picture:
                            student.profile_picture.delete()
                        student.profile_picture = request.FILES['profile_picture']
                    
                    student.save()
                    messages.success(request, 'Student updated successfully!')
                else:  # Create new student
                    new_student = Student(
                        student_id=student_id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        date_of_birth=date_of_birth
                    )
                    
                    if 'profile_picture' in request.FILES:
                        new_student.profile_picture = request.FILES['profile_picture']
                    
                    new_student.save()
                    messages.success(request, 'Student added successfully!')
                
                return redirect('students:student_list')
        else:
            messages.error(request, 'Please fill all required fields!')
    
    context = {
        'student': student,
    }
    return render(request, 'students/student_form.html', context)

# Subject Form Views
def subject_form(request, pk=None):
    """View to add or edit a subject"""
    subject = None
    if pk:
        subject = get_object_or_404(Subject, pk=pk)
    
    # Get search query for students list
    search_query = request.GET.get('student_search', '')
    all_students = Student.objects.all()
    
    # Filter students if search query exists
    if search_query:
        all_students = all_students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        student_ids = request.POST.getlist('students')
        
        # Check if required fields are filled
        if all([code, name]):
            # Check if the code is unique (except for current subject when editing)
            code_exists = Subject.objects.filter(code=code).exclude(pk=pk if pk else None).exists()
            
            if code_exists:
                messages.error(request, 'Subject code already exists. Please use a different code.')
            else:
                # Create or update subject
                if subject:  # Update existing subject
                    subject.code = code
                    subject.name = name
                    subject.description = description
                    subject.save()
                    
                    # Update student enrollments
                    subject.students.clear()
                    for student_id in student_ids:
                        try:
                            student = Student.objects.get(pk=student_id)
                            subject.students.add(student)
                        except Student.DoesNotExist:
                            pass
                    
                    messages.success(request, 'Subject updated successfully!')
                else:  # Create new subject
                    new_subject = Subject.objects.create(
                        code=code,
                        name=name,
                        description=description
                    )
                    
                    # Add student enrollments
                    for student_id in student_ids:
                        try:
                            student = Student.objects.get(pk=student_id)
                            new_subject.students.add(student)
                        except Student.DoesNotExist:
                            pass
                    
                    messages.success(request, 'Subject added successfully!')
                
                return redirect('students:subject_list')
        else:
            messages.error(request, 'Please fill all required fields!')
    
    context = {
        'subject': subject,
        'all_students': all_students,
        'student_search_query': search_query,
    }
    return render(request, 'students/subject_form.html', context)


def delete_grade(request, pk):
    """View to delete a grade"""
    grade = get_object_or_404(Grade, pk=pk)
    student_id = grade.student.id
    
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted successfully!')
        return redirect('students:student_detail', pk=student_id)
    
    return render(request, 'students/confirm_delete.html', {
        'item': grade,
        'item_type': 'Grade',
        'cancel_url': reverse('students:student_detail', args=[student_id])
    })


def delete_student(request, pk):
    """View to delete a student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('students:student_list')
    
    return render(request, 'students/confirm_delete.html', {
        'item': student,
        'item_type': 'Student',
        'cancel_url': reverse('students:student_list')
    })


def delete_subject(request, pk):
    """View to delete a subject"""
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('students:subject_list')
    
    return render(request, 'students/confirm_delete.html', {
        'item': subject,
        'item_type': 'Subject',
        'cancel_url': reverse('students:subject_list')
    })


def admin_dashboard(request):
    """Admin dashboard view with system statistics and overview"""
    # Count statistics
    students_count = Student.objects.count()
    subjects_count = Subject.objects.count()
    grades_count = Grade.objects.count()
    activities_count = Grade.objects.filter(grade_type='ACTIVITY').count()
    
    # Recent grades
    recent_grades = Grade.objects.all().order_by('-date_recorded')[:5]
    
    # Subject statistics with student counts and percentages
    subjects_with_students = []
    subjects = Subject.objects.annotate(students_count=Count('students'))
    
    if students_count > 0:
        for subject in subjects:
            percentage = round((subject.students_count / students_count) * 100, 1)
            subjects_with_students.append({
                'name': subject.name,
                'code': subject.code,
                'students_count': subject.students_count,
                'percentage': percentage
            })
    
    # Create recent activities list (mock data for now)
    recent_activities = [
        {
            'title': 'New Student Registered',
            'description': 'A new student has been added to the system.',
            'timestamp': timezone.now() - timezone.timedelta(hours=2),
            'link': '/students/'
        },
        {
            'title': 'Grades Updated',
            'description': 'New grades have been added for Math 101.',
            'timestamp': timezone.now() - timezone.timedelta(hours=5),
            'link': None
        },
        {
            'title': 'New Subject Added',
            'description': 'Computer Science 202 has been added to the curriculum.',
            'timestamp': timezone.now() - timezone.timedelta(days=1),
            'link': '/subjects/'
        }
    ]
    
    context = {
        'students_count': students_count,
        'subjects_count': subjects_count,
        'grades_count': grades_count,
        'activities_count': activities_count,
        'recent_grades': recent_grades,
        'subjects_with_students': subjects_with_students,
        'recent_activities': recent_activities
    }
    
    return render(request, 'students/admin_dashboard.html', context)
