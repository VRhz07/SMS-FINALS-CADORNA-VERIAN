from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SubjectViewSet, GradeViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
