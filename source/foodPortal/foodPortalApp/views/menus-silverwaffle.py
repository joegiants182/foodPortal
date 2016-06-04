from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from ..forms import *
from ..models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def all(request):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    qset = Q(is_active=True)

    results = Menu.objects.all().filter(qset)
    return render(request, "menus/index.html", locals())

@login_required(login_url='/login/')
def view(request, id=None):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    sections = MenuSection.objects.filter(Q(menu_id=id))
    items = Item.objects.filter(Q(menu_id=id))
    options = Option.objects.filter(menu_id=id)
    # Check if menus exists
    if menu is not None:
        return render(request, "menus/view.html", locals())

@login_required(login_url='/login/')
def add(request):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    form =MenuForm(request.POST or None)
    thing = "Add Menu"
    # If the add menus form is submitted and it is valid
    if form.is_valid():
        new_menu = form.save(commit=False)
        new_menu.curator_id = currUser.id
        new_menu.save()
        messages.success(request, new_menu.restaurant + ' added successfully.')
        
        # Redirect to the dashboard
        return HttpResponseRedirect("/home/")

    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def addSection(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    thing = "Add Section"
    if( currUser.id == menu.curator.id or currUser.is_superuser):
        form =SectionForm(request.POST or None)
        if form.is_valid():
            new_section = form.save(commit=False)
            new_section.menu_id = id
            new_section.save()
            messages.success(request, new_section.name + ' added successfully.')
            return HttpResponseRedirect("/menus/" + str(id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")
    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def editSection(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    section = MenuSection.objects.get(id=id)
    thing = "Edit Section"
    if( currUser.id == section.menu.curator.id or currUser.is_superuser):
        form =SectionForm(request.POST or None, initial={'name' : section.name})
        if form.is_valid():
            section.name = form.data['name']
            section.save()
            messages.success(request, section.name + ' updated successfully.')
            return HttpResponseRedirect("/menus/" + str(section.menu.id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")

    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def disable(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    if (not currUser.is_superuser):
        messages.error(request,"You do not have superuser privileges.")
        return HttpResponseRedirect("/home/")
    else:
        menu = Menu.objects.get(id=id)
        if(not menu.is_active):
            messages.error(request,menu.restaurant + " is already deactivated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/home/'))
        menu.is_active = False
        menu.save()
        messages.success(request,menu.restaurant + " has been deactivated.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/home/'))

@login_required(login_url='/login/')
def enable(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    if (currUser.is_superuser == False):
        messages.error(request,"You do not have superuser privileges.")
        return HttpResponseRedirect("/home/")
    menu = Menu.objects.get(id=id)
    if menu.is_active:
        messages.error(request,menu.restaurant + " is already active!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/home/'))
    menu.is_active = True
    menu.save()
    messages.success(request,menu.restaurant + " activated.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/home/'))