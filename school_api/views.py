import datetime
from functools import partial
from rest_framework import generics
from school.models import Course, User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, CoursesSerializer, EnrollmentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, UpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

class UserDetailAPI(RetrieveUpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  serializer_class = UserSerializer

  def get_object(self):
    return User.objects.get(id=self.request.user.id)

class RegisterUserAPIView(CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class CoursesListAPI(ListAPIView):
  authentication_classes = (TokenAuthentication,)
  serializer_class = CoursesSerializer
  pagination_class = PageNumberPagination

  def get_queryset(self):
    return Course.objects.filter(users__in = [self.request.user.id])

class StudentsListAPI(ListAPIView):
  authentication_classes = (TokenAuthentication,)
  serializer_class = UserSerializer
  pagination_class = PageNumberPagination

  def get_queryset(self):
    if self.request.user.user_type == "STUDENT":
      raise ValidationError(
              {'permission denied': "Can't see this course students"}
            )
    course = Course.objects.get(users__in = [self.request.user.id])
    return course.users.filter(user_type = "STUDENT")

class EnrollmentAPI(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  serializer_class = EnrollmentSerializer
  queryset = Course.objects.all()
  
  def update(self, request, *args, **kwargs):
    date_today = datetime.datetime.now().date()
    course_id = request.data.dict().get("course_id")
    instance = User.objects.get(id=self.request.user.id)
    print(course_id)
    course = Course.objects.get(id = course_id)
    if course.active == 0:
      raise ValidationError(
        {'permission denied': "Course is not active"}
      )
    elif date_today > course.start_date:
      raise ValidationError(
        {'permission denied': "Course has started"}
      )
    elif instance.user_type == "TEACHER":
      raise ValidationError(
        {'permission denied': "Teacher can't enroll"}
      )
    serializer = self.get_serializer(instance, data=request.data.dict(), partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "enrolled successfully"})
    else:
      return Response({"message": "failed", "details": serializer.errors})
