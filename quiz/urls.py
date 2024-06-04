
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('main/', main, name='main'),
    path('index/', index, name='index'),
    path('display/', display, name='display'),
    path('quiz/', quiz, name='quiz'),
    path('questions/<int:quizid>/',questions,name="questions"),
     path('questions/<int:quizid>/upload_to_ipfs/', upload_picture, name='upload_to_ipfs'),
    path('assigned_quiz/',assigned_quiz, name='assigned_quiz'),
    path('upload/<int:quizid>/', upload_picture, name='upload'),
    path('view_quiz/', view_quiz, name='view_quiz'),


    path('view_quiz_created/', view_quiz_created, name='view_quiz_created'),
    path('attempt_quiz/<str:quiz_id>/', attempt_quiz, name='attempt_quiz'),
    path('view_marks/<str:quiz_id>/', view_marks, name='view_marks'),
    path('save_marks/', save_marks, name='save_marks'),
    path('view_each_quiz/<str:quiz_id>/',view_each_quiz, name='view_each_quiz'),
     path('attempt_detail/<int:attempt_id>/', attempt_detail, name='attempt_detail'),
    
]
