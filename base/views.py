from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .form import CallBookingForm
from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
import openai
from django.conf import settings
from .form import ChatForm
from lib2to3.pgen2 import token
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from .form import PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import LogoutView
from .form import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from .form import SignUpForm
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, UserResponse
import os
import joblib
from django.shortcuts import render
from .form import MoodForm
from .models import UserInput
from django.shortcuts import render
from .form import PredictionForm
from .utils import predict_blood_sugar


# Create your views here.

def predict_view(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            bmi = form.cleaned_data['bmi']
            blood_pressure = form.cleaned_data['blood_pressure']
            result = predict_blood_sugar(bmi, blood_pressure)
            return render(request, 'base/result.html', {'result': result})
    else:
        form = PredictionForm()
    return render(request, 'base/predict.html', {'form': form})


# Create your views here.

def chat_page_view(request):
    return render(request, 'base/chat.html')


@login_required
def home_view(request):
    return render(request, 'base/home.html')

@login_required
def fitness_view(request):
    return render(request, 'base/fitness.html')

@login_required
def health_view(request):
    return render(request, 'base/health.html')

@login_required
def medication(request):
    return render(request, 'base/medication.html')

@login_required
def nutrition_view(request):
    return render(request, 'base/nutrition.html')

@login_required
def book_call(request):
    if request.method == 'POST':
        form = CallBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CallBookingForm()
    return render(request, 'base/book_call.html', {'form': form})

def success(request):
    return HttpResponse("Your call has been successfully booked!")
def index(request):
    return render(request, 'base/index.html')



@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'base/quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        for question in quiz.questions.all():
            selected_option = request.POST.get(str(question.id))
            UserResponse.objects.create(
                user=request.user,
                question=question,
                selected_option=selected_option
            )
        return render(request, 'base/quiz_result.html', {'quiz': quiz})
    else:
        return render(request, 'base/take_quiz.html', {'quiz': quiz})

# predictor/views.py
# health_app/views.py


# Define the path to the directory where the model and vectorizer are stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'mood_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# Check if the model and vectorizer files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"Vectorizer file not found: {VECTORIZER_PATH}")
from .form import CustomPasswordResetForm
from .form import PasswordResetForm

# Load the machine learning model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_mood(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)
    return prediction[0]

def mood_predictor_view(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            mood = predict_mood(text)
            UserInput.objects.create(text=text, mood=mood)
            return render(request, 'base/mood_result.html', {'mood': mood})
    else:
        form = MoodForm()
    return render(request, 'base/mood_form.html', {'form': form})

@login_required
def predictor_view(request):
    return render(request, 'base/health_predictor.html')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            subject = 'Welcome to Our Site'
            message = render_to_string('base/welcome_email.html', {'user': user})
            send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message)

            return redirect('custom_login')  
    else:
        form = SignUpForm()
    return render(request, 'base/sign_UP.html', {'form': form})


def send_welcome_email(user_email, username):
    subject = 'Welcome to Our App!'
    html_message = render_to_string('base/welcome_email.html', {'username': username})
    plain_message = strip_tags(html_message)
    from_email = 'vaibhavpatyal507@gmail.com' 
    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                return redirect('forgot_password')
            
            
            reset_link = request.build_absolute_uri('/') + f'reset-password/'
            send_mail(
                'Password Reset',
                f'Click the link below to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Email field is required.')
            return redirect('forgot-password')
    return render(request, 'base/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password')
            
            user = User.objects.filter().first()
            if not user:
                messages.error(request, 'Invalid or expired reset token.')
                return redirect('login')

            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful. You can now login with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Password fields are required.')
            return redirect('reset-password')
    return render(request, 'base/reset_password_form.html')



class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'base/password_reset_confirm.html'

def logout_view(request):
    logout(request)
    return redirect('login')


def send_password_reset_email(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                reset_link = f"http://127.0.0.1:8000/reset-password/{uuid}/{token}/"
                send_mail(
                    'Reset Your Password',
                    f'Click the following link to reset your password: {reset_link}',
                    'vaibhavpatyal507@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'base/password_reset_email_sent.html')
    else:
        form = PasswordResetForm()
    return render(request, 'base/password_reset_form.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if remember_me:
                request.session.set_expiry(604800)
            else:  
                request.session.set_expiry(0)   
            
            login(request, user)  #updated code to save login data into the session
            request.session['username'] = username  # Store username in session
            messages.success(request, 'Login successful.')
            # Print to nderstand whats happening
            print("User authenticated:", user)
            print("Session username after login:", request.session.get('username'))
            
            return redirect('accounts/profile/') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'base/login.html')



def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        return redirect('home/')
    else:
        return render(request, 'base/custom_login.html')

def about_us(request):
    return render(request, 'base/about_us.html')

def logout_view(request):
    logout(request)
    return redirect('login')



from .form import BMICalculatorForm

def bmi_calculator(request):
    bmi = None
    category = None

    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            bmi = weight / ((height / 100) ** 2)

            if bmi < 18.5:
                category = 'Underweight'
            elif 18.5 <= bmi < 24.9:
                category = 'Normal weight'
            elif 25 <= bmi < 29.9:
                category = 'Overweight'
            else:
                category = 'Obese'
    else:
        form = BMICalculatorForm()

    return render(request, 'base/bmi.html', {'form': form, 'bmi': bmi, 'category': category})

from .form import CollegeForm
from .models import DietPlan

def select_college_view(request):
    form = CollegeForm()
    diet_plan = None

    if request.method == 'POST':
        form = CollegeForm(request.POST)
        if form.is_valid():
            college = form.cleaned_data['college']
            goal = form.cleaned_data['goal']
            diet_plan = DietPlan.objects.filter(college=college, goal=goal)

    return render(request, 'base/select_college.html', {
        'form': form,
        'diet_plan': diet_plan,
    })