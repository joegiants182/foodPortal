from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from ..forms import *
from ..models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def addItem(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    thing = "Add Item"
    if( currUser.id == menu.curator.id or currUser.is_superuser ):
        form =ItemForm(request.POST or None)
        if form.is_valid():
            new_menu_item = form.save(commit=False)
            new_menu_item.menu_id = id
            new_menu_item.save()
            new_menu_item.option = request.POST.getlist('optionField')
            new_menu_item.save()
            messages.success(request, new_menu_item.name + ' added successfully.')
            return HttpResponseRedirect("/menus/" + str(menu.id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")

    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def addOption(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    thing = "Add Option"
    if( currUser.id == menu.curator.id or currUser.is_superuser ):
        form =OptionForm(request.POST or None)
        if form.is_valid():
            new_menu_item_option = form.save()
            new_menu_item_option.save()
            messages.success(request, new_menu_item_option.name + ' added successfully.')
            return HttpResponseRedirect("/menus/" + str(id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")

    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def editItem(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    item = Item.objects.get(id=id)
    options = item.option.filter(menu_id=item.menu.id)
    optionIds = [opt.name for opt in options]
    section = item.section
    thing = "Edit Item"

    if( currUser.id == section.menu.curator.id or currUser.is_superuser):
        try:
            request.POST['name']
            form = ItemForm(request.POST or None)
        except:
            form =ItemForm({'name' : item.name,
                                'section' : item.section,
                                'cost' : item.cost,
                                'description' : item.description,
                                'optionField' : options})

        if form.is_valid():
            new_menu_item = form.save(commit=False)
            if( item.name != new_menu_item.name ):
                item.name = new_menu_item.name
            if( item.section != new_menu_item.section ):
                item.section = new_menu_item.section
            if( item.cost != new_menu_item.cost ):
                item.cost = new_menu_item.cost
            if( item.description != new_menu_item.description ):
                item.description = new_menu_item.description
            if( item.option != request.POST.getlist('optionField') ):
                item.option = request.POST.getlist('optionField')
            item.save()
            messages.success(request, item.name + ' updated successfully.')
            return HttpResponseRedirect("/menus/" + str(item.menu.id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")

    return render(request, "menus/add.html", locals())

@login_required(login_url='/login/')
def editOptions(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    options = Option.objects.filter(menu_id=id)
    thing = "Edit Options"
    optionForms = []
    if( currUser.id == menu.curator.id or currUser.is_superuser ):
        try:
            request.POST['name']
            submitted = True
            form = OptionForm(request.POST or None)
            optionForms.append(form)
        except:
            initial = {}
            submitted = False
            for option in options:
                optionForms.append(OptionForm(initial={'name':option.name,
                                                       'description':option.description,
                                                       'optionId':option.id}))

        if optionForms[0].is_valid():
            try:
                option = Option.objects.get(id=request.POST['optionId'])
                if form.data['name'] != option.name:
                    option.name = form.data['name']
                if form.data['description'] != option.description:
                    option.description = request.POST[option.name + "_description"]
                option.save()
                messages.success(request, option.name + ' updated successfully.')
            except:
                pass
            return HttpResponseRedirect("/items/editOptions/" + str(id) + "/")
    else:
        messages.error(request,"You are neither the curator for this menu, nor a superuser, or the Menu does not exist.")
        return HttpResponseRedirect("/menus/all/")

    return render(request, "menus/add.html", locals())