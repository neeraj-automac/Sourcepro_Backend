from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
import random
from . import models
from .models import *
import ast
from rest_framework.renderers import JSONRenderer
from django.core import serializers as core_serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
import json
from datetime import datetime, time, timedelta,date
from django.conf import settings
from django.db.models import Min, Max
from functools import reduce
from .tasks import*
# from datetime import date
# import datetime
# from datetime import datetime
# import datetime




# from rest_framework.utils.serializer_helpers import ReturnList



#################################################################################################################################################################################################################################################################################################################

#----------------------------##########-----------------------MY APIS-----------------------#######################---------------------------------------------



print('^^^^ in views ^^^^^^^')

#
# print(usr_course.objects.all())
tes_fun.apply_async()
@api_view(['GET'])
def download_certificate(request):
    # user_id= request.query_params.get('user_id')
    # user_id = request.query_params.get('user_id')
    # user_course_data=usr_course.objects.filter(user_id=2).values('course','certificate_url')
    # print(user_course_data)
    # # user_assigned_course_ids=[ i['course'] for i in user_course_data]
    # # user_course_certificates=Course.objects.filter(id__in=user_assigned_course_ids).values('certificate')
    # ser_course_data=usr_course_certificate_serializer(user_course_data,many=True)
    # print('ser_course_data',ser_course_data)
    # print( ser_course_data.data)
    # user_course_data = usr_course.objects.filter(user_id=2)

    # Create a list to hold the data for each course
    # course_data_list = []

    # Iterate through the queryset and extract the necessary fields for each course
    # for user_course in user_course_data:
    #     course_data = {
    #         'course': user_course.course,  # Assuming 'course' is a ForeignKey
    #         'certificate_url': user_course.certificate_url
    #     }
    #     course_data_list.append(course_data)
    #     for i in range(len(course_data_list)):
    #         course_value=course_data_list[i]['course']
    #         print(course_value)
    #         print(type(course_value))
    #         certificate_value= course_data_list[i]['certificate_url']
    # user_course_data = usr_course.objects.filter(user_id=2).values('course','certificate_url')
    # print('user_course_data',type(user_course_data[0]))
    # ser_course_data = usr_course_certificate_serializer(course_data_list, many=True)
    # print(ser_course_data.data[0]['course'])
    #
    # print(ser_course_data.data[0].keys())
    user_id = request.query_params.get('user_id')
    filter_data=usr_course.objects.filter(user_id=user_id)
    print(filter_data)
    print(type(filter_data))
    ser_filter_data=usr_course_serializer(filter_data,many=True)
    print('ser_filter_data',ser_filter_data)# returns all fields of model
    print('type----ser_filter_data',type(ser_filter_data))# <class 'rest_framework.serializers.ListSerializer'>
    ser_filter_data_data= ser_filter_data.data
    print('ser_filter_data_data',ser_filter_data_data)#order dict-----------
    print('****type***ser_filter_data_data',type(ser_filter_data_data))#return list

    for i in range(0,len(ser_filter_data_data)):
        print('-------------------------------------------------------------------------------------')
        print(i,ser_filter_data_data)
        print('&&&&&&&&--list$$$$$',list(ser_filter_data_data))
        print('@@@@@@@--listkeys@@@@@@@',list(ser_filter_data_data)[i].keys())#odict_keys
        print('-------------------------------------------------------------------------------------')
        for k in list(ser_filter_data_data[i].keys()):
            if k in ['course_id','certificate_url']:
                continue
            ser_filter_data_data[i].pop(k)
        print('after pop ser_filter_data_data',ser_filter_data_data)
        print('^^^^^^^^----type after pop ser_filter_data_data^^^^^^---------',type(ser_filter_data_data))#return_list

    for i in range(0,len(ser_filter_data_data)):
        filtered_data=Course.objects.filter(course_id=ser_filter_data_data[i]['course_id'])
        print('filtered_data',filtered_data)#queryset
        print('type of filtered_data',type(filtered_data))#queryset
        ser_filtered_data=Course_serializerr(filtered_data,many=True)
        ser_filtered_data_data=ser_filtered_data.data
        print('$$$$$$$$$$*****ser_filtered_data_data',ser_filtered_data_data)#orderdict
        print('type of ser_filtered_data_data',type(ser_filtered_data_data))#return_list
        ser_filter_data_data[i].update(course_id=ser_filtered_data_data[0]['course_name'])
        print('$$$$$$$$$$*****ser_filter_data_data', ser_filter_data_data)
        # crs=ser_filtered_data_data[1].pop('course_name')
        # ces=ser_filtered_data_data[i].pop('certificate_url')

    return JsonResponse({'course_certificate':ser_filter_data_data})











    # for i in range(0,len(ser_course_data.data)):
    #     print(i)



@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    # print('serializer:', serializer)
    # print('serializer_type:', type(serializer))
    if serializer.is_valid():
        print('serializer:', serializer)
        username = serializer.data.get('email')
        # print('serializer_username:', username)
        # print('type_serializer_username:', type(username))
        password = serializer.data.get('password')
        # print('serializer_password:', password)
        # user = User.objects.get(username=username)
        # print(user)
        user  = authenticate(username=username, password=password)
        # print('authenticate_user:', user)

        if  user is not None:
            # print("not none")
            login(request, user)
            print("logged in:", request.user.username)
            # print(request.user)
            # print(request.user.email)
            return JsonResponse({"status": "user_validated"})

        else:
            # print("none")
            return JsonResponse({"status": "unauthorized_user"})
    return JsonResponse({'status':'Invalid Credentials'})

@api_view(['GET'])
def logout_view(request):
    # print("entering logout")


    # print("loggedout",request.user.username)

    logout(request)
    request.session.flush()
    return JsonResponse({"status": "Logged_out"})


@api_view(['POST'])
def set_new_password_send_otp(request):

    # SCREEN 5-----------------

    print(request.data)
    # print(request.user)
    # a=User.objects.get(username='neerajpynam3@gmail.com')
    # a=request.data
    email = request.data.get('email')
    queryset=User.objects.filter(username=email).exists()
    # print('***querset',queryset)
    # print('*****email',email)
    if queryset:
        otp_code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        email_body = f'''<p>Hey, here is your One Time Password for password reset:{otp_code}</p>'''
        send_mail('Source_Pro  Email Verification Code', '', from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email, ], html_message=email_body)
        user = User_details.objects.get(business_email=email)
        # print(user)
        user.otp = otp_code
        user.save()
        return JsonResponse({'status':'OTP sent successfully'})
    return JsonResponse({"status":"Please_provide_valid_email"})




@api_view(['POST'])
def set_new_password(request):

    #SCREEN 6,7 -----------------

    # if request.user.is_authenticated:
        # user=request.user
    email=request.data['email']
    queryset = User.objects.filter(username=email).exists()
    if queryset:

        user_business_email = User_details.objects.get(business_email=email)
        user_business_email_otp=user_business_email.otp
        # print('otppppppp', user_business_email_otp)
        if user_business_email_otp==request.data['otp']:
            current_user=User.objects.get(username=user_business_email)
            current_password=User.objects.get(username=user_business_email).password
            # print('current_password',current_password)
            # print('newpassword_hashed',make_password(request.data['password']))
            # print(check_password(request.data['password'],current_password ))
            if not check_password(request.data['password'],current_password):
                # print(check_password(current_password,request.data['password']))
                # print("setting password")
                current_user.set_password(request.data['password'])
                current_user.save()
                return JsonResponse({"status": "Successfull"})


            return JsonResponse({"status":"current_password_cannot_be_set_as_new_password"})


        # print('wrong otp')
        return JsonResponse({"status":"Invalid_OTP"})

    else:
        # print("wrong")
       return JsonResponse({"status": "Invalid_email_id"})
    # else:
    #     return JsonResponse({"status":"unauthorized_user"})


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def home(request):
    # SCREEN 8-----------
    # print(Course.objects.filter(course=2))
    if request.user.is_authenticated:
        new_courses = Course.objects.filter(type="new")
        new_courses_serializer= Course_serializer(new_courses, many=True)
        print("new_courses_serializer:::::",new_courses_serializer.data,new_courses)

        old_courses = Course.objects.filter(type="old")
        old_courses_serializer = Course_serializer(old_courses, many=True)
        print("old_courses_serializer:::::", old_courses_serializer,old_courses)

        # user_id = request.user
        user_id = 2
        inprogress = usr_course.objects.filter(user_id = user_id ,course_status='Inprogress')
        # print('2222222222222',inprogress)


        continue_learning = usr_course_serializer2data(inprogress, many=True)
        # print('continue_learning',continue_learning)
        continue_learning_data=continue_learning.data
        # print('continue_learning_data',continue_learning_data)
        # print(inprogress[0].course_id.thumbnail)
        for i in range(0, len(continue_learning.data)):
            continue_learning_data[i].update({'thumbnail':inprogress[i].course_id.thumbnail, 'course_name':inprogress[i].course_id.course_name})
        # print('continue_learning_data********',continue_learning_data)

        return JsonResponse({"Continue_Learning": continue_learning_data,
                             "New_Courses": new_courses_serializer.data,
                             "All_Courses":old_courses_serializer.data })#
    else:
        return JsonResponse({"status":"unauthorized_user"})
#
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def mycourses(request):
    # screens 9,10
    # print('8888888',usr_course.objects.filter(course_id=2),request.user)

    if request.user.is_authenticated:
        user_id = request.user #expects user_id
        # user_id = 2 #expects user_id
        info1 = usr_course.objects.filter(user_id = user_id, deactivation_days_left = 0) #this belongs to history tab
        serializer1 = usr_course_serializer(info1, many=True)

        info2 = usr_course.objects.filter(user_id = user_id,deactivation_days_left__in = range(1,100), course_status = "Completed") #this bwelongs to History tab
        serializer2 = usr_course_serializer(info2, many = True)
        # print('info2',info2)
        info3 = usr_course.objects.filter(user_id = user_id, deactivation_days_left__in = range(1,100), course_status = "Inprogress") #this belongs to in progress tab
        serializer3 = usr_course_serializer(info3, many = True)


        for i in range(0, len(serializer1.data)):
            for k in list(serializer1.data[i].keys()):
                if k in ["subscription_datetime", "deactivation_days_left", "course_id", "course_status",'last_viewed_lesson_id']:
                    continue
                else:
                    serializer1.data[i].pop(k)

        for i in range(0, len(serializer1.data)):
            # print('len',serializer2.data)
            a = Course.objects.filter(course_id=serializer1.data[i]["course_id"])
            aa = Course_serializerr(a, many=True)
            # print("aa-----------------------", aa.data)
            serializer1.data[i].update(course_name=aa.data[0]["course_name"])
            serializer1.data[i].update(thumbnail=aa.data[0]["thumbnail"])
            serializer1.data[i].update(author=aa.data[0]["author"])
            serializer1.data[i].update(activation_duration=(Course.objects.get(course_id=serializer1.data[i]["course_id"])).activation_duration)
            # serializer1.data[i].update({"lesson_id": 1})
        for i in range(0, len(serializer2.data)):
            for k in list(serializer2.data[i].keys()):
                if k in ["subscription_datetime", "deactivation_days_left", "course_id", "course_status",'last_viewed_lesson_id']:
                    continue
                else:
                    serializer2.data[i].pop(k)

        for i in range(0, len(serializer2.data)):
            a = Course.objects.filter(course_id=serializer2.data[i]["course_id"])
            aa = Course_serializerr(a, many=True)
            serializer2.data[i].update(course_name=aa.data[0]["course_name"])
            serializer2.data[i].update(thumbnail=aa.data[0]["thumbnail"])
            serializer2.data[i].update(author=aa.data[0]["author"])
            serializer2.data[i].update(activation_duration=(Course.objects.get(course_id=serializer2.data[i]["course_id"])).activation_duration)
            # serializer2.data[i].update({"lesson_id": 1})
        # print("type-----------",type(serializer2.data))

        # print("----------serializer3----------------------",serializer3.data)
        for i in range(0, len(serializer3.data)):
            for k in list(serializer3.data[i].keys()):
                if k in ["subscription_datetime", "deactivation_days_left", "percentage_completed", "minutes_left","course_id",'last_viewed_lesson_id']:
                    continue
                else:
                    serializer3.data[i].pop(k)

        for i in range(0, len(serializer3.data)):
            a = Course.objects.filter(course_id=serializer3.data[i]["course_id"])
            aa = Course_serializerr(a, many=True)
            serializer3.data[i].update(course_name=aa.data[0]["course_name"])
            serializer3.data[i].update(thumbnail=aa.data[0]["thumbnail"])
            serializer3.data[i].update(author=aa.data[0]["author"])
            serializer3.data[i].update(activation_duration=(Course.objects.get(course_id=serializer3.data[i]["course_id"])).activation_duration)
            # serializer3.data[i].update({"lesson_id":1})

        # print('serializer2.data',serializer2.data)
        serializer1_data=list(serializer1.data)
        serializer2_data=list(serializer2.data)
        history_data=serializer1_data+serializer2_data
        # print('history_data',history_data)

        # dict(serializer1.data).update(dict(serializer2.data))
        return JsonResponse({"In_Progress":serializer3.data, "History":history_data})
        # return JsonResponse({"In_Progress":serializer3.data, "History":serializer1.data})
    else:
        return JsonResponse({"status":"unauthorized_user"})



@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def Next_lesson(request):
    if request.user.is_authenticated:
        course_id= request.query_params.get('course_id')
        lesson_id= request.query_params.get('lesson_id')
        # next_lesson_id=int(lesson_id)+1
        user_lesson_queryset=Lessons.objects.filter(course_id=course_id,lesson_id__gt=lesson_id).order_by('lesson_id').first()

        if user_lesson_queryset is not None:


            return JsonResponse({"course_id":user_lesson_queryset.course_id.pk,"next_lesson_id" :user_lesson_queryset.lesson_id})

        else:
            return JsonResponse({"status":"Invalid_lesson_id_or_course_id"})
    else:
        return JsonResponse({"status": "unauthorized_user"})



@api_view(['GET'])#api for course data in course page
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def usr_course_page(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            user_id=request.user

            # user_id=2
            # print(request.user)
            course_id = request.query_params.get('course_id')
            lesson_id = request.query_params.get('lesson_id')

            current_user_courses=usr_course.objects.filter(user_id=user_id,course_id=course_id)
            if current_user_courses.exists():

                # print('current_user_courses',current_user_courses)
                # print("ccccc", current_user_courses[0].course_id.course_name)

                serializer=usr_course_course_page(current_user_courses,many=True)
                serializer_data=serializer.data
                # print(serializer_data)
                course_data_result={}



                for i in range(0,len(serializer_data)):

                    course_data_result.update({
                        "course_name":current_user_courses[i].course_id.course_name,
                        "course_description":current_user_courses[i].course_id.course_description,
                        "author":current_user_courses[i].course_id.author,
                        "creation_date":current_user_courses[i].course_id.created_date,
                        "course_likes":current_user_courses[i].course_id.likes,
                        "course_views":current_user_courses[i].course_id.views,
                        "like_status":current_user_courses[i].like_status
                        # "faq_question":faq_queryset[i].question

                    })


                return JsonResponse({'course_data':course_data_result})#,'lesson_data':lesson_details_serializer_data,'materials':current_user_lesson_material_serializer_data,'clipboards':current_user_lesson_clipboard_serializer_data
            return JsonResponse({'status':'Invalid_course_id_or_lesson_id'})
        else:
            pass

    else:
        return JsonResponse({"status":"unauthorized_user"})



def course_page_lesson_id(user_id,course_id,lesson_id):
    # user_id = request.query_params.get('user_id')
    # course_id = request.query_params.get('course_id')
    # lesson_id = request.query_params.get('lesson_id')
    # print(user_id, course_id, lesson_id)

    # -----current lesson data
    current_user_lesson = User_Lessons.objects.get(user_id=user_id, course_id=course_id,
                                                   lesson_id=lesson_id)
    # print('current_user_lesson', current_user_lesson, current_user_lesson.lesson_id.lesson_name,current_user_lesson.lesson_id.lesson_url, current_user_lesson.lesson_id.lesson_duration)
    lesson_details_serializer = User_Lessons_info_serializer(current_user_lesson)
    lesson_details_serializer_data = lesson_details_serializer.data
    adding_lesson_data = {'lesson_name': current_user_lesson.lesson_id.lesson_name,
                          'lesson_url': current_user_lesson.lesson_id.lesson_url,
                          'lesson_duration': current_user_lesson.lesson_id.lesson_duration,
                          'lesson_subtitle':current_user_lesson.lesson_id.subtitle_file_link

                          }  # 'lesson_material':current_user_lesson.course_lesson_id.material_url
    lesson_details_serializer_data.update(adding_lesson_data)
    # print('lesson_details_serializer.data)))))', lesson_details_serializer.data)
    # print('lesson_details_serializer.data)))))', type(lesson_details_serializer.data))

    current_user_lesson_material = Material.objects.filter(lesson_id=lesson_id)
    # print('current_user_lesson_material:::', current_user_lesson_material)
    current_user_lesson_material_serializer = User_Lessons_material_serializer(current_user_lesson_material,
                                                                               many=True)
    current_user_lesson_material_serializer_data = current_user_lesson_material_serializer.data
    # print('current_user_lesson_material_serializer', current_user_lesson_material_serializer_data, '^^^^^^')

    current_user_lesson_clipboard = Clipboard.objects.filter(lesson_id=lesson_id)
    # print('current_user_lesson_clipboard:::', current_user_lesson_clipboard)
    current_user_lesson_clipboard_serializer = User_Lessons_clipboard_serializer(current_user_lesson_clipboard,
                                                                                 many=True)
    current_user_lesson_clipboard_serializer_data = current_user_lesson_clipboard_serializer.data
    # print('current_user_lesson_clipboard_serializer_data', current_user_lesson_clipboard_serializer_data, '^^^^^^')

    lesson_material_list = []
    lesson_clipboard_list = []

    # material data
    for i in range(0, len(current_user_lesson_material)):
        # print(len(current_user_lesson_material_serializer_data))
        lesson_material_list.append(current_user_lesson_material_serializer_data[i]['material_url'])
    # lesson_material_list.append({'material_name': current_user_lesson.lesson_id.lesson_name})-------manual material name
    lesson_details_serializer_data.update({'materials': lesson_material_list})

    # clipboard data
    for i in range(0, len(current_user_lesson_clipboard)):
        lesson_clipboard_list.append(current_user_lesson_clipboard_serializer_data[i]['clipboard_url'])
    # lesson_clipboard_list.append({'clipboard_name': current_user_lesson.lesson_id.lesson_name})#---------manual key value for clipboard name
    lesson_details_serializer_data.update({'clipboards': lesson_clipboard_list})

    all_lessons_data = []
    all_lessons_data.append(lesson_details_serializer_data)

    all_lesson_queryset = User_Lessons.objects.filter(user_id=user_id, course_id=course_id)
    # print('all_lesson_queryset', all_lesson_queryset)
    # print('current_user_lesson_lesson_name', all_lesson_queryset[0].lesson_id.lesson_name)

    all_lesson_details_serializer = User_lesson_data_serializer(all_lesson_queryset, many=True)
    all_lesson_details_serializer_data = all_lesson_details_serializer.data
    # print('all_lesson_details_serializer', all_lesson_details_serializer_data)

    for i in range(0, len(all_lesson_queryset)):
        # print('current_user_lesson lesson name', all_lesson_queryset[i].lesson_id.lesson_name)
        # print('current_user_lesson lesson duration', current_user_lesson[i].course_lesson_id.lesson_duration)
        # print('current_user_lesson lesson video', current_user_lesson[i].course_lesson_id.lesson_url)
        all_lesson_details_serializer_data[i].update({
            'lesson_name': all_lesson_queryset[i].lesson_id.lesson_name,
            'lesson_duration': all_lesson_queryset[i].lesson_id.lesson_duration,
            # 'lesson_duration': current_user_lesson[i].course_lesson_id.lesson_duration,
            # 'lesson_video':current_user_lesson[i].course_lesson_id.lesson_url

        })
    # print('all_lesson_details_serializer_after_adding_lesson_name', all_lesson_details_serializer_data)
    for i in range(0, len(all_lesson_details_serializer_data)):
        # print(all_lesson_details_serializer_data[i]['lesson_id'])
        if all_lesson_details_serializer_data[i]['lesson_id'] == int(lesson_id):
            # print('True')
            # print('111111111111', type(all_lesson_details_serializer_data[i]))
            # print('2', type(lesson_details_serializer_data))
            all_lesson_details_serializer_data[i] = lesson_details_serializer_data
            # print(all_lesson_details_serializer_data)
        else:
            # print('False')
            pass
            # return JsonResponse({'status': 'Invalid_lesson_id'})

    # return JsonResponse({'all_lessons': all_lesson_details_serializer_data})
    return  all_lesson_details_serializer_data



@api_view(['GET', 'PUT'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def usr_course_page_lesson(request):
    if request.user.is_authenticated:
        if request.method=='PUT':
            course_id=request.data.get('course_id')
            lesson_id = request.data.get('lesson_id')
            print('000',request.data)
            print('1111111',type(request.data.get('minutes_completed')))
            print('1111111',request.data.get('minutes_completed')=="")
            user_id=  request.user
            # user_id= 2
            if lesson_id != '' and request.data.get('minutes_completed')!='':
                # print('lesson_id',lesson_id,type(lesson_id))
                l = request.data
                # print('lllllllll', l)
                lesson_watch_time = request.data.get('minutes_completed')

                d_lesson_watch_time = datetime.datetime.strptime(lesson_watch_time, '%H:%M:%S').time()
                # print('d_lesson_watch_time', d_lesson_watch_time, type(d_lesson_watch_time))
                # lesson_watch_time=d_lesson_watch_time

                # print('???', lesson_watch_time, type(lesson_watch_time))
                converted_lesson_watch_time = {'minutes_completed': d_lesson_watch_time}

            # l=request.data

            #----watch time  and minutes left SAVING

                old_watch_time = User_Lessons.objects.get(user_id=user_id,lesson_id=lesson_id,course_id=course_id)
                print("old_watch_time",old_watch_time)
                total_duration_of_lesson=old_watch_time.lesson_id.lesson_duration
                # print('total_duration_of_lesson',total_duration_of_lesson,type(total_duration_of_lesson))
                if old_watch_time is not None:
                    # print('old_watch_time', old_watch_time.minutes_completed,type(old_watch_time.minutes_completed))
                    old_watch_time_serializer = User_Lessons_serializer_update_watch_time(old_watch_time,
                                                                                          data=converted_lesson_watch_time)

                    if old_watch_time_serializer.is_valid():
                        old_watch_time_serializer.save()
                        queryset=usr_course.objects.get(user_id=user_id,course_id=course_id)
                        # print('*********',queryset.last_viewed_lesson_id)
                        # print('******',queryset.last_viewed_lesson_duration)
                        # print()
                        queryset.last_viewed_lesson_id=int(lesson_id)
                        queryset.last_viewed_lesson_duration=d_lesson_watch_time
                        queryset.save()

                        user_last_watched_course = User_details.objects.get(user_id=user_id)
                        # print('user_last_watched_course setting to None', user_last_watched_course)
                        # print(user_last_watched_course.course_id)
                        user_last_watched_course.course_id = int(course_id)
                        user_last_watched_course.save()


                        if total_duration_of_lesson >= d_lesson_watch_time:
                            # print(total_duration_of_lesson,d_lesson_watch_time)

                            # print('minutes_left--------------',datetime.datetime.strptime(str(total_duration_of_lesson), '%H:%M:%S') - datetime.datetime.strptime(str(d_lesson_watch_time), '%H:%M:%S'))
                            # print('type_minutes_left--------------',type(datetime.datetime.strptime(str(total_duration_of_lesson), '%H:%M:%S') - datetime.datetime.strptime(str(d_lesson_watch_time), '%H:%M:%S')))
                            # print(total_duration_of_lesson,type(total_duration_of_lesson),d_lesson_watch_time,type(d_lesson_watch_time))
                            common_date = datetime.datetime(1970, 1, 1)
                            total_duration_dt = common_date.replace(hour=total_duration_of_lesson.hour,
                                                                    minute=total_duration_of_lesson.minute,
                                                                    second=total_duration_of_lesson.second)
                            # print('total_duration_dt',total_duration_dt,type(total_duration_dt))

                            d_lesson_watch_dt = common_date.replace(hour=d_lesson_watch_time.hour,
                                                                    minute=d_lesson_watch_time.minute,
                                                                    second=d_lesson_watch_time.second)
                            # print('d_lesson_watch_dt', d_lesson_watch_dt,type(d_lesson_watch_dt))
                            # print("type!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",type(total_duration_dt),type(d_lesson_watch_dt))
                            # Calculate the time difference as a timedelta
                            time_difference = total_duration_dt - d_lesson_watch_dt
                            # print('time_difference',time_difference,type(time_difference))

                            # Convert the timedelta to a datetime.datetime object with a common date
                            time_difference_datetime = common_date + time_difference
                            # print('time_difference_datetime',time_difference_datetime,type(time_difference_datetime))

                            # Extract the time component as a datetime.time object
                            new_watch_time_minutes_left = time_difference_datetime.time()

                            # Print the time difference as a datetime.time object
                            # print('{{{}}}}}',new_watch_time_minutes_left,type(new_watch_time_minutes_left))
                            # print(old_watch_time.minutes_left)
                            # print('before saving',old_watch_time.minutes_left)
                            old_watch_time.minutes_left=new_watch_time_minutes_left
                            old_watch_time.save()
                            # print('after saving',old_watch_time.minutes_left)

                            course_lessons=User_Lessons.objects.filter(user_id=user_id,course_id=course_id)

                            # print('course_lessons',course_lessons[0].minutes_completed,course_lessons[0].minutes_completed)
                            list_of_minutes_completed=[]
                            list_of_total_duration=[]
                            print("lennnnnnnnnnnnn",len(course_lessons))
                            for i in range(len(course_lessons)):
                                # print(course_lessons[i].minutes_completed.hour,course_lessons[i].minutes_completed.minute,course_lessons[i].minutes_completed.second)
                                #
                                # print('lesson and its total duration',course_lessons[i].lesson_id.lesson_name,course_lessons[i].lesson_id.lesson_duration)
                                print("iiiiiiiiiiiii",i)
                                total_duration_timedelta_object=timedelta(hours=course_lessons[i].lesson_id.lesson_duration.hour,minutes=course_lessons[i].lesson_id.lesson_duration.minute,seconds=course_lessons[i].lesson_id.lesson_duration.second)
                                minutes_completed_timedelta_object = timedelta(hours=course_lessons[i].minutes_completed.hour,minutes=course_lessons[i].minutes_completed.minute,seconds=course_lessons[i].minutes_completed.second)
                                print('timedelta_object',minutes_completed_timedelta_object)

                                list_of_total_duration.append(total_duration_timedelta_object)
                                list_of_minutes_completed.append(minutes_completed_timedelta_object)
                            print("list------------------",list_of_total_duration)
                            # print(list_of_minutes_completed)
                            all_lessons_minutes_completed=reduce(lambda n,m:n+m,list_of_minutes_completed)
                            print('all_lessons_minutes_completed',all_lessons_minutes_completed)
                            course_total_duration=reduce(lambda a,b:a+b,list_of_total_duration)
                            # print('course_total_duration',course_total_duration,type(course_total_duration))
                            # print('reducing_minutes_completed',all_lessons_minutes_completed,type(all_lessons_minutes_completed))
                            # print((common_date+course_total_duration-all_lessons_minutes_completed).time())
                            course_minutes_left_datetime=common_date + course_total_duration - all_lessons_minutes_completed
                            course_minutes_left_time=course_minutes_left_datetime.time()
                            print('/////course_minutes_left for a course////////',course_minutes_left_time,type(course_minutes_left_time))
                            # print((common_date+course_total_duration).time())
                            course_total_duration_date_time=common_date+course_total_duration
                            course_total_duration_time=course_total_duration_date_time.time()
                            print('^^^^^^^^ dynamic total course duration^^^^^^^^^^^^',course_total_duration_time)
                            course_minutes_completed_datetime=common_date+all_lessons_minutes_completed
                            course_minutes_completed_time=course_minutes_completed_datetime.time()
                            # print('$$$$$$$$$ course_minutes_completed for a course $$$$$$$$', course_minutes_completed_time,type(course_minutes_completed_time))

                            user_course_queryset=usr_course.objects.get(user_id=user_id,course_id=course_id)
                            # user_course_queryset=usr_course.objects.get(user=request.user,course=course_id)
                            # print('user_course_queryset',user_course_queryset)

                            user_course_queryset.minutes_left=course_minutes_left_time
                            # print('user_course_queryset.minutes_left',user_course_queryset.minutes_left)
                            user_course_queryset.minutes_Completed = course_minutes_completed_time
                            # print('user_course_queryset.minutes_completed', user_course_queryset.minutes_Completed)



                            # Calculate the total seconds for both time objects
                            total_duration_of_course_seconds = course_total_duration_time.hour * 3600 + course_total_duration_time.minute * 60 + course_total_duration_time.second
                            minutes_completed_of_course_seconds = course_minutes_completed_time.hour * 3600 + course_minutes_completed_time.minute * 60 + course_minutes_completed_time.second

                            # Calculate the percentage of completion
                            percentage_completion = (minutes_completed_of_course_seconds / total_duration_of_course_seconds) * 100
                            # print(percentage_completion)
                            user_course_queryset.percentage_completed=percentage_completion
                            user_course_queryset.save()

                            course_queryset_total_duration=Course.objects.get(course_id=course_id)
                            # print('course_queryset_total_duration',course_queryset_total_duration)
                            course_queryset_total_duration.total_duration=course_total_duration_time
                            course_queryset_total_duration.save()
                            return JsonResponse({'status': 'watch_time_updated'})

                        else:
                            # print('******cant substract as minutes completed is greater than total duration of lesson ******')
                            return JsonResponse({'status':'cant_substract_as_minutes_completed_is_greater_than_total_duration_of_lesson'})


                    else:
                        # print('serializer_is_not_valid')
                        # print(old_watch_time_serializer.errors)
                        return JsonResponse({'status':old_watch_time_serializer.errors})

                else:
                    return JsonResponse({'status': 'Invalid_course_id_or_lesson_id'})
            elif lesson_id=='':
                # print("*********saving empty lesson id********")
                queryset = usr_course.objects.get(user_id=user_id,course_id=course_id)
                # print('*********', queryset.last_viewed_lesson_id)
                # print('******', queryset.last_viewed_lesson_duration)

                queryset.last_viewed_lesson_id = None
                queryset.last_viewed_lesson_duration = time(0,0,0)
                queryset.save()


                return JsonResponse({"status":"storing_empty_lesson_id_and_watch_time_00:00:00_for_user"})

        # elif request.method=="GET" and  request.query_params.get('lesson_id')=='':
        #     # print('--------dataaaaaaaaaaaaaaaaaa--------', type(request.query_params.get('lesson_id')))
        #     # print('--------dataaaaaaaaaaaaaaaaaa--------', request.query_params.get('lesson_id')=="")
        #     # print('--------dat--------', type(request.query_params.get('course_id')))
        #
        #     user_id = 2
        #     # user_id = request.user
        #     course_id = request.query_params.get('course_id')
        #
        #     # lesson_id_query_set = User_Lessons.objects.filter(user_id=user_id, course=course_id).values('course_lesson_id')
        #     lesson_id_query = User_Lessons.objects.filter(user_id=user_id, course_id=course_id)
        #     # print('lesson_id_query',lesson_id_query)
        #     if lesson_id_query.exists():
        #         lesson_id_query_set=lesson_id_query.aggregate(Min('lesson_id'))
        #         # print('lesson_id_query_set',lesson_id_query_set['lesson_id__min'])
        #         lesson_id = lesson_id_query_set['lesson_id__min']
        #         # print('lesson_id_query_set',lesson_id_query_set.aggregate(Min('course_lesson_id')))
        #         # print('user_id',user_id,'course_id' ,course_id,'lesson_id', lesson_id)
        #         u=usr_course.objects.get(user_id=user_id,course_id=course_id)
        #         # print('uuuuu',u)
        #         print(u.last_viewed_lesson_id, type(u.last_viewed_lesson_duration))
        #         if u is not None:
        #             print(u.last_viewed_lesson_id,type(u.last_viewed_lesson_duration))
        #             if u.last_viewed_lesson_id is None and u.last_viewed_lesson_duration==time(0,0,0):
        #                 print('--------------------No lesson_id in db and time zero---------------------')
        #
        #                 # -----current lesson data
        #                 try:
        #                     data = course_page_lesson_id(user_id, course_id, lesson_id)
        #                     return JsonResponse({'all_lessons': data})
        #                 except:
        #                     return JsonResponse({'status':'Invalid_user_id_or_course_id_or_lesson_id'})
        #                 # current_user_lesson = User_Lessons.objects.get(user_id=user_id, course=course_id,
        #                 #                                                course_lesson_id=lesson_id)
        #                 # print('current_user_lesson', current_user_lesson, current_user_lesson.course_lesson_id.lesson_name,
        #                 #       current_user_lesson.course_lesson_id.lesson_url, current_user_lesson.course_lesson_id.lesson_duration)
        #                 # lesson_details_serializer = User_Lessons_info_serializer(current_user_lesson)
        #                 # lesson_details_serializer_data = lesson_details_serializer.data
        #                 # adding_lesson_data = {'lesson_name': current_user_lesson.course_lesson_id.lesson_name,
        #                 #                       'lesson_url': current_user_lesson.course_lesson_id.lesson_url,
        #                 #                       'lesson_duration': current_user_lesson.course_lesson_id.lesson_duration}  # 'lesson_material':current_user_lesson.course_lesson_id.material_url
        #                 # lesson_details_serializer_data.update(adding_lesson_data)
        #                 # print('lesson_details_serializer.data)))))', lesson_details_serializer.data)
        #                 # print('lesson_details_serializer.data)))))', type(lesson_details_serializer.data))
        #                 #
        #                 # current_user_lesson_material = Material.objects.filter(lesson=lesson_id)
        #                 # print('current_user_lesson_material:::', current_user_lesson_material)
        #                 # current_user_lesson_material_serializer = User_Lessons_material_serializer(current_user_lesson_material,
        #                 #                                                                            many=True)
        #                 # current_user_lesson_material_serializer_data = current_user_lesson_material_serializer.data
        #                 # print('current_user_lesson_material_serializer', current_user_lesson_material_serializer_data, '^^^^^^')
        #                 #
        #                 # current_user_lesson_clipboard = Clipboard.objects.filter(lesson=lesson_id)
        #                 # print('current_user_lesson_clipboard:::', current_user_lesson_clipboard)
        #                 # current_user_lesson_clipboard_serializer = User_Lessons_clipboard_serializer(current_user_lesson_clipboard,
        #                 #                                                                              many=True)
        #                 # current_user_lesson_clipboard_serializer_data = current_user_lesson_clipboard_serializer.data
        #                 # print('current_user_lesson_clipboard_serializer_data', current_user_lesson_clipboard_serializer_data,
        #                 #       '^^^^^^')
        #                 #
        #                 # lesson_material_list = []
        #                 # lesson_clipboard_list = []
        #                 #
        #                 # # material data
        #                 # for i in range(0, len(current_user_lesson_material)):
        #                 #     print(len(current_user_lesson_material_serializer_data))
        #                 #     lesson_material_list.append(current_user_lesson_material_serializer_data[i]['material_url'])
        #                 # lesson_details_serializer_data.update({'materials': lesson_material_list})
        #                 #
        #                 # # clipboard data
        #                 # for i in range(0, len(current_user_lesson_clipboard)):
        #                 #     lesson_clipboard_list.append(current_user_lesson_clipboard_serializer_data[i]['clipboard_url'])
        #                 # lesson_details_serializer_data.update({'clipboards': lesson_clipboard_list})
        #                 #
        #                 # all_lessons_data = []
        #                 # all_lessons_data.append(lesson_details_serializer_data)
        #                 #
        #                 # all_lesson_queryset = User_Lessons.objects.filter(user_id=user_id, course=course_id)
        #                 # print('all_lesson_queryset', all_lesson_queryset)
        #                 # print('current_user_lesson_lesson_name', all_lesson_queryset[0].course_lesson_id.lesson_name)
        #                 #
        #                 # all_lesson_details_serializer = User_lesson_data_serializer(all_lesson_queryset, many=True)
        #                 # all_lesson_details_serializer_data = all_lesson_details_serializer.data
        #                 # print('all_lesson_details_serializer', all_lesson_details_serializer_data)
        #                 #
        #                 # for i in range(0, len(all_lesson_queryset)):
        #                 #     print('current_user_lesson lesson name', all_lesson_queryset[i].course_lesson_id.lesson_name)
        #                 #     # print('current_user_lesson lesson duration', current_user_lesson[i].course_lesson_id.lesson_duration)
        #                 #     # print('current_user_lesson lesson video', current_user_lesson[i].course_lesson_id.lesson_url)
        #                 #     all_lesson_details_serializer_data[i].update({
        #                 #         'lesson_name': all_lesson_queryset[i].course_lesson_id.lesson_name,
        #                 #         'lesson_duration': all_lesson_queryset[i].course_lesson_id.lesson_duration,
        #                 #         # 'lesson_duration': current_user_lesson[i].course_lesson_id.lesson_duration,
        #                 #         # 'lesson_video':current_user_lesson[i].course_lesson_id.lesson_url
        #                 #
        #                 #     })
        #                 # print('all_lesson_details_serializer_after_adding_lesson_name', all_lesson_details_serializer_data)
        #                 # for i in range(0, len(all_lesson_details_serializer_data)):
        #                 #     print(all_lesson_details_serializer_data[i]['course_lesson_id'])
        #                 #     if all_lesson_details_serializer_data[i]['course_lesson_id'] == int(lesson_id):
        #                 #         print('True')
        #                 #         print('111111111111', type(all_lesson_details_serializer_data[i]))
        #                 #         print('2', type(lesson_details_serializer_data))
        #                 #         all_lesson_details_serializer_data[i] = lesson_details_serializer_data
        #                 #         print(all_lesson_details_serializer_data)
        #                 #     else:
        #                 #         print('False')
        #                 #
        #                 # return JsonResponse({'all_lessons': all_lesson_details_serializer_data})
        #
        #
        #             elif u.last_viewed_lesson_id is not None and u.last_viewed_lesson_duration != time(0, 0, 0):
        #                 # print('------------lesson_id in db and time not zero-------------')
        #                 lesson_id=u.last_viewed_lesson_id
        #                 try:
        #                     data = course_page_lesson_id(user_id, course_id, lesson_id)
        #                     return JsonResponse({'all_lessons': data})
        #                 except:
        #                     return JsonResponse({'status': 'Invalid_user_id_or_course_id_or_lesson_id'})
        #
        #
        #
        #             elif u.last_viewed_lesson_id is not None and u.last_viewed_lesson_duration == time(0, 0, 0):
        #
        #                 # print('------------lesson_id in db and time also zero-------------')
        #
        #                 lesson_id = u.last_viewed_lesson_id
        #
        #                 try:
        #
        #                     data = course_page_lesson_id(user_id, course_id, lesson_id)
        #
        #                     return JsonResponse({'all_lessons': data})
        #
        #                 except:
        #
        #                     return JsonResponse({'status': 'Invalid_user_id_or_course_id_or_lesson_id'})
        #             else:
        #                 # print("no two cases belongs to empty lesson id were satisfied ")
        #                 return JsonResponse({"status": "no_two_cases_belongs_to_empty_lesson_id_were_satisfied"})
        #         else:
        #             return JsonResponse({"status": "Invalid_user_id"})
        #     else:
        #         return JsonResponse({"status": "Invalid_user_id_or_course_id"})
        #
        #     #             current_user_lesson = User_Lessons.objects.get(user_id=user_id, course=course_id,
        #     #                                                            course_lesson_id=lesson_id)
        #     #             print('current_user_lesson', current_user_lesson, current_user_lesson.course_lesson_id.lesson_name,
        #     #                   current_user_lesson.course_lesson_id.lesson_url, current_user_lesson.course_lesson_id.lesson_duration)
        #     #             lesson_details_serializer = User_Lessons_info_serializer(current_user_lesson)
        #     #             lesson_details_serializer_data = lesson_details_serializer.data
        #     #             adding_lesson_data = {'lesson_name': current_user_lesson.course_lesson_id.lesson_name,
        #     #                                   'lesson_url': current_user_lesson.course_lesson_id.lesson_url,
        #     #                                   'lesson_duration': current_user_lesson.course_lesson_id.lesson_duration}  # 'lesson_material':current_user_lesson.course_lesson_id.material_url
        #     #             lesson_details_serializer_data.update(adding_lesson_data)
        #     #             print('lesson_details_serializer.data)))))', lesson_details_serializer.data)
        #     #             print('lesson_details_serializer.data)))))', type(lesson_details_serializer.data))
        #     #
        #     #             current_user_lesson_material = Material.objects.filter(lesson=lesson_id)
        #     #             print('current_user_lesson_material:::', current_user_lesson_material)
        #     #             current_user_lesson_material_serializer = User_Lessons_material_serializer(current_user_lesson_material,
        #     #                                                                                        many=True)
        #     #             current_user_lesson_material_serializer_data = current_user_lesson_material_serializer.data
        #     #             print('current_user_lesson_material_serializer', current_user_lesson_material_serializer_data, '^^^^^^')
        #     #
        #     #             current_user_lesson_clipboard = Clipboard.objects.filter(lesson=lesson_id)
        #     #             print('current_user_lesson_clipboard:::', current_user_lesson_clipboard)
        #     #             current_user_lesson_clipboard_serializer = User_Lessons_clipboard_serializer(current_user_lesson_clipboard,
        #     #                                                                                          many=True)
        #     #             current_user_lesson_clipboard_serializer_data = current_user_lesson_clipboard_serializer.data
        #     #             print('current_user_lesson_clipboard_serializer_data', current_user_lesson_clipboard_serializer_data,
        #     #                   '^^^^^^')
        #     #
        #     #             lesson_material_list = []
        #     #             lesson_clipboard_list = []
        #     #
        #     #             # material data
        #     #             for i in range(0, len(current_user_lesson_material)):
        #     #                 print(len(current_user_lesson_material_serializer_data))
        #     #                 lesson_material_list.append(current_user_lesson_material_serializer_data[i]['material_url'])
        #     #             lesson_details_serializer_data.update({'materials': lesson_material_list})
        #     #
        #     #             # clipboard data
        #     #             for i in range(0, len(current_user_lesson_clipboard)):
        #     #                 lesson_clipboard_list.append(current_user_lesson_clipboard_serializer_data[i]['clipboard_url'])
        #     #             lesson_details_serializer_data.update({'clipboards': lesson_clipboard_list})
        #     #
        #     #             all_lessons_data = []
        #     #             all_lessons_data.append(lesson_details_serializer_data)
        #     #
        #     #             all_lesson_queryset = User_Lessons.objects.filter(user_id=user_id, course=course_id)
        #     #             print('all_lesson_queryset', all_lesson_queryset)
        #     #             print('current_user_lesson_lesson_name', all_lesson_queryset[0].course_lesson_id.lesson_name)
        #     #
        #     #             all_lesson_details_serializer = User_lesson_data_serializer(all_lesson_queryset, many=True)
        #     #             all_lesson_details_serializer_data = all_lesson_details_serializer.data
        #     #             print('all_lesson_details_serializer', all_lesson_details_serializer_data)
        #     #
        #     #             for i in range(0, len(all_lesson_queryset)):
        #     #                 print('current_user_lesson lesson name', all_lesson_queryset[i].course_lesson_id.lesson_name)
        #     #                 # print('current_user_lesson lesson duration', current_user_lesson[i].course_lesson_id.lesson_duration)
        #     #                 # print('current_user_lesson lesson video', current_user_lesson[i].course_lesson_id.lesson_url)
        #     #                 all_lesson_details_serializer_data[i].update({
        #     #                     'lesson_name': all_lesson_queryset[i].course_lesson_id.lesson_name,
        #     #                     'lesson_duration': all_lesson_queryset[i].course_lesson_id.lesson_duration,
        #     #                     # 'lesson_duration': current_user_lesson[i].course_lesson_id.lesson_duration,
        #     #                     # 'lesson_video':current_user_lesson[i].course_lesson_id.lesson_url
        #     #
        #     #                 })
        #     #             print('all_lesson_details_serializer_after_adding_lesson_name', all_lesson_details_serializer_data)
        #     #             for i in range(0, len(all_lesson_details_serializer_data)):
        #     #                 print(all_lesson_details_serializer_data[i]['course_lesson_id'])
        #     #                 if all_lesson_details_serializer_data[i]['course_lesson_id'] == int(lesson_id):
        #     #                     print('True')
        #     #                     print('111111111111', type(all_lesson_details_serializer_data[i]))
        #     #                     print('2', type(lesson_details_serializer_data))
        #     #                     all_lesson_details_serializer_data[i] = lesson_details_serializer_data
        #     #                     print(all_lesson_details_serializer_data)
        #     #                 else:
        #     #                     print('False')
        #     #
        #     #             return JsonResponse({'all_lessons': all_lesson_details_serializer_data})
        #     #     else:
        #     #         print('----------u---------')
        #     #         return JsonResponse({"status": "Invalid_course_id_or_lesson_id"})
        #     #
        #     #
        #     # else:
        #     #     print('-----------lesson_id_query-----------')
        #     #     return JsonResponse({"status":"Invalid_course_id_or_user_id"})

        elif request.method=="GET" and request.query_params.get('lesson_id')!='':
            # print('-------******* lesson id exists in request fetching lesson details---------------')

            # user_id =  2
            user_id = request.user
            course_id = request.query_params.get('course_id')
            lesson_id = request.query_params.get('lesson_id')
            # print(user_id, course_id, lesson_id)
            try:
                # print("in try")
                lesson_status_queryset=User_Lessons.objects.get(user_id=user_id,lesson_id=lesson_id,course_id=course_id)
                # print('lesson_status-----',lesson_status_queryset.lesson_status)
                print('lesson_status-----',lesson_status_queryset.lesson_status)

                if lesson_status_queryset.lesson_status!='locked' and lesson_status_queryset.lesson_status=='unlocked':
                    print('unlocked',lesson_status_queryset.lesson_status)
                    print(lesson_status_queryset.lesson_status == 'locked')
                    data=course_page_lesson_id(user_id,course_id,lesson_id)
                    return JsonResponse({'all_lessons': data})

                elif lesson_status_queryset.lesson_status!='locked' and lesson_status_queryset.lesson_status=='completed':
                    print('completed',lesson_status_queryset.lesson_status)
                    print(lesson_status_queryset.lesson_status == 'locked')
                    data=course_page_lesson_id(user_id,course_id,lesson_id)
                    return JsonResponse({'all_lessons': data})


                elif lesson_status_queryset.lesson_status=='locked' and lesson_status_queryset.lesson_status!='unlocked' and 'completed':
                    print('locked')
                    return JsonResponse({'status': 'please_complete_the_current_lesson_quiz_and_come_back'})
                else:
                    # print('pass')
                    pass
            except:
                return JsonResponse({'status':'Invalid_user_id_or_course_id_or_lesson_id'})
            #
            # # -----current lesson data
            # current_user_lesson = User_Lessons.objects.get(user_id=user_id, course=course_id,
            #                                                course_lesson_id=lesson_id)
            # print('current_user_lesson', current_user_lesson, current_user_lesson.course_lesson_id.lesson_name,
            #       current_user_lesson.course_lesson_id.lesson_url, current_user_lesson.course_lesson_id.lesson_duration)
            # lesson_details_serializer = User_Lessons_info_serializer(current_user_lesson)
            # lesson_details_serializer_data = lesson_details_serializer.data
            # adding_lesson_data = {'lesson_name': current_user_lesson.course_lesson_id.lesson_name,
            #                       'lesson_url': current_user_lesson.course_lesson_id.lesson_url,
            #                       'lesson_duration': current_user_lesson.course_lesson_id.lesson_duration}  # 'lesson_material':current_user_lesson.course_lesson_id.material_url
            # lesson_details_serializer_data.update(adding_lesson_data)
            # print('lesson_details_serializer.data)))))', lesson_details_serializer.data)
            # print('lesson_details_serializer.data)))))', type(lesson_details_serializer.data))
            #
            # current_user_lesson_material = Material.objects.filter(lesson=lesson_id)
            # print('current_user_lesson_material:::', current_user_lesson_material)
            # current_user_lesson_material_serializer = User_Lessons_material_serializer(current_user_lesson_material,
            #                                                                            many=True)
            # current_user_lesson_material_serializer_data = current_user_lesson_material_serializer.data
            # print('current_user_lesson_material_serializer', current_user_lesson_material_serializer_data, '^^^^^^')
            #
            # current_user_lesson_clipboard = Clipboard.objects.filter(lesson=lesson_id)
            # print('current_user_lesson_clipboard:::', current_user_lesson_clipboard)
            # current_user_lesson_clipboard_serializer = User_Lessons_clipboard_serializer(current_user_lesson_clipboard,
            #                                                                              many=True)
            # current_user_lesson_clipboard_serializer_data = current_user_lesson_clipboard_serializer.data
            # print('current_user_lesson_clipboard_serializer_data', current_user_lesson_clipboard_serializer_data, '^^^^^^')
            #
            # lesson_material_list = []
            # lesson_clipboard_list = []
            #
            # # material data
            # for i in range(0, len(current_user_lesson_material)):
            #     print(len(current_user_lesson_material_serializer_data))
            #     lesson_material_list.append(current_user_lesson_material_serializer_data[i]['material_url'])
            # lesson_details_serializer_data.update({'materials': lesson_material_list})
            #
            # # clipboard data
            # for i in range(0, len(current_user_lesson_clipboard)):
            #     lesson_clipboard_list.append(current_user_lesson_clipboard_serializer_data[i]['clipboard_url'])
            # lesson_details_serializer_data.update({'clipboards': lesson_clipboard_list})
            #
            # all_lessons_data = []
            # all_lessons_data.append(lesson_details_serializer_data)
            #
            # all_lesson_queryset = User_Lessons.objects.filter(user_id=user_id, course=course_id)
            # print('all_lesson_queryset', all_lesson_queryset)
            # print('current_user_lesson_lesson_name', all_lesson_queryset[0].course_lesson_id.lesson_name)
            #
            # all_lesson_details_serializer = User_lesson_data_serializer(all_lesson_queryset, many=True)
            # all_lesson_details_serializer_data = all_lesson_details_serializer.data
            # print('all_lesson_details_serializer', all_lesson_details_serializer_data)
            #
            # for i in range(0, len(all_lesson_queryset)):
            #     print('current_user_lesson lesson name', all_lesson_queryset[i].course_lesson_id.lesson_name)
            #     # print('current_user_lesson lesson duration', current_user_lesson[i].course_lesson_id.lesson_duration)
            #     # print('current_user_lesson lesson video', current_user_lesson[i].course_lesson_id.lesson_url)
            #     all_lesson_details_serializer_data[i].update({
            #         'lesson_name': all_lesson_queryset[i].course_lesson_id.lesson_name,
            #         'lesson_duration': all_lesson_queryset[i].course_lesson_id.lesson_duration,
            #         # 'lesson_duration': current_user_lesson[i].course_lesson_id.lesson_duration,
            #         # 'lesson_video':current_user_lesson[i].course_lesson_id.lesson_url
            #
            #     })
            # print('all_lesson_details_serializer_after_adding_lesson_name', all_lesson_details_serializer_data)
            # for i in range(0, len(all_lesson_details_serializer_data)):
            #     print(all_lesson_details_serializer_data[i]['course_lesson_id'])
            #     if all_lesson_details_serializer_data[i]['course_lesson_id'] == int(lesson_id):
            #         print('True')
            #         print('111111111111', type(all_lesson_details_serializer_data[i]))
            #         print('2', type(lesson_details_serializer_data))
            #         all_lesson_details_serializer_data[i] = lesson_details_serializer_data
            #         print(all_lesson_details_serializer_data)
            #     else:
            #         print('False')
            #
            # return JsonResponse({'all_lessons': all_lesson_details_serializer_data})


        else:
            # print("not get or put")
            return JsonResponse({"status": "other_scenario_not_get_or_put"})
    else:
        return JsonResponse({"status":"unauthorized_user"})



@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def learners_count(request):
    if request.user.is_authenticated:
        course_id=request.query_params.get('course_id')

        queryset = usr_course.objects.filter(course_id=course_id)


        if queryset.exists():
            learners=len(queryset)
            # print('learners',type(learners))
            # print('queryset',queryset,len(queryset))
            course_learners_count=Course.objects.filter(course_id=course_id)
            for i in range(len(course_learners_count)):
                course_learners_count[i].views=learners
                course_learners_count[i].save()


            # return JsonResponse({'status':'Invalid course id'})

            return JsonResponse({"Learners":len(queryset)})
        return JsonResponse({"status":"course_id_does_not_exist"})
    else:
        return JsonResponse({'status': "unauthorized_user"})


@api_view(['PUT'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def likes_count(request):
    if request.user.is_authenticated:
        user_id=request.user
        # user_id = 2
        course_id = request.data.get('course_id')

        # course_id =2

        try:
            course_queryset=Course.objects.get(course_id=course_id)

            user_queryset = usr_course.objects.filter(user_id=user_id,course_id=course_id)
        except:
            return JsonResponse({"status": "course_id_does_not_exist"})

        if user_queryset.exists():
            for i in range(0,len(user_queryset)):
                # print(user_queryset[i].like_status)
                status=user_queryset[i].like_status
                if status==False:
                    # print('status',status)
                    user_queryset[i].like_status=True
                    user_queryset[i].save()
                    # print('after like the status is', user_queryset[i].like_status)

                    # print('course_queryset.likes',course_queryset.likes)
                    course_queryset.likes+=1
                    course_queryset.save()
                    # print('after increment of likes count', course_queryset.likes)

                    return JsonResponse({"status":user_queryset[i].like_status,"Likes": course_queryset.likes})


                elif status==True:
                    # print('status', status)
                    user_queryset[i].like_status = False
                    user_queryset[i].save()
                    # print('after like the status is', user_queryset[i].like_status)

                    # print('course_queryset.likes', course_queryset.likes)
                    if course_queryset.likes>0:
                        course_queryset.likes -= 1
                        course_queryset.save()
                        # print('after increment of likes count', course_queryset.likes)
                        return JsonResponse({"status":user_queryset[i].like_status,"Likes":course_queryset.likes})
                    else:
                        pass

        else:
            return JsonResponse({"status":"matching_query_set_does_not_exists"})

    else:
        return JsonResponse({'status':"unauthorized_user"})


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def FAQ_API(request):
    if request.user.is_authenticated:
        course_id=request.query_params.get('course_id')
        faq_queryset = FAQ.objects.filter(course_id=course_id)
        faq_serializer=FAQ_serializer(faq_queryset,many=True)
        faq_serializer_data=faq_serializer.data
        # print('faq_queryset',faq_queryset)
        # print('faq_serializer',faq_serializer)
        # print('faq_serializer_data',faq_serializer_data)
        return JsonResponse({"Course_FAQ": faq_serializer_data})
    else:
        return JsonResponse({"status":"unauthorized_user"})






@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def quiz(request):
    # screens 14,15
    if request.user.is_authenticated:
        # print()
        course_id = request.query_params.get('course_id')  # expects course_id
        lesson_id = request.query_params.get('lesson_id')  # expects lesson_id
        user_id=request.user# e
        # user_id=2# e
        # user_id=request.query_params.get('user_id')
        # print("COURSE_ID", course_id)
        # print("LESSON_ID", lesson_id)
        # print("USER_ID", user_id)

        info = QnA.objects.filter(course_id = course_id, lesson_id = lesson_id)
        # print('info',info)
        sinfo = QnA_serializer2(info, many=True)
        # print('sinfo_data',sinfo.data)

        # info2 = User_answers.objects.filter(user_id = user_id, Course_id = course_id, lesson_id = lesson_id)
        # print('info2',info2)
        # sinfo2 = User_answers_serializer2(info2, many=True)
        # print("sinfo2.data --------------------------------",sinfo2.data)
        # print(info2[0].answer,info2[0].status)


        for i in range(0,len(sinfo.data)):

            # sinfo.data[i].update({'user_entered_answer':info2[i].answer,'answer_status':info2[i].status})
            sinfo.data[i].pop("correct_answer")
            sinfo.data[i].pop("lesson_id")
            sinfo.data[i].pop("course_id")
            qsn_optn=sinfo.data[i].pop('question_options')
            sinfo.data[i].update({'question':qsn_optn['qsn'],'options':qsn_optn['options']})
            # print('///////////////////////////////',qsn_optn)

        # print(sinfo.data)

        return JsonResponse({'quiz': sinfo.data})#'course_id': course_id, 'lesson_id': lesson_id
    else:
        return JsonResponse({'status':'unauthorized_user'})



@api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def quiz_attempt(request):
    if request.user.is_authenticated:
        attempt_info=request.data
        # print('attemp_info',attempt_info)
        # print(lesson_id)
        final_response = []
        # lesson_id = attempt_info[0]['lesson_id']
        lesson_id = request.data['lesson_id']
        max_lesson_id = User_Lessons.objects.filter(course_id=request.data.get('course_id')).aggregate(Max('lesson_id'))['lesson_id__max']
        # print('max_lesson_id',max_lesson_id,type(max_lesson_id))
        # for i in range(1,len(attempt_info)):
        for i in range(0,len(request.data['questions'])):
            # print('*****request.dataquestions',request.data['questions'])

            # print('lllllllll',len(attempt_info))
            # lesson_id = attempt_info[i]['lesson_id']
            question_id=int(request.data['questions'][i]['question_id'])

            u_correct_answer=request.data['questions'][i]['option']
            # print('question_id', question_id,lesson_id,u_correct_answer)
            # print(type(u_correct_answer))
            a = QnA.objects.filter( question_id=question_id)  # ,correct_answer=u_correct_answer
            quiz_serializer=QnA_serializer(a,many=True)
            quiz_serializer_data=quiz_serializer.data
            # print('.........',a)
            # print('--------',quiz_serializer_data)
            for i in range(0,len(quiz_serializer_data)):

                # print('a',a[i].correct_answer)
                # print('ahhhhh',len(quiz_serializer_data))
                # print('answer in db',a[i].correct_answer)
                # print('user answer',u_correct_answer)
                if len(a[i].correct_answer)==1:#scq
                    # print(type(a[i].correct_answer))

                    if len(a[i].correct_answer) == len(u_correct_answer):
                        if a[i].correct_answer == u_correct_answer:

                            # print('True')
                            final_response.append({"question_id": question_id,"user_answer":u_correct_answer ,"status": "True"})
                            # break
                        else:

                            # print('false')
                            final_response.append({"question_id": question_id, "user_answer":u_correct_answer ,"status": "False"})
                    # else:
                    #     final_response.append(f'please select {len(a[i].correct_answer)} option')

                elif len(a[i].correct_answer)==2:
                    # res = []
                    # if len(a[i].correct_answer) == len(u_correct_answer):

                    # print('mcq',a[i].correct_answer,u_correct_answer)
                    if a[i].correct_answer==u_correct_answer :
                        final_response.append({"question_id":question_id,"user_answer":u_correct_answer ,"status":"True"})
                        # print("appended true for mcq")
                    else:
                        final_response.append({"question_id":question_id,"user_answer":u_correct_answer ,"status":"False"})
                        # print("appended False for mcq")
                    # for x,y in list(zip(a[i].correct_answer,u_correct_answer)):
                    #     print(list(zip(a[i].correct_answer,u_correct_answer)))
                    #     print('xy',x,y)
                    #     if x == y:
                    #         res.append('True')
                    #     else:
                    #         res.append('False')
                    # print('res',res)
                    # final_response.append(res)
                    # else:
                    #     res.append(f'please select {len(a[i].correct_answer)} options')
                    #     final_response.append(res)

                        # return JsonResponse()
                # elif len(u_correct_answer)==0:
                #     print('---------------------------------i am else')
                #     for j in range(len(request.data['questions'])):
                #         print(len(request.data['questions']))
                #         final_response.append({"question_id":request.data['questions'][j]['question_id'], "user_answer": u_correct_answer, "status": "False"})
                else:
                    return JsonResponse({"status":"unexpected_response_from_user"})
            # print(final_response,type(final_response))
        response = {"answer_status":final_response}


        total_questions = len(response["answer_status"])
        total_correct = 0

        for answer_status in response["answer_status"]:
            # print('00000000000000', answer_status)
            for k, v in answer_status.items():
                # print(k, v)
            # print(answer_status)
                if isinstance(v, str):  # Single choice question/blank(single word(single blank _ ),sentence)/question answer in text box
                    # print('answer_status',answer_status,type(answer_status))
                    # print('****', isinstance(v, str))
                    if v == "True":
                        total_correct += 1
            # elif isinstance(answer_status, list):#mcq/blank(multiple blanks _ , _ , _)
            #     print('&&&&&&', isinstance(answer_status, list))
            #     correct_choices = answer_status.count("True")
            #     if correct_choices == len(answer_status):
            #         print('answer_status list',answer_status,type(answer_status))
            #         total_correct += 1
            #     elif correct_choices > 0 and correct_choices < len(answer_status):
            #         print(len(answer_status))
            #         partial_credit = correct_choices / len(answer_status)  # Calculate dynamic partial credit
            #         total_correct += partial_credit
        # print('total_correct',total_correct,total_questions)
        quiz_percentage = int((total_correct / total_questions * 100))
        # print(quiz_percentage)
        quiz_status="Fail"
        if quiz_percentage>70:
            quiz_status="Pass"




        # print(f"Total Correct: {total_correct}")
        # print(f"Total Questions: {total_questions}")
        # print(f"Quiz Percentage: {quiz_percentage}%")
        # print('final_response',final_response)

        user_id=request.user
        # user_id=2
        # print('user_id',user_id)
        # course_id=attempt_info[0]['course_id']
        # print('course_id',course_id)
        lesson_id = request.data['lesson_id']
        # print('lesson_id',lesson_id)
        queryset=User_Lessons.objects.get(user_id=user_id,lesson_id=lesson_id)#,course=course_id
        # print(queryset)
        serializer=User_Lessons_quiz_score_serializer(queryset,data={"quiz_score":quiz_percentage})
        if serializer.is_valid():
            # print('serializer',serializer,serializer.data,serializer.validated_data['quiz_score'])
            queryset.quiz_attempt_status=True
            queryset.save()
            serializer.save()
            lesson_scores=[]

            course_status_queryset=User_Lessons.objects.filter(user_id=user_id,course_id=request.data.get('course_id'))

            course_status_update=usr_course.objects.get(user_id=user_id, course_id=request.data.get('course_id'))
            # print('course_status_update',course_status_update)

            for i in range(len(course_status_queryset)):

                # print('course_status_queryset',course_status_queryset[i].quiz_score)
                lesson_scores.append(course_status_queryset[i].quiz_score)
            print('lesson_scores',lesson_scores)

            # for score in lesson_scores:
            #     # print(i)
            #     if score<70:
            #
            #         # print('inprogress')
            #         # pass
            #         course_status_update.course_status = 'Inprogress'
            #         course_status_update.save()
            #         print('course_status_update',course_status_update.course_status)
            #     else:
            #         course_status_update.course_status='Completed'
            #         course_status_update.save()
            #         print('course_status_update',course_status_update.course_status)

            if all(score > 70 for score in lesson_scores):
                course_status_update.course_status = 'Completed'
                course_status_update.save()
                print('course_status_update', course_status_update.course_status)
            else:
                course_status_update.course_status = 'Inprogress'
                course_status_update.save()
                print('course_status_update', course_status_update.course_status)

            # user
            # course
            if queryset.quiz_attempt_status==True and queryset.quiz_score>70 and int(lesson_id)!=max_lesson_id:
                # below lessons variable represents querying the next most greater lesson id based on request came on lesson id from frontend ,to update next lesson staus
                lessons=User_Lessons.objects.filter(course_id=request.data.get('course_id'), lesson_id__gt=lesson_id).order_by('lesson_id').first()

                # print(lessons,len(lessons))
                # print('next lesson id from multiple lessons of course',lessons.lesson_id.lesson_id,lessons)
                next_lesson=User_Lessons.objects.get(lesson_id=lessons.lesson_id.lesson_id)
                # print('next_lesson single object',next_lesson.lesson_id.lesson_id,next_lesson)
                # user_lesson_queryset=Lessons.objects.filter(course_in_lessons=course_id,lesson_id__gt=lesson_id).order_by('lesson_id').first()
                if next_lesson.lesson_status=='locked':
                    next_lesson.lesson_status='unlocked'
                    next_lesson.save()

                    current_lesson=User_Lessons.objects.get(lesson_id=lesson_id)
                    # print('current lesson id',current_lesson.lesson_id.lesson_id,current_lesson)
                    current_lesson.lesson_status='completed'
                    current_lesson.save()
                elif  next_lesson.lesson_status=='unlocked' or 'completed':
                    pass
                else:
                    return JsonResponse({"status":"not_locked_not_unlocked_not_completed_got_diffrent_lesson_status_in_db"})
                    # print('not locked not unlocked not completed got diffrent lesson status in db')

            # current_lesson = User_Lessons.objects.get(course_lesson_id=lesson_id)
            # current_lesson_id=current_lesson.course_lesson_id.lesson_id
            # print('current lesson id', current_lesson.course_lesson_id.lesson_id, current_lesson)
            # max_lesson_id = User_Lessons.objects.filter(course=request.data.get('course_id')).aggregate(Max('course_lesson_id'))['course_lesson_id__max']
            elif int(lesson_id)==max_lesson_id and queryset.quiz_attempt_status==True and queryset.quiz_score>70:
                #no next lesson is present and user is in last lesson scenario
                # print('--------------updating max lesson data-----------------------------------------------------------------------------')
                current_lesson = User_Lessons.objects.get(user_id=user_id,lesson_id=lesson_id)
                # print('current lesson id', current_lesson.lesson_id.lesson_id, current_lesson)
                current_lesson.lesson_status = 'completed'
                current_lesson.save()




            else:
                # return JsonResponse({"status":"no_lesson_status_updated"})
                # print("no lesson status updated")
                pass

            # print('sk')


        # print(serializer.errors)


        # if len(a[i].correct_answer) == len(u_correct_answer):
        #     print(len(a[i].correct_answer),len(u_correct_answer),a[i].correct_answer,u_correct_answer)
        return JsonResponse({'answer_status':final_response,'quiz_score':quiz_percentage,'quiz_status':quiz_status})
        # return JsonResponse({'answer_status':final_response})
    else:
        return  JsonResponse({'status':'unauthorized_user'})



@api_view(['GET','PUT'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def user_details(request):
    """assuming that post will always come after get. So that there is no need to ask for user-id again in
    the elif statement in order to compare the existing record and the changed data of that record(that comes
    from the post request)"""
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_id = request.user
            # user_id = 2
            d = User_details.objects.filter(user_id = user_id)
            # print("read the record")
            d_s = user_details_serializer(d, many=True)
            ds_data=d_s.data
            # print(ds_data)
            # ds_data[0].update({"name":"neeraj"})
            # d_s.data[0].pop("password")
            return JsonResponse({"user_details": ds_data[0]})
        elif request.method == 'PUT':

            ds = request.data  # expects a dictionary with user details as per the user_details model
            user_id = request.user
            # user_id = 2
            try:
                rec = User_details.objects.get(user_id = user_id)#ds["user_id"]

                rec_list = json.loads(serializers.serialize('json', [rec, ]))

                for item in ds and rec_list[0]["fields"]:
                    # print('(((((((((((', ds[item], rec_list[0]["fields"][item])
                    # if ds[item] == rec_list[0]["fields"][item]:
                    #
                    #     print("no change in value")
                    #     continue
                    # else:
                    if item == "name" and ds[item]!="":

                        rec.name = ds[item]
                    else:
                        rec.name =  rec.name
                    if item == "contact_no" and ds[item]!="":
                        rec.contact_no = ds[item]
                    else:
                        rec.contact_no=rec.contact_no
                    if item == "company" and ds[item]!="":
                        rec.company = ds[item]
                    else:
                        rec.company = rec.company
                    if item == "business_email" and ds[item]!="":
                        rec.business_email = ds[item]
                    else:
                        rec.business_email = rec.business_email
                    if item == "years_of_experience" and ds[item]!="":
                        rec.years_of_experience = ds[item]
                    else:
                        rec.years_of_experience=rec.years_of_experience

                    if item == "job_position" and ds[item]!="":
                        rec.job_position = ds[item]
                    else:
                        rec.job_position=rec.job_position

                    if item == "location" and ds[item]!="":
                        rec.location = ds[item]
                    else:
                        rec.location=rec.location


                    # else:
                    #     continue
                    rec.save()
                    # print("item found -->", item)
                de = User_details.objects.filter(user_id=user_id)#ds["user_id"]
                de_s = user_details_serializer(de, many=True)
                # print("d_s", de_s.data)
                return Response({"user_details":de_s.data})
            except User_details.DoesNotExist:
                return JsonResponse({"status":"user_does_not_exist"})
        else:
            pass
    else:
        return JsonResponse({"status":"unauthorized_user"})




@api_view(['PUT'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def change_password(request):
# ChangePasswordSerializer
    if request.user.is_authenticated:
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password=serializer.validated_data['current_password']
            new_password=serializer.validated_data['new_password']
            confirm_new_password=serializer.validated_data['confirm_new_password']
            userr = request.user
            # userr="neerajpynam3@gmail.com"
            user = User.objects.get(username=userr)
            # print(user)
            if new_password!=confirm_new_password and not check_password(current_password,user.password):
                return JsonResponse({"status": ["you_have_entered_wrong_password","password_do_not_match"]})
            if not check_password(current_password,user.password):
                return JsonResponse({"status":"you_have_entered_wrong_password"})
            if new_password!=confirm_new_password:
                return JsonResponse({"status":"password_do_not_match"})
            # if new_password == current_password:
            #     return JsonResponse({"status": "New_password_cannot_be_the_same_as_the_old_password"})

            user.set_password(new_password)
            user.save()

            return JsonResponse({"status":"successfull"})
    else:
        return JsonResponse({"status":"unauthorized_user"})




@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def training_subscription(request):
    # this api sends subscription data of the courses user 1 has enrolled for
    if request.user.is_authenticated:
        user_id= request.user
        # user_id= 2
        info1 = usr_course.objects.filter(user_id = user_id)
        serializer1 = usr_course_serializer(info1, many = True)
        # print('serializer1------------',serializer1)
        # print('serializer1.data-----whole',serializer1.data)

        for i in range(0, len(serializer1.data)):
            for k in list(serializer1.data[i].keys()):
                if k in ['course_id',"order_id","subscription_datetime","amount"]:
                    continue
                else:
                    serializer1.data[i].pop(k)
        # print('serializer1.data after pop keys-----------',serializer1.data)
        for i in range(0, len(serializer1.data)):
            # print('/////////',serializer1.data)
            info2 = Course.objects.filter(course_id = serializer1.data[i]["course_id"])
            # print('info2----',info2)
            serializer2 = Course_serializerr(info2, many=True)
            # print('serializer2****',serializer2.data)
            serializer1.data[i].pop('course_id')
            subscription_datetime = serializer1.data[i].pop("subscription_datetime")
            # Extract date and time components separately
            serializer1.data[i]["subscription_date"] = datetime.datetime.strptime(subscription_datetime,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            serializer1.data[i]["subscription_time"] = datetime.datetime.strptime(subscription_datetime,"%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S")
            serializer1.data[i].update(Course_name = serializer2.data[0]["course_name"])
            serializer1.data[i].update({'amount':serializer2.data[0]["amount"]})


            # serializer1.data[i].update()
        # print('serializer1.data after updating keys',serializer1.data)

        return JsonResponse({"Training_Subscription" : serializer1.data})
    else:
        return JsonResponse({"status":"unauthorized_user"})




