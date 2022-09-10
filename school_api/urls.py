from django.urls import path
# from .views import StudentstList, UserDetail, TeachersList, CoursesList
from .views import UserDetailAPI, RegisterUserAPIView, CoursesListAPI, StudentsListAPI, EnrollmentAPI

app_name = 'school_api'

urlpatterns = [
    path('students-list', StudentsListAPI.as_view()),
    path('enroll', EnrollmentAPI.as_view()),
    path('courses-list', CoursesListAPI.as_view()),
    path('user-details',UserDetailAPI.as_view()),
    path('register',RegisterUserAPIView.as_view()),
]