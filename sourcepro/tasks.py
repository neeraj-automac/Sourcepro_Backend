import datetime

from django.db.models import F, Case, When

from .models import *

from celery import shared_task

from .serializers import usr_course_serializer

print('^^^^ in task ^^^^^^^')



@shared_task(bind=True)
def tes_fun(self):
    print('inside function executing in tasks.py')
    # usr_course.objects.update(deactivation_days_left=F('deactivation_days_left') - 1)
    # usr_course.objects.update(
    #     deactivation_days_left=Case(
    #         When(deactivation_days_left__gt=0, then=F('deactivation_days_left') - 1))
    # )

    # usr_course.objects.update(
    #     deactivation_days_left=Case(
    #         When(deactivation_days_left__exact=0, then=F('deactivation_days_left')),
    #         default=F('deactivation_days_left'),  # Leave it unchanged if it's not exactly 0
    #     )
    # )

    # usr_course.objects.update(
    #     deactivation_days_left=Case(
    #         When(deactivation_days_left__isnull=True, then=F('deactivation_days_left')),
    #         default=F('deactivation_days_left'),  # Leave it unchanged if it's not exactly 0
    #     )
    # )



    # usr_course_queryset=usr_course.objects.all()
    # a = usr_course_serializer(usr_course_queryset, many=True)
    # for i in range(len(a.data)):
    #     # print('before'+str(a.data[i]['deactivation_days_left']))
    #     # a.data[i]['deactivation_days_left']=a.data[i]['deactivation_days_left']-1
    #     print('after'+str(a.data[i]['deactivation_days_left']))

    # print('request',request.user)
    # print(datetime.datetime.now())
    # usr_course_queryset=usr_course.objects.all()
    #
    # print('--------------------usr_course_queryset------------------')
    # a=usr_course_serializer(usr_course_queryset,many=True)
    # for i in range(len(a.data)):
    #     print('before'+str(a.data[i]['deactivation_days_left']))
    #     a.data[i]['deactivation_days_left']=a.data[i]['deactivation_days_left']-1
    #     print('after'+str(a.data[i]['deactivation_days_left']))
    # for i in range(len(usr_course_queryset)):
    #     b=usr_course_queryset[i]
    #     if b.deactivation_days_left>0:
    #         b.deactivation_days_left=b.deactivation_days_left-1
    #         b.save()
    #
    #     else:
    #         print('days left is zero or less than zero')
    #         pass

    return 'Done'