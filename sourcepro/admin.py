from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class SampleAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UserDetailsInline(admin.StackedInline):
    model = User_details
    can_delete = False

class UserDetailsAdmin(AuthUserAdmin):
    list_display =['id','username']
    def add_view(self,*args,**kwargs):#for error
        self.inlines=[]
        return super(UserDetailsAdmin, self).add_view(*args, **kwargs)

    def change_view(self,*args,**kwargs):
        self.inlines =[UserDetailsInline]
        return super(UserDetailsAdmin, self).change_view(*args, **kwargs)


    #inlines=[UserProfileInline]






admin.site.unregister(User)
admin.site.register(User,UserDetailsAdmin)



# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id','username']


# @admin.register(UserDetailsAdmin)
# class UserDetailsAdminAdmin(admin.ModelAdmin):
#     list_display = ['id','username']



# admin.site.register(User_details)
@admin.register(User_details)
class User_detailsAdmin(admin.ModelAdmin):
    list_display = ['id','name']

# admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_name','course_status','type']

# admin.site.register(usr_course)
@admin.register(usr_course)
class usr_courseAdmin(admin.ModelAdmin):
    list_display = ['user_id','course_id','course_status']

# admin.site.register(Lessons)
@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['lesson_id','lesson_name','course_id_id','course_id']

# admin.site.register(User_Lessons)
@admin.register(User_Lessons)
class User_LessonsAdmin(admin.ModelAdmin):
    list_display = ['user_id_id','user_id','user_lesson_id','course_id_id','lesson_id_id','lesson_id']


# admin.site.register(FAQ)
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_id_id']


# admin.site.register(QnA)
@admin.register(QnA)
class QnAAdmin(admin.ModelAdmin):
    list_display = ['question_id','question_type','course_id_id','lesson_id_id']

# admin.site.register(Material)
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['lesson_id','lesson_id_id']

# admin.site.register(Clipboard)
@admin.register(Clipboard)
class ClipboardAdmin(admin.ModelAdmin):
    list_display = ['lesson_id','lesson_id_id']




