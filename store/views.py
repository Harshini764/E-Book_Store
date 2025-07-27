from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def home(request):
    q = request.GET.get('q', '')
    if q:
        books = Book.objects.filter(title__icontains=q) | Book.objects.filter(author__icontains=q)
    else:
        books = Book.objects.all()
    return render(request, 'store/home.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'store/book_detail.html', {'book': book})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def add_to_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id not in cart:
        cart.append(book_id)
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'store/cart.html', {'books': books})

def remove_from_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id in cart:
        cart.remove(book_id)
        request.session['cart'] = cart
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    if request.method == 'POST':
        # Save ordered books info in session for success page
        request.session['ordered_books'] = list(cart)
        request.session['cart'] = []
        return redirect('order_success')
    return render(request, 'store/checkout.html', {'books': books})

def order_success(request):
    ordered_book_ids = request.session.get('ordered_books', [])
    books = Book.objects.filter(id__in=ordered_book_ids)
    # Clear ordered_books from session after displaying
    if 'ordered_books' in request.session:
        del request.session['ordered_books']
    return render(request, 'store/order_success.html', {'books': books})
