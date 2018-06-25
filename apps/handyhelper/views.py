from django.shortcuts import render, HttpResponse, redirect
from apps.handyhelper.models import *
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from djangounchained_flash import ErrorManager, ErrorMessage, getFromSession
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.

def index(request):
    # return HttpResponse("hello")
    if 'flash' not in request.session:
        request.session['flash'] = ErrorManager().addToSession()
    e = getFromSession(request.session['flash'])
    first_name_errors = e.getMessages('first_name')
    last_name_errors = e.getMessages('last_name')
    email_errors = e.getMessages('email')
    password_errors = e.getMessages('password')
    passc_errors = e.getMessages('passc')
    email2_errors = e.getMessages('email2')
    email_login_errors = e.getMessages('email_login')
    email2_login_errors = e.getMessages('email_login2')
    pass_login_errors = e.getMessages('pass_login2')
    request.session['flash'] = e.addToSession()
    context={
        'first_name_e':first_name_errors,
        'last_name_e':last_name_errors,
        'email_e': email_errors,
        'email2_e': email2_errors,
        'password_e':password_errors,
        'passc_e':passc_errors,
        'email_1':email_login_errors,
        'email_2':email2_login_errors,
        'pass_log':pass_login_errors
    }
        
    if 'first_name' not in request.session:
        return render(request, 'handyhelper/index.html', context)
    else:
        return redirect('/clear')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        e = getFromSession(request.session['flash'])
        if len(errors):
            for tag, error in errors.items():
                e.addMessage(error,tag)
            request.session['flash'] = e.addToSession()
            return redirect('/')
        # need to add another vaidator for login
        print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        conf = request.POST['passconf']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name = first_name, last_name = last_name, email = email, password = hash1)
        user = User.objects.get(first_name = first_name, last_name = last_name, email = email, password = hash1)
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['id']=user.id
        return redirect('/dashboard')
    else:
        return redirect('/')
    
def login(request):
    if request.method =='POST':
        email = request.POST['login_email']
        passw = request.POST['login_password']
        errors = User.objects.login_validator(request.POST)
        e = getFromSession(request.session['flash'])
        if len(errors):
            for tag, error in errors.items():
                e.addMessage(error, tag)
            request.session['flash'] = e.addToSession()
            return redirect('/')

        user = User.objects.get(email = email)
        if bcrypt.checkpw(passw.encode(), user.password.encode()):
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['id']=user.id
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')

def dashboard(request):
    # need the first_name, last_name, date
    if 'first_name' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['id'])
    myjob = myjobs.objects.all()
    
    context = {
        "user" : User.objects.get(id= request.session['id']),
        "jobs" : Job.objects.filter(flag = False).reverse().order_by('created_at'),
        "my_jobs": myjobs.objects.filter(user = user)
        }
    return render(request, 'handyhelper/dashboard.html', context)

def addjob(request):
    if 'flash' not in request.session:
        request.session['flash'] = ErrorManager().addToSession()
    e = getFromSession(request.session['flash'])
    title_errors = e.getMessages('title_errors')
    description_errors = e.getMessages('description_errors')
    location_errors = e.getMessages('location_errors')
    
    request.session['flash'] = e.addToSession()
    context={
        'title_e':title_errors,
        'desc_e':description_errors,
        'loc_e': location_errors,
    }

    return render(request, 'handyhelper/addjob.html', context)

def adding(request):
    errors = Job.objects.adding_validator(request.POST)
    e = getFromSession(request.session['flash'])
    if len(errors):
        for tag, error in errors.items():
            e.addMessage(error, tag)
        request.session['flash'] = e.addToSession()
        return redirect('/addJob/')
    user = User.objects.get(id = request.session['id'])
    Job.objects.create(user = user, title=request.POST['title'], description=request.POST['description'], location=request.POST['location'])
    return redirect('/dashboard')

def view(request, numbers):
    context = {"jobs": Job.objects.get(id = numbers)}
    return render(request, 'handyhelper/view.html', context)

def addtouser(request,numbers):
    user = User.objects.get(id = request.session['id'])
    job = Job.objects.get(id = numbers)
    job.flag = True
    job.save()
    myjobs.objects.create(user = user, job = job)
    return redirect('/dashboard')

def edit(request, numbers):
    if request.session['id'] != Job.objects.get(id=numbers).user.id:
        return redirect('/dashboard')
    if 'flash' not in request.session:
        request.session['flash'] = ErrorManager().addToSession()
    e = getFromSession(request.session['flash'])
    title_errors = e.getMessages('title_errors')
    description_errors = e.getMessages('description_errors')
    location_errors = e.getMessages('location_errors')
    
    request.session['flash'] = e.addToSession()
    context={
        'title_e':title_errors,
        'desc_e':description_errors,
        'loc_e': location_errors,
    }
    context = {"jobs": Job.objects.get(id = numbers)}
    return render(request, 'handyhelper/edit.html', context)

def editing(request, numbers):
    errors = Job.objects.adding_validator(request.POST)
    e = getFromSession(request.session['flash'])
    if len(errors):
        for tag, error in errors.items():
            e.addMessage(error, tag)
        request.session['flash'] = e.addToSession()
        return redirect('/addJob/')
    user = User.objects.get(id = request.session['id'])
    job = Job.objects.get(id = numbers)
    # job.user = user
    job.title = request.POST['title']
    job.description = request.POST['description']
    job.location = request.POST['location']
    job.save()
    return redirect('/dashboard')

def delete(request, numbers):
    job = Job.objects.get(id=numbers)
    try:
        myjob = myjobs.objects.get(job = job)
        myjob.delete()
        job.delete()
    except:
        job.delete()

    return redirect('/dashboard')


def clear(request):
    if 'first_name' in request.session:
        del request.session['first_name']
    if 'last_name' in request.session:
        del request.session['last_name']
    if 'id' in request.session:
        del request.session['id']
    return redirect('/')