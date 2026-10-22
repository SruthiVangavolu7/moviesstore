from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from cart.models import Item


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
        
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})
    
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})


@staff_member_required
def admin_top_purchaser(request):
    purchase_counts = ( 
        Item.objects
        .filter(order__user__is_staff= False)
        .values(
            username=F('order__user__username')
        )
        .annotate(
            total_movies=Sum('quantity')
        )
        .order_by(
            '-total_movies',
            'username'
        )
    )

    top_buyer= purchase_counts.first()
    template_data = {}
    template_data['title'] = 'Admin Dashboard'
    template_data['top_buyer'] = top_buyer
    template_data['purchase_counts'] = purchase_counts

    return render(
        request, 
        'accounts/admin_top_purchaser.html',
        {'template_data': template_data}
    )