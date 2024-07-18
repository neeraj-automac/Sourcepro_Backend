from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(error_messages={
        'blank': ' password_field_cannot_be_blank.'
    })

    email = serializers.CharField(error_messages={
        'blank': 'username_field_cannot_be_blank.'
    })



    class Meta:
            model = User
            fields = ('email', 'password')




class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=OTP
#         fields='__all__'


class Course_serializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        # fields = '__all__'
        fields= ['course_id',"thumbnail","course_name","total_duration"]

class Course_serializerr(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class course_name_serializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']




class usr_course_serializer(serializers.ModelSerializer):
    class Meta:
        model = usr_course
        fields = '__all__'
        # fields=["thumbnail", "course_name", "minutes_left", "percentage_completed"]


class usr_course_serializer2data(serializers.ModelSerializer):
    class Meta:
        model = usr_course
        fields = ['course_id','minutes_left','percentage_completed','last_viewed_lesson_id']

class usr_course_certificate_serializer(serializers.ModelSerializer):
    class Meta:
        model = usr_course
        fields = ['course_id','certificate_url']



class usr_course_course_page(serializers.ModelSerializer):
    class Meta:
        model = usr_course
        fields = ['user_id','course_id']

class QnA_serializer(serializers.ModelSerializer):
    class Meta:
        model = QnA
        fields = ['lesson_id','question_id','correct_answer']


class QnA_serializer2(serializers.ModelSerializer):
    class Meta:
        model = QnA
        fields = '__all__'


class Lessons_serializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['lesson_id', 'course_id', 'lesson_name', 'lesson_duration', 'lesson_url', 'pass_percentage',
                  'materials', 'clipboards','subtitle_file_link']


class User_Lessons_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Lessons
        fields = '__all__'


class User_Lessons_serializer_update_watch_time(serializers.ModelSerializer):
    class Meta:
        model = User_Lessons
        fields = ['minutes_completed']


class User_Lessons_material_serializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['material_url']
class User_Lessons_clipboard_serializer(serializers.ModelSerializer):
    class Meta:
        model = Clipboard
        fields = ['clipboard_url']


class User_Lessons_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Lessons
        fields = ['user_lesson_id','lesson_id','minutes_completed','minutes_left','lesson_status','quiz_score','quiz_attempt_status']
        # fields='__all__'

class User_lesson_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Lessons
        fields=['lesson_id','lesson_status','quiz_score','quiz_attempt_status']




class User_Lessons_quiz_score_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Lessons
        fields = ['quiz_score']



# class User_answers_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User_answers
#         fields = ['user_id', 'course_id', 'lesson_id', 'question_id', 'answer']
#
#
# class User_answers_serializer2(serializers.ModelSerializer):
#     class Meta:
#         model = User_answers
#         fields = '__all__'
#
#
# class User_answers_serializer3(serializers.ModelSerializer):
#     class Meta:
#         model = User_answers
#         fields = ['answer', 'status']


class user_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = '__all__'
class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

class like_seraializer(serializers.ModelSerializer):
    class Meta:
        model=usr_course
        fields ='__all__'

class FAQ_serializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields=['question','answer']


class User_create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        
class User_doj_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['date_joined']

class UserDetails_create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = ['user_id','name','contact_no','business_email','location','user_status']



class UserDetails_pagination_Serializer(serializers.ModelSerializer):
    #----in order to access other model fileds in same serializer u need to use nested serializer here we have
    date_joined = serializers.DateTimeField(source='user_id.date_joined', read_only=True)
    # date_joined = User_doj_Serializer(many=True, read_only=True)
    # print('--------------------date_joined',date_joined)
    # name = serializers.CharField()
    # contact_no = serializers.IntegerField()
    # user_status = serializers.CharField()
    # business_email = serializers.EmailField()
    # location = serializers.CharField()



    class Meta:

        model = User_details
        fields = ['date_joined','name','contact_no','user_status','business_email','location']

class UserDetails_business_email_Serializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='users.username', read_only=True)

    class Meta:
        model = User_details
        fields = ['name','id']



class TemplateDetails_pagination_Serializer(serializers.ModelSerializer):


    class Meta:

        model = Template
        fields = ["id","template_name","template_heading","template_body"]

class Template_dropdown_Serializer(serializers.ModelSerializer):




    class Meta:

        model = Template
        fields = ["id","template_name"]

class Broadcast_Serializer(serializers.ModelSerializer):
# In Django REST Framework, when you use serializers.SerializerMethodField(), it automatically looks for
# a method in the serializer class named get_ < field_name >
# In your case, since the field is named users, it looks for a method named get_users.so it is mandatory to name method as get_users
# if not named in such a way it raises a attribute error as no get_users






        # fields = [,,,,,,]
        # fields = '__all__'


        template = serializers.CharField(source='template.template_name', read_only=True)
        # users = serializers.CharField(source='users.business_email', read_only=True)

        template_id = serializers.CharField(source='template.id', read_only=True)
        users = serializers.SerializerMethodField()
        frequency = serializers.CharField()
        follow_up = serializers.CharField()
        time = serializers.TimeField()
        sent_status = serializers.BooleanField()

        class Meta:
            model = Broadcast
            fields=['id','template','template_id','users','frequency','follow_up','time','sent_status']

        def get_users(self, obj):
            # return [user.business_email for user in obj.users.all()]
            return [{'user_id': user.id, 'username': user.name} for user in obj.users.all()]


