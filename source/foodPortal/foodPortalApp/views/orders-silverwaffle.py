from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from ..forms import *
from ..models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required(login_url='/login/')
def addTo(request, id):
    currUser = Member.objects.get(user_ptr_id=request.user.id)
    menu = Menu.objects.get(id=id)
    item = Item.objects.get(id=request.POST['itemId'])
    option = Option.objects.get(id=request.POST['optionId'])
    orderItem = OrderItem()
    orderItem.option = option
    orderItem.item = item
    orderItem.cost = item.cost
    orderItem.save()
    try:
        order = Order.objects.filter(status='Open').get(customer__id = currUser.id)
        order.total = str(float(order.total) + float(orderItem.cost))
        order.orderItems.add(orderItem)
        order.save()
        messages.success(request, item.name + ' ' + option.name + ' was added to your open order.')
    except:
        order = Order()
        order.customer = currUser
        order.status = 'Open'
        order.total = item.cost
        order.menu = item.menu
        order.save()
        order.orderItems.add(orderItem)
        order.save()
        messages.success(request, item.name + ' ' + option.name + ' was added to your new order.')
    return HttpResponseRedirect("/menus/" + str(menu.id) + "/")

@login_required(login_url='/login/')
def view(request, id):
    currUser = Member.objects.get(id=request.user.id)
    order = Order.objects.get(id=id)
    if order.customer_id != currUser.id and not request.user.is_superuser:
        messages.error(request, "This is neither your order, nor are you a superuser.")
        return HttpResponseRedirect("/home/")
    else:
        orderItems = order.orderItems
        menuId = orderItems.all()[0].item.menu.id
        menu = Menu.objects.get(id=menuId)
        return render(request, "orders/view.html", locals())

@login_required(login_url='/login/')
def findMyOrder(request):
    currUser = Member.objects.get(id=request.user.id)
    order = Order.objects.filter(customer__id=currUser.id).filter(~Q(status='Closed'))
    if order != None:
    	return HttpResponseRedirect("/orders/view/" + str(order[0].id) + "/")
    else:
    	messages.error(request, "You do not have an order in progress, please create one.")
    	return HttpResponseRedirect("/menus/all/")

@login_required(login_url='/login/')
def update(request, id=''):
    currUser = Member.objects.get(id=request.user.id)
    try:
        currUserOrder = Order.objects.filter(customer_id=currUser.id).filter(status__in=['Open','Placed','Paid For','On The Way','In The Kitchen'])
    except:
        currUserOrder = None
    order = Order.objects.get(id=id)
    if order is None or not request.POST.has_key('action'):
        messages.error(request, 'Order not found, or no action was chosen.')
        return HttpResponseRedirect("/home/")

    if request.user.is_superuser() or request.user.id == order.customer_id or order.menu.curator.id == request.user.id:
        if request.POST['action'] == 'close':
            if order.status != 'Open' or 'In The Kitchen':
                messages.error(request, "This order is currently in progress, and cannot be closed.")
                return HttpResponseRedirect("/")
            else:
                order.status = 'Closed'
                order.save()
                messages.success(request, "Your open order has been closed. Go to your order history to re-open it. You can only have one open order at a time.")
        elif request.POST['action'] == 'open':
            if order.status != 'Closed':
                messages.error(request, "This order is not closed, and therefore cannot be opened.")
                return HttpResponseRedirect("/home/")
            else:
                order.status = 'Open'
                order.save()
                messages.success(request, "Your closed order has been re-opened.")
        elif request.POST['action'] == 'place':
            if order.status != 'Open':
                messages.error(request, "An order can only be placed if it is open.")
                return HttpResponseRedirect("/home/")
            else:
                order.status = 'Placed'
                order.save()
                messages.success(request, "Your order has been placed.")
        elif request.POST['action'] == 'pay':
            if order.status != 'Placed':
                messages.error(request, "You can only mark paid an order that is placed.")
                return HttpResponseRedirect("/home/")
            else:
                order.status = 'Paid For'
                order.save()
                messages.success(request, order.customer.get_full_name() + "'s order from " + order.menu.restaurant + " has been marked as paid.")
        else:
            messages.error(request, 'Invalid action')
        return HttpResponseRedirect("/home/")