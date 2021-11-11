from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from . models import Book
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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
            books_name = request.POST['books_name']
            books_img = request.POST['books_img']
            books_description= request.POST['books_description']
            if not user or not books_name or not books_img or not books_description:
                messages.error(request, 'All fields are mandatory')
                return redirect('create_book_record')
            data = Book(books_name=books_name, books_img=books_img, books_description=books_description, user=user)
            data.save()
            messages.info(request, 'New Book record created')
        except Exception as e:
            messages.error(request, e)
            return redirect('create_book_record')
    return render(request, 'create_book_record.html')