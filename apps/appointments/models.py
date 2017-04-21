# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASS_REGEX = re.compile(r'^\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def register(self, user_dict):
        error_list = []
        properly_validated = True

        if len(user_dict['name']) < 2:
            error_list.append('Name too short')
            properly_validated = False

        if len(user_dict['password']) < 8:
            error_list.append('Password is too short')
            properly_validated = False

        if user_dict['password'] != user_dict['confirm_password']:
            error_list.append('Passwords do not match')
            properly_validated = False

        if not EMAIL_REGEX.match(user_dict['email']):
            error_list.append('email  too short')
            properly_validated = False
            
        if not NAME_REGEX.match(user_dict['name']):
            error_list.append('Name can only have letters')
            properly_validated = False

        

        # if not PASS_REGEX.match(user_dict['password']):
        #     error_list.append('Password requires upper case and special character')
        #     properly_validated = False
        
        if properly_validated == True:
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(str(user_dict['password']), salt)
            try:
                User.objects.create(name=user_dict['name'], email=user_dict['email'], password=hashed_pw, salt=salt, birthday=user_dict['birthday'])
                return (properly_validated)
            except:
                properly_validated = False
                error_list.append('Email is already registered')
                return(properly_validated, error_list)
        else:
            return(properly_validated, error_list)
    
    
    
    
    def login(request, user_dict):
        error_list = []
        properly_logged = True
        try:
            user = User.objects.get(email=user_dict['email'])
        except:
            properly_logged = False
            error_list.append("Email does not exist, please register")
            return(properly_logged, error_list)
        
        if bcrypt.hashpw(str(user_dict['password']), str(user.salt)) != user.password:
            properly_logged = False
            error_list.append("Password invalid")
            return (properly_logged, error_list)

        else:
            return (properly_logged, error_list)


class User(models.Model):
    name = models.CharField(max_length=100)
    email=models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100, default="$2b$12$pTnZS9g9dWx1ZveqSkHL5e")
    birthday = models.DateField()
    objects = UserManager()


class Appointment(models.Model):
    task = models.CharField(max_length=100)
    date= models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, default="Pending")
    user = models.ForeignKey(User, related_name="appointments")

