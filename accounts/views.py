from django.contrib import messages
from django.contrib.admin import action
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache


# Create your views here.
# def dashboard():
#     return None
@never_cache
@login_required
def dashboard_view(request):
    return render(request,'dashboard.html')


CustomUser = get_user_model()


def add_employee(request):
    if request.method == "POST":
        username = request.POST.get('username')
        # age = request.POST.get('age')
        email = request.POST.get('email')
        # user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check password match
        if password != confirm_password:
            return render(request, 'add_employee.html')

        # Create User with selected user_type
        user = CustomUser(
            username=username,
            email=email,
            user_type='hr',
        )
        user.password = make_password(password)
        user.save()

        messages.success(request, "User Created Successfully!")
        return redirect('view_employee')

    return render(request, 'add_employee.html', {"password":True,"action":'Add'})



def view_employee(request):
    if request.user.user_type == 'admin':
        employees = CustomUser.objects.filter(user_type='hr')
        return render(request,'view_employee.html',{"employees":employees})
    return render(request,'view_employee.html',{"error":"you dont have permission"})


def employee_home(request):
    return render(request,'employee.html')

@never_cache
@login_required
def update_employee(request,id):
    employee = get_object_or_404(CustomUser,id=id)
    if request.method == "POST":
        employee.name = request.POST.get('username')
        employee.email = request.POST.get('email')
        employee.save()
        return redirect('view_employee')

    return render(request,'add_employee.html',{"password":False,"action":'Update',"employee":employee })


def delete_employee(request,id):
    employee = get_object_or_404(CustomUser,id=id)
    employee.delete()
    return redirect('view_employee')