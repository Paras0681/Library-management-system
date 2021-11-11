from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from . models import Book
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import cloudinary.uploader 
from django.conf import settings
from .forms import BookForm
# cloudinary.config(
#     cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
#     api_key = settings.CLOUDINARY_STORAGE['API_KEY'],
#     api_secret = settings.CLOUDINARY_STORAGE['API_SECRET']
# )

# Create your views here.
def home(request):
    data = Book.objects.order_by('-id')[:3]
    return render(request, 'home.html', {'data': data})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('all_books')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username Taken")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email-id Taken")
            return redirect('register')
        elif User.objects.filter(password=password).exists():
            messages.info(request, "Password Taken")
            return redirect('register')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            messages.info(request, 'New User created')
        return redirect('login')
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def all_books(request):
    data = Book.objects.all().order_by('-id')
    return render(request, 'all_books.html', {'data': data})



@login_required(login_url='login')
def create_book_record(request):
    if request.method == 'POST':
        try:
            user = request.user
            context = dict( backend_form = BookForm())
            form = BookForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                data = Book(books_name = form.cleaned_data['books_name'], books_img = form.cleaned_data['books_img'], books_description= form.cleaned_data['books_description'], user=user)
                data.save()
            messages.info(request, 'New Book record created')
        except Exception as e:
            messages.error(request, e)
            return redirect('create_book_record')
    return render(request, 'create_book_record.html')