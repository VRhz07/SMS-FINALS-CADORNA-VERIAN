from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(Student, related_name='subjects')
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Grade(models.Model):
    GRADE_TYPES = [
        ('ACTIVITY', 'Activity'),
        ('QUIZ', 'Quiz'),
        ('EXAM', 'Exam'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPES)
    title = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'grade_type', 'title']
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.title} ({self.grade_type})"
