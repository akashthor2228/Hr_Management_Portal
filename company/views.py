from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

import company
from company.models import Company
from student.models import AppliedDrive, Student


# Create your views here.


def company_home(request):
    return render(request, 'company.html')


def add_company(request):
   if request.method == "POST":
       company_name = request.POST.get('company_name')
       role = request.POST.get('role')
       salary = request.POST.get('salary')
       tech_stack = request.POST.get('tech_stack')
       address = request.POST.get('address')
       year_of_passing = request.POST.get('year_of_passing')


       Company.objects.create(
           company_name=company_name,
           role=role,
           salary=salary,
           tech_stack=tech_stack,
           address=address,
           year_of_passing=year_of_passing,
           added_by=request.user  # Auto capture logged-in user
       )


       # messages.success(request, "Company added successfully!")
       # --- Email Logic Starts ---
       subject = f"New Job Alert: {role} at {company_name}"
       message = f"""
                       Hey Aliens,

                       A new job opportunity has been posted in HrManagementPortal!

                       Company: {company_name}
                       Role: {role}
                       Tech Stack: {tech_stack}
                       Salary: {salary}
                       Year of Passing: {year_of_passing}

                       Login to the portal to apply now http://127.0.0.1:8000/ !
                       """

       # Get all students who match the Year of Passing
       # (You can add more logic here to filter by tech stack if needed)
       # eligible_students = Student.objects.filter(year_of_passing=year_of_passing)
       #
       # recipient_list = [student.user.email for student in eligible_students if student.user.email]

       all_students = Student.objects.all()

       recipient_list = [student.user.email for student in all_students if student.user.email]

       if recipient_list:
           send_mail(
               subject,
               message,
               settings.EMAIL_HOST_USER,
               recipient_list,
               fail_silently=True,  # Set to False if you want to see errors during debugging
           )
       # --- Email Logic Ends ---

       messages.success(request, "Company added and emails sent successfully!")

       return redirect('view_company')  # redirect to companies list


   return render(request, 'add_company.html',{"action":"add"})



def view_company(request):
   companies = Company.objects.all()
   for company in companies:
       company.auto_update_status()
   context = {
       'companies': companies
   }
   return render(request, 'view_company.html', context)


def update_company(request,id):
    company = get_object_or_404(Company, id=id)
    if request.method == "POST":
        company.company_name = request.POST.get('company_name')
        company.role = request.POST.get('role')
        company.salary = request.POST.get('salary')
        company.tech_stack = request.POST.get('tech_stack')
        company.address = request.POST.get('address')
        company.year_of_passing = request.POST.get('year_of_passing')
        company.save()
        return redirect('view_company')
    return render(request, 'add_company.html',{'action':'update',"company":company })


def delete_company(request,id):
    company = get_object_or_404(Company,id=id)
    company.delete()
    return redirect('view_company')


def view_applied_students(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    applied_students = AppliedDrive.objects.filter(company=company).select_related("student__user")

    return render(request, "view_applied_students.html", {
        "company": company,
        "applied_students": applied_students
    })
