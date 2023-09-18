from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Question
from .serializers import CourseSerializer, QuestionSerializer,StudentSerializer
import datetime
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework import status


JWT_SECRET = 'jfejefj8jefefje8fjelfjqef8'

class ViewQuestions(APIView):
    def get(self, request):
        #Get question against the course
        courses = Course.objects.all()
        data = {}
        for course in courses:
            questions = Question.objects.filter(course=course)
            question_serializer = QuestionSerializer(questions, many=True)
            data[course.course_name] = question_serializer.data
        return Response(data)

class LoginView(APIView):
    def post(self, request):
        user = request.data['user']
        password = request.data['password']

        user = user.objects.filter(user=user).first()
        if user is None:
            raise AuthenticationFailed('user not found')

        checkpass = user.objects.filter(password=password).first()
        if checkpass is None:
            raise AuthenticationFailed('wrong password')

        payload = {
            'id': user.id,
            # expired in  1 minute
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'email' : user.email,
            'name' : user.name,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        res = Response()
        # res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt':  token,
        }

        return res
    
class CreateStudentView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 'ok',
                'message': 'Student created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        


class CreateQuestionView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 'ok',
                'message': 'question created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateCourseView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 'ok',
                'message': 'course created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

