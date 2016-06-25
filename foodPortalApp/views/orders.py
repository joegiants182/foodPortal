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
        order = Order.objects.filter(status='Open').filter(menu_id=menu.id).get(customer__id = currUser.id)
        order.total = str(float(order.total) + float(orderItem.cost))
        order.orderItems.add(orderItem)
        order.save()
        messages.success(request, item.name + ' ' + option.name + ' was added to your open order for ' + menu.restaurant + '.')
    except:
        otherOrders = Order.objects.filter(customer_id=currUser.id)
        for other in otherOrders:
            if other.menu.id == menu.id and other.status != 'Closed':
                messages.error(request, "This customer already has a pending order for the same restaurant. Please close that order first and try again.")
                return HttpResponseRedirect("/home/")
        order = Order()
        order.customer = currUser
        order.status = 'Open'
        order.total = item.cost
        order.menu = item.menu
        order.save()
        order.orderItems.add(orderItem)
        order.save()
        messages.success(request, item.name + ' ' + option.name + ' was added to your new order for ' + menu.restaurant + '.')
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login/')
def view(request):
    currUser = Member.objects.get(id=request.user.id)
    orders = Order.objects.filter(customer__id=currUser.id).filter(~Q(status='Closed'))
    if len(orders) > 0:
        return render(request, "orders/view.html", locals())
    else:
        messages.error(request, "You do not have an order in progress, please create one by adding an item.")
        return HttpResponseRedirect("/menus/all/")

@login_required(login_url='login')
def removeItem(request, id):
    currUser = Member.objects.get(id=request.user.id)
    order = Order.objects.get(id=id)
    orderItem = OrderItem.objects.get(id=request.POST["orderItemId"])

    if (order != None and orderItem != None and (order.customer.id == currUser.id or request.user.is_superuser)):
        orderItems = order.orderItems
        for item in orderItems.all():
            if item.id == orderItem.id:
                order.total -= item.cost
                orderItems.remove(item)
                order.save()
                break
        messages.success(request, "Item successfully removed from order for " + order.menu.restaurant + ".")
        return HttpResponseRedirect("/orders/view/")
    else:
        messages.error(request, "This is not your order, you are not a superuser, or this order doesn't exist.")
        return HttpResponseRedirect("/home/")

@login_required(login_url='/login/')
def update(request, id):
    valid = True
    currUser = Member.objects.get(id=request.user.id)
    if request.POST['action'].split('-')[0] == 'curator':
        menu = Menu.objects.get(id=id)
        orders = Order.objects.all()
        if currUser.id != menu.curator.id:
            valid = False
    else:
        order = Order.objects.get(id=id)
        if currUser.id != order.customer.id:
            valid = False

    if request.user.is_superuser or valid:
        if request.POST['action'] == 'close':
            if order.status != 'Open' and order.status != 'In The Kitchen' and order.status != 'Placed':
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
                otherOrders = Order.objects.filter(customer_id=order.customer.id)
                for other in otherOrders:
                    if other.menu.id == order.menu.id and other.status != 'Closed':
                        messages.error(request, "This customer already has a pending order for the same restaurant. Please close that order first and try again.")
                        return HttpResponseRedirect("/home/")
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
        elif request.POST['action'] == 'curator-Placed':
            for order in orders:
                if order.status == 'Paid For':
                    order.status = 'On The Way'
                    order.save()
                elif order.status == 'Placed':
                    order.status = 'Open'
                    order.save()
            messages.success(request, "Orders marked On The Way for " + menu.restaurant + ". Any placed but not paid for orders were marked open.")
        elif request.POST['action'] == 'curator-Kitchen':
            for order in orders:
                if order.status == 'On The Way':
                    order.status = 'In The Kitchen'
                    order.save()
            messages.success(request, "Orders marked In The Kitchen for " + menu.restaurant + ".")
        else:
            messages.error(request, 'Invalid action')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])