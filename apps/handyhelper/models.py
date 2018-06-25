from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <2 or str.isalpha(postData['first_name']) == False:
            errors['first_name'] = 'First Name should be at least 2 characters and must be letters only'
        if len(postData['last_name']) <2 or str.isalpha(postData['last_name']) == False:
            errors['last_name'] = 'Last name should be at least 2 characters and must be letters only'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not a valid format'
        if postData['password'] != postData['passconf']:
            errors['passc'] = 'Passwords must match'
        if len(postData['password'])<8:
            errors['password'] = 'Password must be at least 8 characters'
        if len(User.objects.filter(email = postData['email'])) == 1:
            errors['email2'] = 'Email already in system'
        return errors
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['email_login'] = 'Email is not a valid format'
        try:
            user = User.objects.get(email = postData['login_email'])
            if not bcrypt.checkpw(postData['login_password'].encode(), user.password.encode()):
                errors['pass_login2'] = 'Try again'
        except ObjectDoesNotExist:
            errors['email_login2'] = 'Try again'
        
        return errors
class JobManager(models.Manager):
    def adding_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title_errors'] = 'Title is too short'
        if len(postData['description']) < 10:
            errors['description_errors'] = 'Description is too short'
        if len(postData['location']) < 1:
            errors['location_errors'] = 'Location is too short'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Job(models.Model):
    user = models.ForeignKey(User, related_name = 'jobs')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    flag = models.BooleanField(default = False)
    objects = JobManager()

class myjobs(models.Model):
    user = models.ForeignKey(User, related_name = 'myjobs')
    job = models.ForeignKey(Job, related_name = 'myjobs')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)