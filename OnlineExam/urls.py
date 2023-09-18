from django.contrib import admin
from django.urls import path
from Main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Course/', ViewQuestions.as_view(), name='Course details'),
    path('CreateStudent/', CreateStudentView.as_view(), name='create student'),
]
