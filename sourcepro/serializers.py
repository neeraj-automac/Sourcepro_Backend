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