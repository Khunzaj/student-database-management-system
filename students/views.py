from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student


def home(request):
    recent_students = Student.objects.order_by('-id')[:3]
    total_students = Student.objects.count()

    return render(request, 'students/home.html', {
        'recent_students': recent_students,
        'total_students': total_students
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
