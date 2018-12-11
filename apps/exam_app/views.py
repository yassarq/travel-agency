from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    context = {
            # 'users' : User.objects.all()
        }
    return render(request, 'exam_app/index.html', context)


def register(request):
    results = User.objects.regValidator(request.POST)
    if results[0] == True:
        request.session['id'] = results[1].id
        request.session['first_name'] = results[1].name
        return redirect('/dashboard')
    else:
        error_list = results[1]
        for error in error_list:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def dashboard(request):
    if 'id' in request.session:
        context = {
        'mytrips':Trip.objects.filter(planner_id=request.session['id']) | Trip.objects.filter(joiners__id = request.session['id']), 
        'othertrips': Trip.objects.exclude(planner = request.session['id']) & Trip.objects.exclude(joiners__id = request.session['id']) ,

        
        }
        return render(request, 'exam_app/dashboard.html', context)
    else:
        return redirect('/')

def login(request):
    results = User.objects.loginValidator(request.POST)
    if results[0] == True:
        request.session['id'] = results[1].id
        request.session['first_name'] = results[1].name
        return redirect('/dashboard')
    else:
        error_list = results[1]
        for error in error_list:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    return render(request, 'exam_app/add.html')

def createtrip(request):
    results = Trip.objects.tripValidator(request.POST,request.session['id'])
    if results[0] == True:
        return redirect('/dashboard')
    else:
        error_list = results[1]
        for error in error_list:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/add')

def show(request, trip_id):
    context = {
        'trip': Trip.objects.get(id = trip_id),
        
    }
    return render(request, 'exam_app/show.html', context)

def join(request, trip_id):
    Trip.objects.get(id = trip_id).joiners.add(User.objects.get(id = request.session['id']))

    return redirect('/dashboard')