from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import CustomUser
from company.models import Company
from student.models import Student, AppliedDrive


# Create your views here.
def student_home(request):
    return render(request, 'student.html')


def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        qualification = request.POST.get("qualification")
        tech_stack = request.POST.get("tech_stack")
        year_of_passing = request.POST.get("year_of_passing")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('add_student')

        # Create CustomUser
        user = CustomUser.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password,  # Auto hashed!
            user_type="student",
            is_staff=False,
            is_active=True,
        )

        # Create Student profile
        Student.objects.create(
            user=user,
            qualification=qualification,
            tech_stack=tech_stack,
            year_of_passing=year_of_passing,
            mobile=mobile
        )

        messages.success(request, "Student added successfully!")
        return redirect('view_students')
    return render(request, 'add_student.html',{ 'action':'Add'})



@login_required
def view_students(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'view_students.html', context)


@login_required(login_url='login')
def student_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        # Update User-related fields (Name, Email)
        student.user.first_name = request.POST.get('name')
        student.user.email = request.POST.get('email')


        # Handle Password Update
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password:
            if password == confirm_password:
                student.user.set_password(password)
            else:
                messages.error(request, "Passwords do not match!")
                return render(request, 'add_student.html', {'student': student, 'action': 'update'})

        student.user.save()

        # Update Student-specific fields
        student.qualification = request.POST.get('qualification')
        student.tech_stack = request.POST.get('tech_stack')
        student.year_of_passing = request.POST.get('year_of_passing')
        student.mobile = request.POST.get('mobile')
        student.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')
    return render(request, 'add_student.html', {'student': student, 'action': 'update'})



@login_required
def available_drives(request):
    user = request.user
    student = get_object_or_404(Student, user=user)

    # Convert student tech stack to lowercase list for match
    student_skills = [skill.strip().lower() for skill in student.tech_stack.split(',')]

    eligible_drives = []
    companies = Company.objects.filter(status="active")

    for c in companies:
        company_skills = [skill.strip().lower() for skill in c.tech_stack.split(',')]

        # Check skill match and YOP match
        if (
            any(skill in company_skills for skill in student_skills)
            # and c.year_of_passing == student.year_of_passing
        ):
            eligible_drives.append(c)

    applied = AppliedDrive.objects.filter(student=student).values_list("company_id", flat=True)

    return render(request, "available_drives.html", {
        "drives": eligible_drives,
        "applied": applied
    })


@login_required
def applied_drives(request):
    user = request.user
    student = get_object_or_404(Student, user=user)

    applied_drives = AppliedDrive.objects.filter(student=student)

    return render(request, "applied_drives.html", {
        "applied_drives": applied_drives
    })


@login_required
def update_student(request,id):
    student = get_object_or_404(Student, id=id)
    user = student.user
    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        student.qualification = request.POST.get('qualification')
        student.tech_stack = request.POST.get('tech_stack')
        student.year_of_passing = request.POST.get('year_of_passing')
        student.mobile = request.POST.get('mobile')
        user.email = request.POST.get('email')
        user.save()
        student.save()
        return redirect('view_students')
    return render(request, 'add_student.html', {'student': student, 'action': 'update'})


@login_required
def delete_student(request,id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('view_students')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('student_profile')
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'change_password.html')


@login_required
def apply_drive(request, company_id):
    user = request.user
    student = get_object_or_404(Student, user=user)
    company = get_object_or_404(Company, id=company_id)

    # Check if already applied
    if AppliedDrive.objects.filter(student=student, company=company).exists():
        messages.warning(request, "Already applied for this drive!")
        return redirect('available_drives')

    AppliedDrive.objects.create(student=student, company=company)
    messages.success(request, "Applied successfully!")
    return redirect('applied_drives')
