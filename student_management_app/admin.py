from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedBackStudent, FeedBackStaffs, NotificationStudent, NotificationStaffs

#test *****

#from .models import Author, Book
 
 # how the model will look like in the admin

#class BookInLineAdmin(admin.TabularInline):
#    model = Book
 
 
#class AuthorAdmin(admin.ModelAdmin):
#    inlines = [BookInLineAdmin]
 
 
#admin.site.register(Author, AuthorAdmin)
##admin.site.register(Author)
#fin test****


# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)
