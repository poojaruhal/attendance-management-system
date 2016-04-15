from django.contrib import admin
from django.contrib.auth.models import User
from basic import models

class StudentAdmin(admin.ModelAdmin):

	#exclude = ('student_id',)

	def get_queryset(self, request):
		qs = super(StudentAdmin, self).get_queryset(request)

		# If the user is a student then only show only one record
		if request.user.groups.filter(name="Students").exists():
			return qs.filter(user=request.user)
		return qs


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		"""Limit choices for 'user' field to only current user."""

		# Limit restriction for user field
		if db_field.name == 'user':

			# For student, user field can take current user 
			if request.user.groups.filter(name="Students").exists():
				kwargs["queryset"] = User.objects.filter(
				username=request.user)

		return super(StudentAdmin, self).formfield_for_foreignkey(
	db_field, request, **kwargs)



admin.site.register(models.Course)
admin.site.register(models.Room)
admin.site.register(models.Time)
admin.site.register(models.Semester)

admin.site.register(models.Student,StudentAdmin)
admin.site.register(models.Faculty)

admin.site.register(models.Department)
admin.site.register(models.Designation)


admin.site.register(models.CourseClass)
admin.site.register(models.Attendance)

admin.site.register(models.MarkingUnit)
admin.site.register(models.Report)

