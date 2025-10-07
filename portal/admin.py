from django.contrib import admin
from .models import User, Announcement, Course, Department, Enrollment, Grade

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter  = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'matric_no', 'staff_id')
    ordering = ('username',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_field = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'unit', 'lecturer')
    list_filter = ('department',)
    search_fields = ('code', 'title')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'session', 'date_enrolled')
    list_filter = ('semester', 'session')
    search_fields = ('student__username', 'course__code')
    autocomplete_fields = ('student', 'course')

    @admin.register(Grade)
    class GradeAdmin(admin.ModelAdmin):
        list_display = ('enrollment', 'score', 'grade')
        search_fields = ('enrollment__student__username', 'enrollment__course__code')