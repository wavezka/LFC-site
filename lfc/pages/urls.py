from django.urls import path
from . import views
urlpatterns = [

    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.loginform,name='login'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('contacts/',views.contacts,name='contacts'),
    path('faq/',views.faq,name='faq'),
    path('blog/',views.blog,name='blog'),
    path("account/addfriend/<str:name>", views.addFriend, name="addFriend"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]



