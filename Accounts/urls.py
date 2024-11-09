
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login_user/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('send_mail/', send_mail_req, name='send_mail'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('forget_password/', forget_pass, name='forget_pass'),
    path('verify_user/', verify_user, name='verify_user'),

]