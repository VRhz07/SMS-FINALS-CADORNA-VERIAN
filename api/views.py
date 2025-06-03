from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from students.models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer, GradeDetailSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['student_id', 'last_name', 'date_joined']
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        student = self.get_object()
        subjects = student.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        student = self.get_object()
        grades = Grade.objects.filter(student=student)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        subject = self.get_object()
        students = subject.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        subject = self.get_object()
        grades = Grade.objects.filter(subject=subject)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__first_name', 'student__last_name', 'subject__name', 'title']
    ordering_fields = ['date_recorded', 'grade_type']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GradeDetailSerializer
        return self.serializer_class
    
    def get_queryset(self):
        queryset = Grade.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        grade_type = self.request.query_params.get('grade_type', None)
        
        if student_id:
            queryset = queryset.filter(student__id=student_id)
        if subject_id:
            queryset = queryset.filter(subject__id=subject_id)
        if grade_type:
            queryset = queryset.filter(grade_type=grade_type)
            
        return queryset
