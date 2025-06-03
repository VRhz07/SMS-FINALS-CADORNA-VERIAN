from rest_framework import serializers
from students.models import Student, Subject, Grade

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Grade
        fields = '__all__'
        
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
        
    def get_subject_name(self, obj):
        return obj.subject.name
        
class GradeDetailSerializer(GradeSerializer):
    class Meta(GradeSerializer.Meta):
        depth = 1
