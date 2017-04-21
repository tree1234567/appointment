# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from datetime import datetime
from .models import *
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, 'appointments/index.html')


def home(request):
    today = datetime.now()
    user = User.objects.get(email=request.session['email'])
    context = {
        # 'reviews': Review.objects.all().order_by("-created_at")[:3],
        'user': User.objects.all(),
        'appointments': Appointment.objects.filter(user=user),
        'today': today.date()
    }
    return render(request,'appointments/home.html', context)



def register(request):
    if request.method == 'POST':
        birthday = request.POST['birthday']
        try:
            birthday_formatted = datetime.strptime(birthday, '%Y-%m-%d')
        except:
            messages.add_message(request, messages.ERROR, "please put in a Birthday")
            return redirect("appointments:index")
       
        user_dict = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password'],
            'birthday' : birthday_formatted           
            }
        
        register_result = User.objects.register(user_dict)]

        if register_result == True:
            request.session['name'] = request.POST['name']
            request.session['email']  = request.POST['email'] 
            return redirect('appointments:home')
        
        elif register_result[0] == False:
            for message in register_result[1]:
                messages.add_message(request, messages.ERROR, message)
        
    return redirect('appointments:index')

def login(request):
    
    if request.method == 'POST':
        user_dict = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        login_result = User.objects.login(user_dict)
        

        if login_result[0] == True:
            user = User.objects.get(email=user_dict['email'])
            request.session['email']=user.email
            request.session['name'] = user.name
            return redirect('appointments:home')
        if login_result[0] == False:
            for message in login_result[1]:
                messages.add_message(request, messages.ERROR, message)
            
    return redirect('appointments:index')

def logout(request):
    for key in request.session.keys():
        del request.session[key]

    return redirect('appointments:index')

def add_task(request):
    if request.method == "POST":
        date = request.POST['date']
        time = request.POST['time']
        today = datetime.now()
        if len(request.POST['task'])< 1:
            messages.add_message(request, messages.ERROR, "please add a description of the Task")
        try:
            date_formatted = datetime.strptime(date, '%Y-%m-%d')
            time_formatted = datetime.strptime(time, '%H:%M')

        except:
            messages.add_message(request, messages.ERROR, "please put in a Time/Date")
            return redirect("appointments:home")
        
        if date_formatted.date() >= today.date():

            user =User.objects.get(email=request.session['email'])
            
            Appointment.objects.create(task=request.POST['task'], date=date_formatted, time=time_formatted, status="pending",user=user)
        else:
            messages.add_message(request, messages.ERROR, "Tasks cannot be scheduled earlier than today (unless you own a DeLorean.. )")
    return redirect("appointments:home")


def delete_task(request, id):
    instance = Appointment.objects.get(id=id)
    instance.delete()
    return redirect("appointments:home")

def edit_task(request, id):

    context={
        "task": Appointment.objects.get(id=id)
    }
    

    return render(request, "appointments/edit_task.html", context)


def update_task(request, id):
    if request.method == "POST":
        task = Appointment.objects.get(id=id)
        
        today = datetime.now()
        if len(request.POST['date'])  ==  10 :
            date = request.POST['date']
              
            try:
                date_formatted = datetime.strptime(date, '%Y-%m-%d')
               
                # time_formatted = datetime.strptime(time, '%H:%M')
                if date_formatted.date() >= today.date():
                    task.date = date_formatted
                    # task.time = time_formatted
                   

                else:
                    messages.add_message(request, messages.ERROR, "Tasks cannot be scheduled earlier than today (unless you own a DeLorean.. )")
                    return redirect(reverse("appointments:edit_task", kwargs={"id":task.id}))
                
            except:
                messages.add_message(request, messages.ERROR, "please put in a Time/Date")
                return redirect(reverse("appointments:edit_task", kwargs={"id":task.id}))

        if len(request.POST['time']) == 5:
            time = request.POST['time']
            time_formatted = datetime.strptime(time, '%H:%M')
            task.time = time_formatted  

        if len(request.POST['task'])< 1:
            messages.add_message(request, messages.ERROR, "please add a description of the Task")
            return redirect(reverse("appointments:edit_task", kwargs={"id":task.id}))
        
        task.task= request.POST['task']
        task.status = request.POST['status']
        task.save()
            
    return redirect("appointments:home")