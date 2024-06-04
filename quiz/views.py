
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from web3 import Web3
from django.http import HttpResponse
from django.http import JsonResponse
from ipfshttpclient import connect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PictureForm 
import os
import requests
from dotenv import load_dotenv


load_dotenv()


def upload_to_pinata(filepath, jwt_token):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:
        response = requests.post(url, files={'file': file}, headers=headers)
        if response.status_code == 200:
            return response.json().get('IpfsHash')  # Return the IPFS hash
        else:
            return None  # Return None if upload fails
@csrf_exempt
def upload_picture(request,quizid):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            print("lll")
            picture = form.cleaned_data['picture']
            # Assuming MEDIA_ROOT is where you store uploaded files
            file_path = os.path.join(settings.MEDIA_ROOT, picture.name)
            with open(file_path, 'wb') as f:
                for chunk in picture.chunks():
                    f.write(chunk)
            PINATA_JWT_TOKEN = os.getenv('PINATA_JWT_TOKEN')
            ipfs_hash = upload_to_pinata(file_path, PINATA_JWT_TOKEN)
            print(ipfs_hash)
            os.remove(file_path)
            if ipfs_hash:
                return JsonResponse({'success': True, 'ipfs_hash': ipfs_hash})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to upload picture to Pinata'}, status=500)
    return  render(request, 'upload.html',{'quizid': quizid})


def index(request):
    return render(request, 'index.html')


def display(request):
    return render(request, 'display.html')

def questions(request,quizid):
    return render(request, 'questions.html', {'quizid': quizid})
    



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

def quiz(request):
    if request.method == 'POST':
        cur_user=request.user

        quiz_name = request.POST.get('quiz_name')
        question_texts = request.POST.getlist('question_text[]')
        question_marks = request.POST.getlist('question_marks[]')

        if quiz_name and question_texts and question_marks:
            quiz = Quiz.objects.create(quiz_name=quiz_name,user=cur_user)

            for text, marks in zip(question_texts, question_marks):
                Question.objects.create(question_text=text, quiz=quiz, question_marks=marks)

            return redirect('main')  

    return render(request, 'quiz.html')

def home(request):
    return render(request, 'home.html')

def main(request):
    return render(request, 'main.html')

def view_quiz(request):
    return render(request, 'view_quiz.html')

def assigned_quiz(request):
    quizzes = Quiz.objects.all()
    user = request.user
    attempted_quizzes = quiz_attempted.objects.filter(user_attempt=user).values_list('quiz_attempt', flat=True)
    return render(request, 'assigned_quiz.html', {'quizzes': quizzes, 'attempted_quizzes': attempted_quizzes})

def view_quiz_created(request):
    cur_user= request.user
    quizzes_created_by_user = Quiz.objects.filter(user=cur_user)
    print(quizzes_created_by_user)
    return render(request, 'view_quiz_created.html', {'quizzes': quizzes_created_by_user})

def view_each_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    quiz_attempts = quiz_attempted.objects.filter(quiz_attempt=quiz)
    print("qqq",quiz_attempts)
    user_attempts = []
    for attempt in quiz_attempts:
        user = attempt.user_attempt
        print("user",user)
        attempt_id = attempt.id
        is_evaluated = evaluated.objects.filter(quiz_eval=quiz, user_eval=user)
        print("iss",is_evaluated)
        user_evaluation_status = "Evaluated" if is_evaluated else "Evaluate"
        user_attempts.append({'user': user, 'attempt_id': attempt_id, 'evaluation_status': user_evaluation_status})
        print(user_attempts)

    context = {
        'quiz': quiz,
        'questions': questions,
        'user_attempts': user_attempts
    }
 
    return render(request, 'view_each_quiz.html', context)
       


def attempt_quiz(request, quiz_id):
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        answers = []
        for question in questions:
            answer_pic = request.FILES.get(f'answer_{question.question_id}') 
            if answer_pic:
                answers.append(Answer(student=request.user, question=question, answer_pic=answer_pic))
            else:
                messages.error(request, f'Answer for question "{question.question_text}" is missing.')
              
        if answers:
            Answer.objects.bulk_create(answers)
            quiz_attempted.objects.create(quiz_attempt=quiz, user_attempt=request.user)
            messages.success(request, 'Your answers have been submitted successfully!')
            return redirect('main')

    return render(request, 'attempt_quiz.html', {'quiz': quiz, 'questions': questions})

def attempt_detail(request, attempt_id):
    attempt = get_object_or_404(quiz_attempted, id=attempt_id)
    user_attempt = attempt.user_attempt
    quiz = attempt.quiz_attempt
    questions = Question.objects.filter(quiz=quiz)
    answers = Answer.objects.filter(student=user_attempt, question__quiz=quiz)
    print(answers)
    return render(request, 'attempt_detail.html', {'user_attempt': user_attempt, 'quiz': quiz, 'questions': questions, 'answers': answers})

def save_marks(request):
    if request.method == 'POST':
       
        for answer in Answer.objects.all():
            marks_field_name = 'marks_' + str(answer.id)
            if marks_field_name in request.POST:
                marks = int(request.POST[marks_field_name])
                answer.marks = marks
                answer.save()
        evaluated.objects.create( quiz_eval=answer.question.quiz,user_eval=answer.student)
        return render(request, 'main.html')
    else:
        
        pass
def view_marks(request,quiz_id):
  
    current_user = request.user
    quiz_questions = Question.objects.filter(quiz=quiz_id)
    question_marks = {}

    for question in quiz_questions:

        answer = Answer.objects.get(student=current_user, question=question)
        question_marks[question.question_text] = answer.marks
       

    context = {
        'question_marks': question_marks
    }
    return render(request, 'view_marks.html', context)


