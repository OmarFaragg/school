from rest_framework import serializers
from school.models import User, Course
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "user_type", "gender", "date_of_birth"]
    read_only_fields = ('user_type', 'date_of_birth', 'id')

class CoursesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ["id", "name", "start_date", "end_date", "active"]

class EnrollmentSerializer(serializers.ModelSerializer):
  course_id = serializers.IntegerField()
  class Meta:
    model = Course
    fields = ["id", "active", "course_id"]

  def update(self, instance, validated_data):
    course_id = validated_data.get("course_id")
    course = Course.objects.get(id=course_id)
    course.users.add(instance)
    return instance

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name', 'gender', 'user_type', 'date_of_birth')
    extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True},
        'user_type': {'required': True},
        'gender': {'required': True},
        'date_of_birth': {'required': True},
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      gender=validated_data['gender'],
      user_type=validated_data['user_type'],
      date_of_birth=validated_data['date_of_birth']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

