from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from . models import Book
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import BookForm

# Home view to view the homepage of the website
def home(request):
    data = Book.objects.order_by('-id')[:3]
    return render(request, 'home.html', {'data': data})

# Login view to get required credentials from the user
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

# Register view to create new user
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

# Logout view to logout from the site
def logout(request):
    auth.logout(request)
    return redirect('home')

# To retrieve all books
def all_books(request):
    data = Book.objects.all().order_by('-id')
    return render(request, 'all_books.html', {'data': data})

# To retrieve particular books
def author_books(request):
    data = Book.objects.filter(user=request.user).order_by('-id')
    return render(request, 'all_books.html', {'data': data})

# To create new records of the books
@login_required(login_url='login')
def create_book_record(request):
    if request.method == 'POST':
        try:
            user = request.user
            context = dict(backend_form=BookForm())
            form = BookForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                data = Book(books_name=form.cleaned_data['books_name'], books_img=form.cleaned_data['books_img'],
                            books_description=form.cleaned_data['books_description'], user=user)
                data.save()
            messages.info(request, 'New Book record created')
        except Exception as e:
            messages.error(request, e)
            return redirect('create_book_record')
    return render(request, 'create_book_record.html')

# To update a record in the database
def update_book_record(request, pk):
    books_data = Book.objects.get(id=pk)
    if books_data.user != request.user:
        return redirect('home')
    if request.method == 'POST':
        try:
            form = BookForm(request.POST, request.FILES, instance=books_data)
            if form.is_valid():
                books_data.books_name = form.cleaned_data['books_name'] if form.cleaned_data.get(
                    'books_name') else books_data.books_name
                books_data.books_img = form.cleaned_data['books_img'] if form.cleaned_data.get(
                    'books_img') else books_data.books_img
                books_data.books_description = form.cleaned_data['books_description'] if form.cleaned_data.get(
                    'books_description') else books_data.books_description
                books_data.save()
            messages.info(request, 'Book record updated')
        except Exception as e:
            messages.error(request, e)
            return redirect('create_book_record')

    return render(request, 'update_book_record.html', {'books_data': books_data})

# To remove the record from the database.
def delete_record(request, pk):
    books_data = Book.objects.get(id=pk)
    if books_data.user != request.user:
        return redirect('home')
    books_data.delete()
    messages.info(request, 'Book record deleted')
    return redirect('all_books')