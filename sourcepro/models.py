from datetime import timedelta
from datetime import time
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.fields import EmailField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Min, Max
from django.core.mail import send_mail
from django.conf import settings

class User_details(models.Model):
    objects = models.Manager()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE )
    name=models.CharField(max_length = 50,blank=False)
    contact_no = models.BigIntegerField()
    user_status=models.CharField(max_length = 50,blank=True)
    company = models.CharField(max_length = 30,blank=True)#remove?
    business_email = models.EmailField(max_length = 254,blank=False)
    years_of_experience = models.PositiveSmallIntegerField(null=True, blank=True)#remove?
    job_position = models.CharField(max_length = 30,blank=True)#remove?
    location = models.CharField(max_length = 30,blank=False)
    otp = models.CharField(max_length=255, unique=True, blank=True, null=True)
    course_id=models.IntegerField(null=True, blank=True)




    def __str__(self):
        return self.user_id.username








class Course(models.Model):
    objects = models.Manager()

    course_id = models.AutoField(primary_key = True)
    course_name = models.CharField(max_length = 100,blank=False)
    thumbnail = models.URLField()
    author = models.CharField(max_length = 20, blank=False)
    created_date = models.DateField()  #date of release
    total_duration = models.TimeField()# update the value of total duration based on no of total lessons duration sum
    course_description = models.TextField()
    COURSE_STATUS_CHOICES = (('active', 'Active'), ('inactive', 'Inactive'))
    course_status = models.CharField(max_length=15, choices=COURSE_STATUS_CHOICES)
    amount = models.PositiveSmallIntegerField()
    views = models.PositiveSmallIntegerField(default = 0)
    likes = models.PositiveSmallIntegerField(default=0)
    activation_duration = models.IntegerField(default=48) #no of days course active
    COURSE_TYPE_CHOICEs = (('new', 'new'), ('old', 'old'))
    type = models.CharField(default='new',max_length=25,choices=COURSE_TYPE_CHOICEs)



    def __str__(self):  # to display  in admin page
        return (self.course_name)

class usr_course(models.Model):
    objects = models.Manager()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)# -Course_id
    COURSE_STATUS_CHOICES = (('Inprogress', 'Inprogress'), ('Completed', 'Completed'))
    course_status = models.CharField(max_length=15,choices=COURSE_STATUS_CHOICES,default='Inprogress' )
    order_id = models.CharField(max_length=50,blank=False)
    subscription_datetime = models.DateTimeField(null=True, blank=True)
    deactivation_datetime = models.DateTimeField(null=True, blank=True)
    percentage_completed = models.DecimalField(default=00.00,max_digits=5, decimal_places=2)# ajax #update based on fromula
    completed_default = time(0, 0, 0)
    minutes_Completed = models.TimeField(default=completed_default)#  ajax # update after taking value from frontend note update with greatest watch time day to day
    minutes_left = models.TimeField(default=completed_default)# dynamic Ajax
    certificate_url = models.URLField(null=True)
    deactivation_days_left = models.PositiveSmallIntegerField(null=True, blank=True)#----------celery--------------/ajax
    like_status=models.BooleanField(default=False)
    last_viewed_lesson_id = models.IntegerField(null=True, blank=True)
    completed_default = time(0, 0, 0)
    last_viewed_lesson_duration = models.TimeField(default=completed_default)

    class Meta:
        unique_together = ('user_id', 'course_id')

    def __str__(self):
        return f'{self.user_id} - {self.course_id}'


@receiver(post_save, sender=usr_course)
def set_deactivation_datetime(sender, instance, created, **kwargs):
    if created:
        # print("created")
        COURSE = instance.course_id# Access the related course object  # -Course_id
        # print(COURSE,"COURSE")
        activation_duration = COURSE.activation_duration  # Get the activation duration from the course
        # print("activation_duration",activation_duration)
        subscription_datetime = instance.subscription_datetime  # Get the subscription datetime
        # print('subscription_datetime',subscription_datetime)

        # Calculate the deactivation datetime by adding the activation duration to the subscription datetime
        deactivation_datetime = subscription_datetime + timedelta(days=activation_duration)
        # print('deactivation_datetime',deactivation_datetime)

        # Set the calculated deactivation datetime and save the instance
        instance.deactivation_datetime = deactivation_datetime
        # print("assigning deactivation_datetime")
        instance.deactivation_days_left = activation_duration
        # print('instance.deactivation_days_left',instance.deactivation_days_left)
        # print("assigning deactivation_days_left")
        #------------------storing minimum lesson id of a course--------------------
        get_course=Lessons.objects.filter(course_id=COURSE)
        print('get_course',get_course)
        min_lesson_id=get_course.aggregate(Min('lesson_id'))
        print('min_lesson_id',min_lesson_id)
        instance.last_viewed_lesson_id=min_lesson_id['lesson_id__min']
        print('instance.last_viewed_lesson_id',instance.last_viewed_lesson_id)


        instance.save()
        # print('saved deactivation_datetime as:',deactivation_datetime)
        # print('saved instance.deactivation_days_left',instance.deactivation_days_left)
    # print("--------------------------------------")
    # print("assigning deactivation_datetime")
    # print('instance.deactivation_days_left', instance.deactivation_days_left)
    # print("assigning deactivation_days_left")
    # print('saved deactivation_datetime as:', instance.deactivation_datetime)
    # print('saved instance.deactivation_days_left', instance.deactivation_days_left)
    else:
        # print('----------------------------EDITED----------------------------')
        pass

class Lessons(models.Model):
    objects = models.Manager()

    lesson_id = models.AutoField(primary_key = True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE) # -Course_id
    lesson_name = models.CharField(max_length= 200)
    lesson_duration = models.TimeField()
    lesson_url = models.URLField()
    pass_percentage = models.DecimalField(default=80.00,max_digits=4,decimal_places=2)#?--------
    lesson_status = models.CharField(max_length=15, default='Locked')
    subtitle_file_link = models.URLField(default = None)
    class Meta:
        unique_together = ('course_id', 'lesson_name')

    def __str__(self):  # to display  in admin page
        return f'{self.lesson_name} - {self.course_id.course_name}'



class QnA(models.Model):
    objects = models.Manager()
    question_id = models.AutoField(primary_key = True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)# courses as foreign key
    lesson_id = models.ForeignKey(Lessons , on_delete=models.CASCADE)# lesson as foreign key
    question_options = models.JSONField()
    correct_answer = ArrayField(models.TextField(), default=list)
    question_type = models.CharField(max_length= 50, default = "SCQ")

    def __str__(self):
        return " %s %s %s" %(self.course_id.course_name,self.lesson_id.lesson_name ,self.question_options)


class FAQ(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faqs')# -Course_id
    question = models.TextField()
    answer = models.TextField()
    # def __str__(self):  # to display  in admin page
    #     return (self.course_id)



class User_Lessons(models.Model):
    objects = models.Manager()

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_lesson_id = models.AutoField(primary_key = True)
    lesson_id = models.ForeignKey(Lessons,on_delete=models.CASCADE)#lesson present in a course # -lesson_id
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_default= time(0, 0, 0)
    minutes_completed = models.TimeField(default=completed_default)
    minutes_left = models.TimeField(default=completed_default)
    LESSON_STATUS_CHOICES = (('locked', 'locked'),('unlocked', 'unlocked'),('completed','completed'))
    lesson_status = models.CharField(max_length=15, choices=LESSON_STATUS_CHOICES, default='Locked')
    quiz_score = models.DecimalField(default=00.00,max_digits=5,decimal_places=2)
    quiz_attempt_status=models.BooleanField(default=False)


    class Meta:
        # Add the unique_together constraint to prevent duplicates
        unique_together = (('user_id', 'course_id', 'lesson_id'),)

    def __str__(self):  # to display  in admin page
        return self.lesson_id.lesson_name


class Material(models.Model):
    lesson_id = models.ForeignKey(Lessons, on_delete=models.CASCADE)#,related_name='materials' # -lesson_id
    material_url = models.URLField()
    def __str__(self):  # to display  in admin page
        return (self.lesson_id.lesson_name)

class Clipboard(models.Model):
    lesson_id = models.ForeignKey(Lessons, on_delete=models.CASCADE)# -lesson_id
    clipboard_url = models.TextField()



#-----------------------hct models-----------------------

class Template(models.Model):

    template_name = models.CharField(max_length=50, blank=False)
    template_heading= models.CharField(max_length=100, blank=False)
    template_body=models.TextField()

    def __str__(self):
        return self.template_name






# class UserTemplateManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user_detail__user_status='active')


class Broadcast(models.Model):
    # user_detail = models.ForeignKey(User_details, on_delete=models.CASCADE)
    # user_template= models.ForeignKey(Template, on_delete=models.CASCADE)
    template=models.ForeignKey(Template, on_delete=models.CASCADE)
    users=models.ManyToManyField(User_details)
    frequency=models.CharField(max_length=150)
    follow_up=models.CharField(max_length=50,blank=False)
    time=models.TimeField(null=True, blank=True)
    sent_status=models.BooleanField(default=False)




    # objects = UserTemplateManager()
    #
    # def save(self, *args, **kwargs):
    #
    #     # if self.user_detail.user_status != 'active':
    #     #     raise ValidationError('User must be active to be included in UserTemplate.')
    #     # super().save(*args, **kwargs)
    #     if self.user_detail.user_status != 'active':
    #         logger.warning(f'Attempted to save UserTemplate for inactive user: {self.user_detail.user_id.username}')
    #         return  # Skip saving the instance
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.follow_up


@receiver(post_save, sender=Broadcast)
def send_broadcast(sender, instance, created, **kwargs):
    if created:
        print("created")


    else:
        print("edited in models.py")
        if instance.sent_status==True:


            print("broadcast_usersssss", instance.users.all())
            email_addresses = list(instance.users.values_list('business_email', flat=True))
            print("User email addresses:", email_addresses, type(email_addresses))
            contact_numbers = list(instance.users.values_list('contact_no', flat=True))
            print("User contact_numbers:", contact_numbers, type(contact_numbers))
            print(instance.template.template_name)
            print(instance.template.template_heading)
            print(instance.template.template_body)
            # email_body = f'''<p>instance.template.template_heading</p>'''
            if instance.frequency == "once" and instance.follow_up == "mail":
                print("sending once via mail")
                send_mail(instance.template.template_heading, '', from_email=settings.EMAIL_HOST_USER,
                          recipient_list=email_addresses, html_message=instance.template.template_body)
                print("sended")

            elif instance.frequency == "periodically" and instance.follow_up == "mail":
                print("sending periodically via mail by calling celery")


            elif instance.frequency == "once" and instance.follow_up == "whatsapp":
                print("sending once via  whastapp")
            elif instance.frequency == "periodic" and instance.follow_up == "whatsapp":
                print("sending periodically via  whatsapp ")

            elif instance.frequency == "once" and instance.follow_up == "both":
                print("sending once via both by calling send mail and whastapp")
            elif instance.frequency == "periodic" and instance.follow_up == "both":
                print("sending periodically via both by calling celery and writting send mail")


            else:
                print("not once not periodic ")

        else:
            print("executing -sent status is False")
    # else:
    #     print("not created not updated")




