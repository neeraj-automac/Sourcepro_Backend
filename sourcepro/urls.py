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
    path('add_delete_users/',views.add_delete_users),
    path('update_user_status/',views.update_user_status),
    path('pagination/',views.pagination),
    path('edit_user_details_hct/',views.edit_user_details_hct),
    path('broadcast/', views.broadcast, name='broadcast'),
    path('hct_active_users_dd/', views.hct_active_users, name='hct_active_users'),
    path('create_template/', views.create_template, name='create_template'),
    path('update_template/', views.update_template, name='update_template'),
    path('delete_template/', views.delete_template, name='delete_template'),
    path('template_pagination/',views.Templates_pagination,name='Templates_pagination'),
    path('create_broadcast/', views.create_broadcast, name='create_broadcast'),
    path('update_broadcast/', views.update_broadcast, name='update_broadcast'),
    path('delete_broadcast/', views.delete_broadcast, name='delete_broadcast'),
    path('hct_template_dd/', views.hct_template_dd, name='hct_template_dd'),
    path('broadcast_pagination/',views.Broadcast_pagination,name='Broadcast_pagination'),

    # path('training_subscription/', views.training_subscription),
    # path('update_user_course/', views.update_user_course),
    # path('in_course/<str:pk>/', views.in_course),#unused
    # path('in_course/<str:pk>/quiz/', views.quiz),
    # path('FAQs/<str:pk>/', views.get_faq),
    # path('in_course/<str:pk>/quiz/<lesson_name>',views.quiz),
    # path('in_course/<str:pk>/quiz/<lesson_name>/',views.quiz),
    # path('quiz/result/', views.quiz_results)
]