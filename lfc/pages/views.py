from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .forms import LoginForm, Registrationform
from django.contrib.auth import authenticate, login
import os, io
from PIL import Image
import numpy as np
from django.urls import path, include
import base64

import face_recognition
import cv2

from .models import UserProfile, Messages
from .serializers import MessageSerializer


def facedect(loc, imgstr):
    imgstr = Image.open(io.BytesIO(base64.b64decode(imgstr)))
    imgstr = cv2.cvtColor(np.array(imgstr), cv2.COLOR_BGR2RGB)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'pages')

    format, loc = loc.split(';base64,')
    loc = Image.open(io.BytesIO(base64.b64decode(loc)))
    loc = cv2.cvtColor(np.array(loc), cv2.COLOR_BGR2RGB)

    face_1_face_encoding = face_recognition.face_encodings(loc)[0]

    small_frame = cv2.resize(imgstr, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    check = face_recognition.compare_faces(face_1_face_encoding, face_encodings)

    print(check)
    if check[0]:
        return True

    else:
        return False


def about(request):
    return render(request, "about.html", {})


def loginform(request):
    if request.method == "POST":
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            hiddenimage = request.POST['hiddenimage']

            from django.core.files.base import ContentFile
            format, imgstr = hiddenimage.split(';base64,')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if facedect(user.userprofile.head_shott, imgstr):
                    login(request, user)
                return redirect('/')
            else:
                return redirect('/')
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def home(request):
    return render(request, 'home.html', {})


def register(request):
    if request.method == "POST":
        form = Registrationform(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

    form = Registrationform()

    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    return render(request, 'profile.html', {})


def contacts(request):
    return render(request, 'contacts.html', {})


def faq(request):
    return render(request, 'faq.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def getFriendsList(id):
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    use = UserProfile.objects.get(username=username)
    id = use.user.id
    return id


def addFriend(request):
    # позже заменить
    friendname = 'admin'
    username = request.user
    id = getUserId(username)
    friend = UserProfile.objects.get(username=friendname)
    curr_user = UserProfile.objects.get(user_id=id)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.user_id:
            flag = 1
            break
    if flag == 0:
        curr_user.friends_set.create(friend=friend.user_id)
        friend.friends_set.create(friend=id)
    return redirect("/search")


def chat(request, username):
    addFriend(request)
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(user_id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.user_id) | Messages.objects.filter(
        sender_name=friend.user_id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
