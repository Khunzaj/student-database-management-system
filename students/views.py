from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student

@login_required
def home(request):

    students = Student.objects.all()

    total_students = students.count()
    total_courses = students.values('course').distinct().count()
    total_semesters = students.values('semester').distinct().count()

    recent_students = students.order_by('-id')[:3]

    return render(request, 'students/home.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_semesters': total_semesters,
        'recent_students': recent_students,
    })


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})


def student_list(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(course__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query
    })

def student_detail(request, id):

    student = Student.objects.get(id=id)

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )

def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_student.html', {
        'form': form
    })


def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()

    return redirect('student_list')

def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'students/login.html',
        {'form': form}
    )

def user_logout(request):
    logout(request)
    return redirect('login')