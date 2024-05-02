from django.urls import path
from . import views
from .views import*


urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('otp/',views.set_new_password_send_otp),
    path('set_password/',views.set_new_password),
    path('home/',views.home),
    path('mycourses/', views.mycourses),
    path('usr_course_page/',views.usr_course_page),
    path('usr_course_page_lesson/',views.usr_course_page_lesson),
    path('faq/',views.FAQ_API),
    path('learners_count/',views.learners_count),
    path('likes_count/',views.likes_count),
    path('quiz/', views.quiz),
    # path('course_page/',views.course_page),
    # path('quiz_result/',views.quiz_result),
    path('quiz_attempt/',views.quiz_attempt),
    path('user_details/', views.user_details),
    # path('lesson_details/',views.lesson_details),
    path('change_password/', views.change_password),
    path('training_subscription/',views.training_subscription),
    path('next_lesson/',views.Next_lesson),
    path('download_certificate/',views.download_certificate),
    path('all_users_status/',views.all_users_status),

    # path('training_subscription/', views.training_subscription),
    # path('update_user_course/', views.update_user_course),
    # path('in_course/<str:pk>/', views.in_course),#unused
    # path('in_course/<str:pk>/quiz/', views.quiz),
    # path('FAQs/<str:pk>/', views.get_faq),
    # path('in_course/<str:pk>/quiz/<lesson_name>',views.quiz),
    # path('in_course/<str:pk>/quiz/<lesson_name>/',views.quiz),
    # path('quiz/result/', views.quiz_results)
]