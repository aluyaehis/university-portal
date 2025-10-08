# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Enrollment, Course, Announcement

# def home(request):
#     return render(request, 'home.html')

# @login_required
# def dashboard(request):
#     user = request.user

#     if user.role == 'student':
#         enrollments = Enrollment.objects.filter(student=user).select_related('course')
#         announcements = Announcement.objects.filter(department__in=[e.course.department for e in enrollments]).order_by('-created_at')[:5]
#         return render(request, 'dashboard_student.html', {'enrollments':enrollments, 'announcements':announcements})
#     elif user.role == 'teacher':
#         courses = Course.objects.filter(lecturer=user)
#         students = Enrollment.objects.filter(course__in=courses).select_related('student', 'course')
#         return render(request, 'dashboard_lecturer.html', {'courses':courses, 'students':students})
#     else:
#         total_students = Enrollment.objects.values('student').distinct().count()
#         total_course = Course.objects.count()
#         total_announcements = Announcement.objects.count()
#         return render(request, 'dashboard_admin.html', {'total_students':total_students, 'total_course':total_course, 'total_announcements':total_announcements})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment, Course, Announcement

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    user = request.user

    # 🧑‍🎓 Student Dashboard
    if user.role == 'student':
        enrollments = Enrollment.objects.filter(student=user).select_related('course')
        announcements = Announcement.objects.filter(
            target_role__in=['student', 'all']
        ).order_by('-date_created')[:5]

        return render(request, 'dashboard_student.html', {
            'enrollments': enrollments,
            'announcements': announcements
        })

    # 👨‍🏫 Teacher Dashboard
    elif user.role == 'teacher':
        courses = Course.objects.filter(lecturer=user)
        students = Enrollment.objects.filter(course__in=courses).select_related('student', 'course')
        announcements = Announcement.objects.filter(
            target_role__in=['teacher', 'all']
        ).order_by('-date_created')[:5]

        return render(request, 'dashboard_lecturer.html', {
            'courses': courses,
            'students': students,
            'announcements': announcements
        })

    # 🧑‍💼 Admin Dashboard
    else:
        total_students = Enrollment.objects.values('student').distinct().count()
        total_courses = Course.objects.count()
        total_announcements = Announcement.objects.count()

        return render(request, 'dashboard_admin.html', {
            'total_students': total_students,
            'total_courses': total_courses,
            'total_announcements': total_announcements
        })
