from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from students.models import Student, Subject, Grade
from django.db import transaction

class Command(BaseCommand):
    help = 'Adds sample data to the database for testing and development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to add sample data...')
        
        # Clear existing data if needed
        self.stdout.write('Clearing existing data...')
        Grade.objects.all().delete()
        Subject.objects.all().delete()
        Student.objects.all().delete()
        
        try:
            with transaction.atomic():
                # Create sample students
                self.stdout.write('Creating sample students...')
                students = self._create_sample_students()
                
                # Create sample subjects
                self.stdout.write('Creating sample subjects...')
                subjects = self._create_sample_subjects()
                
                # Enroll students in subjects
                self.stdout.write('Enrolling students in subjects...')
                self._enroll_students_in_subjects(students, subjects)
                
                # Add sample grades
                self.stdout.write('Adding sample grades...')
                self._add_sample_grades(students, subjects)
                
            self.stdout.write(self.style.SUCCESS('Successfully added sample data to database!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error adding sample data: {str(e)}'))
    
    def _create_sample_students(self):
        students = []
        
        # Sample student data
        student_data = [
            {
                'student_id': '2023-0001',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'date_of_birth': datetime(2000, 5, 15)
            },
            {
                'student_id': '2023-0002',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@example.com',
                'date_of_birth': datetime(2001, 8, 22)
            },
            {
                'student_id': '2023-0003',
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'email': 'michael.johnson@example.com',
                'date_of_birth': datetime(2000, 11, 10)
            },
            {
                'student_id': '2023-0004',
                'first_name': 'Emily',
                'last_name': 'Williams',
                'email': 'emily.williams@example.com',
                'date_of_birth': datetime(2001, 3, 28)
            },
            {
                'student_id': '2023-0005',
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@example.com',
                'date_of_birth': datetime(2000, 7, 4)
            },
            {
                'student_id': '2023-0006',
                'first_name': 'Sarah',
                'last_name': 'Miller',
                'email': 'sarah.miller@example.com',
                'date_of_birth': datetime(2001, 9, 17)
            },
            {
                'student_id': '2023-0007',
                'first_name': 'James',
                'last_name': 'Wilson',
                'email': 'james.wilson@example.com',
                'date_of_birth': datetime(2000, 1, 30)
            },
            {
                'student_id': '2023-0008',
                'first_name': 'Lisa',
                'last_name': 'Anderson',
                'email': 'lisa.anderson@example.com',
                'date_of_birth': datetime(2001, 6, 12)
            },
            {
                'student_id': '2023-0009',
                'first_name': 'Robert',
                'last_name': 'Thomas',
                'email': 'robert.thomas@example.com',
                'date_of_birth': datetime(2000, 10, 5)
            },
            {
                'student_id': '2023-0010',
                'first_name': 'Jennifer',
                'last_name': 'Garcia',
                'email': 'jennifer.garcia@example.com',
                'date_of_birth': datetime(2001, 4, 20)
            }
        ]
        
        for data in student_data:
            student = Student.objects.create(**data)
            students.append(student)
            self.stdout.write(f'Created student: {student}')
        
        return students
    
    def _create_sample_subjects(self):
        subjects = []
        
        # Sample subject data
        subject_data = [
            {
                'name': 'Introduction to Computer Science',
                'code': 'CS101',
                'description': 'Fundamental concepts of computer programming and software development.',
                'credits': 3
            },
            {
                'name': 'Data Structures and Algorithms',
                'code': 'CS201',
                'description': 'Study of data structures, algorithms, and their analysis.',
                'credits': 4
            },
            {
                'name': 'Database Systems',
                'code': 'CS301',
                'description': 'Fundamentals of database design, development, and management.',
                'credits': 3
            },
            {
                'name': 'Web Development',
                'code': 'CS401',
                'description': 'Principles and practices of web application development.',
                'credits': 3
            },
            {
                'name': 'Artificial Intelligence',
                'code': 'CS501',
                'description': 'Introduction to artificial intelligence concepts and techniques.',
                'credits': 4
            },
            {
                'name': 'Calculus I',
                'code': 'MATH101',
                'description': 'Introduction to differential and integral calculus.',
                'credits': 4
            },
            {
                'name': 'Statistics',
                'code': 'MATH201',
                'description': 'Statistical methods and their applications.',
                'credits': 3
            }
        ]
        
        for data in subject_data:
            subject = Subject.objects.create(**data)
            subjects.append(subject)
            self.stdout.write(f'Created subject: {subject}')
        
        return subjects
    
    def _enroll_students_in_subjects(self, students, subjects):
        # Each student takes 3-5 subjects randomly
        for student in students:
            num_subjects = random.randint(3, 5)
            selected_subjects = random.sample(subjects, num_subjects)
            
            for subject in selected_subjects:
                student.subjects.add(subject)
                self.stdout.write(f'Enrolled {student} in {subject}')
    
    def _add_sample_grades(self, students, subjects):
        grade_types = dict(Grade.GRADE_TYPES)
        
        for student in students:
            # Get the subjects this student is enrolled in
            enrolled_subjects = student.subjects.all()
            
            for subject in enrolled_subjects:
                # Add activities
                for i in range(1, 4):  # 3 activities
                    score = random.uniform(70, 100)
                    max_score = 100
                    
                    Grade.objects.create(
                        student=student,
                        subject=subject,
                        grade_type='ACTIVITY',
                        title=f'Activity {i}',
                        score=round(score, 2),
                        max_score=max_score,
                        comments=f'Sample activity {i} for {subject.code}'
                    )
                
                # Add quizzes
                for i in range(1, 3):  # 2 quizzes
                    score = random.uniform(60, 100)
                    max_score = 100
                    
                    Grade.objects.create(
                        student=student,
                        subject=subject,
                        grade_type='QUIZ',
                        title=f'Quiz {i}',
                        score=round(score, 2),
                        max_score=max_score,
                        comments=f'Sample quiz {i} for {subject.code}'
                    )
                
                # Add midterm exam
                midterm_score = random.uniform(65, 95)
                Grade.objects.create(
                    student=student,
                    subject=subject,
                    grade_type='EXAM',
                    title='Midterm Exam',
                    score=round(midterm_score, 2),
                    max_score=100,
                    comments=f'Midterm exam for {subject.code}'
                )
                
                # Add final exam
                final_score = random.uniform(70, 98)
                Grade.objects.create(
                    student=student,
                    subject=subject,
                    grade_type='EXAM',
                    title='Final Exam',
                    score=round(final_score, 2),
                    max_score=100,
                    comments=f'Final exam for {subject.code}'
                )
