from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from ..forms import *
from ..models import *
from django.contrib.auth.decorators import login_required
from django import forms

def index(request):
    """
        Renders the homepage.
        
        - If your are signed in, the page redirects to the dashboard
        - If you are not, the page renders.
        - The registration form submits to this page, and then validates/shows errors
        - If the registration form is submitted correctly, the user is redirected to the login page
        
        Parameters:
            request - Django Request
    """
    
    # Redirect if authenticated
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    
    form = RegistrationForm(request.POST or None)

    # If the registration form is valid
    if form.is_valid():
    
        # Check for unique email
        if Member.objects.filter(email=form.data['email']).exists():
            error = form._errors.setdefault('email', forms.ErrorList())
            error.append("Email is already registered.")
            return render(request, "index.html", locals())

        try :
            int(form.data['phoneNumber'])
            # Negative Phone Number???
            if (int(form.data['phoneNumber']) < 0):
                error = form._errors.setdefault('phoneNumber', forms.ErrorList())
                error.append("phoneNumber cannot be negative.")
                return render(request, "index.html", locals())
            # Less Than 10 Digits Phone Number???
            if (len(form.data['phoneNumber']) != 10):
                error = form._errors.setdefault('phoneNumber', forms.ErrorList())
                error.append("Phone Number should be 10 digits long.")
                return render(request, "index.html", locals())
        except ValueError:
            error = form._errors.setdefault('phoneNumber', forms.ErrorList())
            error.append("Phone Number can only contain numbers.")
            return render(request, "index.html", locals())

        # Create the user and redirect to login
        user = Member.objects.create_user(form.data['username'],form.data['email'],form.data['password'],
                                          phoneNumber=form.data['phoneNumber'], room=form.data['room'],
                                          bio=form.data['bio'],first_name=form.data['first_name'],
                                        last_name=form.data['last_name'])
        messages.success(request, 'Account Created Successfully')
        return HttpResponseRedirect("/login/")

    # Render the page
    return render(request, "index.html", locals())

def login(request):
    """
        Renders the login page.
        
        - Validates form on submissions, and then check if they are valid credentials
        - If valid auth, the user is redirected to the dashboard
        
        Parameters:
            request - Django Request
    """
    
    # Redirect to home if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")

    form = AuthenticationForm(data=request.POST or None)
    
    # the bootstrap class to each form element
    for field in form.fields:
        form.fields[field].widget.attrs.update({'class' : 'form-control'})
    
    # If the user submitted the login form and it is valid
    if form.is_valid():
        username = form.data['username']
        password = form.data['password']
        
        # Try to authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                
                # Authorize the user then redirect to the dashboard
                auth_login(request, user)
                return HttpResponseRedirect("/home/")
            else:
                
                # If inactive, let them know
                messages.error(request, "Account Inactive")
                return render(request, "login.html", locals())

    return render(request, "users/login.html", locals())

@login_required(login_url='/login/')
def logout(request):
    """
        Logs out the current user
        
        Preconditions:
            User is authenticated
        
        Parameters:
            request - Django Request
    """
    auth_logout(request)

    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def home(request):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    try:
        myMenus = Menu.objects.filter(Q(curator_id=currUser.id))
        numMenus = len(myMenus)
    except ObjectDoesNotExist:
        numMenus = 0

    try:
        myOpenOrders = Order.objects.filter(Q(customer_id=currUser.id)).filter(~Q(status='Closed'))
        numOpenOrders = len(myOpenOrders)
    except ObjectDoesNotExist:
        numOpenOrders = 0

    try:
        myClosedOrders = Order.objects.filter(Q(customer_id=currUser.id)).filter(Q(status='Closed'))
        numClosedOrders = len(myClosedOrders)
    except ObjectDoesNotExist:
        numClosedOrders = 0

    return render(request, "users/home.html", locals())
