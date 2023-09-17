from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
# Create your views here.

class ViewQuestions(APIView):
    def get(self, request):
        query = Course.objects.all()
        serializer = CourseSerializer(query ,many=True)
        return Response(serializer.data)