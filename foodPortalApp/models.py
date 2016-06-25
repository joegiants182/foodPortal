from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

class Member(User):
    phoneNumber = models.CharField(max_length=10)
    room = models.CharField(max_length=4)
    bio = models.TextField(default="None :'(", max_length=1024)

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return smart_text(self.email)

class Menu(models.Model):
    restaurant = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    image = models.URLField(max_length=200, blank=True)
    curator = models.ForeignKey(Member, related_name='curator', default=1)

    def __str__(self):
        return self.restaurant

class MenuSection(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, related_name="menu")
    def __str__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, related_name="optionMenu", default=1)
    description = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

    @property
    def price(self):
        return "$%s" % self.price

class Item(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, related_name="itemMenu", default=1)
    section = models.ForeignKey(MenuSection, related_name="section", default=1)
    option = models.ManyToManyField(Option, related_name='options')
    cost = models.CharField(max_length=7, default='0.00')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    item = models.ForeignKey(Item)
    option = models.ForeignKey(Option)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
    STATUSES = (
        ('Open', 'Open'),
        ('Placed', 'Placed'),
        ('Paid For', 'Paid For'),
        ('On The Way', 'On The Way'),
        ('In The Kitchen', 'In The Kitchen'),
        ('Closed', 'Closed'),
    )
    orderItems = models.ManyToManyField(OrderItem)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(default='Open', max_length=256, choices=STATUSES)
    menu = models.ForeignKey(Menu, default=1)
    customer = models.ForeignKey(Member, related_name="customer", default=1)
    dateCreated = models.DateField(auto_now_add=True)
    timeCreated = models.TimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.status + '_' + self.dateCreated.__str__() + '_' + self.timeCreated.__str__()

    @property
    def price(self):
        return "$%s" % self.price