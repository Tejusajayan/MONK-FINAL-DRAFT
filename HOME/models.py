from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class product(models.Model):
    product_id=models.PositiveIntegerField(default=0)
    brand=models.CharField(max_length=30)
    proname=models.CharField(max_length=50)
    starrating=models.DecimalField(max_digits=3,decimal_places=2,default=0)
    price=models.PositiveIntegerField()
    size_choice=(('S','Small'),('M','Medium'),('L','Large'),('XL','Extra-Large'),('XXL','Extra-Extra-Large'))
    feature=models.BooleanField(default=False)
    newarrivals=models.BooleanField(default=False)
    mainimg=models.ImageField(upload_to='DRESS')
    subimg1=models.ImageField(upload_to='DRESS')
    subimg2=models.ImageField(upload_to='DRESS')
    subnimg3=models.ImageField(upload_to='DRESS')
    subimg4=models.ImageField(upload_to='DRESS')

    def __str__(self):
        return str(self.product_id)

class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class cartitem(models.Model):
    order=models.ForeignKey(customer,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    size=models.CharField(max_length=3,default='')
    quantity=models.PositiveIntegerField(default=1)
    subtotal=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    orderid=models.CharField(max_length=10)

    def __str__(self):
        return self.orderid 

class address(models.Model):
    cust=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=30,default="")
    d_s_a=models.TextField(default="")
    landmark=models.CharField(max_length=30,default="")
    pincode=models.PositiveIntegerField(default=0)
    number=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.cust.name

class orderdescription(models.Model):
    cust=models.ForeignKey(customer,on_delete=models.CASCADE,blank=True,null=True)
    transaction_id=models.PositiveIntegerField(default=0)
    date_ordered=models.DateTimeField(auto_now_add=True)
    items=models.TextField(default="")
    complete=models.BooleanField(default=False)
    amount=models.PositiveIntegerField(default=0)
    address=models.TextField(default="")
    payment_type=models.CharField(max_length=30,default='-')

    def __str__(self):
        if(self.complete==True):
            return f"{self.cust.name}-----Completed"
        else:
            return f"{self.cust.name}-----Not Completed"
    
class order(models.Model):
    cus=models.ForeignKey(customer,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(_("Customer Name"),max_length=20,blank=False,null=False)
    amount=models.FloatField(_("Amount"),null=False,blank=False)
    trans_id=models.PositiveIntegerField(default=0)
    status=models.CharField(
        _("Payment Status"),
        default="PENDING",max_length=254,null=False,blank=False
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return str(self.trans_id)

class message(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    number=models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.name