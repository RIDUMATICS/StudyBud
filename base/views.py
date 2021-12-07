from django.http.response import Http404
from django.shortcuts import redirect, render
from .models import Room
from .forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def home(request):
    q = request.GET.get('q')
    if q:
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(
            description__icontains=q) | Q(name__icontains=q))
    else:
        rooms = Room.objects.all()
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count})


def room(request, id):
    room = Room.objects.get(id=id)
    return render(request, 'base/room.html', {'room': room})


@login_required(login_url='/auth/login')
def createRoom(request):
    context = {}
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()
        context['form'] = form

    return render(request, 'base/room_form.html', context)


@login_required(login_url='/auth/login')
def updateRoom(request, id):
    context = {}

    try:
        room = Room.objects.get(id=int(id))
        form = RoomForm(instance=room)
        context['form'] = form

        if request.method == 'POST':
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('home')

        return render(request, 'base/room_form.html', context)
    except Room.DoesNotExist:
        raise Http404("Invalid Room ID")


@login_required(login_url='/auth/login')
def deleteRoom(request, id):
    context = {}
    try:
        room = Room.objects.get(id=int(id))
        context['room'] = room
        if request.method == 'POST':
            room.delete()
            return redirect('home')

        return render(request, 'base/delete.html', context)
    except Room.DoesNotExist:
        raise Http404("Invalid Room ID")


@login_required(login_url='/auth/login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerOrLoginView(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')

    if request.path_info == '/auth/register' and request.method == 'GET':
        form = UserCreationForm()
        context['form'] = form
    elif request.path_info == '/auth/login' and request.method == 'GET':
        form = AuthenticationForm()
        context['form'] = form
    elif request.path_info == '/auth/register' and request.method == 'POST':
        form = UserCreationForm(request.POST)

        if(form.is_valid()):
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            user.save()
            login(request, user)
            return redirect('auth/login')
        else:
            messages.error(
                request, 'An error occurred while registering. Please try again.')

    elif request.path_info == '/auth/login' and request.method == 'POST':
        try:
            form = AuthenticationForm(request, data=request.POST)

            if(form.is_valid()):
                user = authenticate(
                    request, username=form.cleaned_data['username'].lower(), password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'base/login_register.html', context)
