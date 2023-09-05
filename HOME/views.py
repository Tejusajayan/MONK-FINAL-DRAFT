import re
import json
import random
import datetime
import threading
from .models import *
from .forms import *
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

# TO ACTIVATE USER ACCOUNTS
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.views.generic import View
# TO ACTIVATE USER ACCOUNTS

# GETTING TOKENS
from .utils import TokenGenerator
# GETTING TOKENS

# SENDING MAILS
from django.core.mail import send_mail,EmailMultiAlternatives,BadHeaderError,EmailMessage
from django.core import mail
from django.conf import settings
# SENDING MAILS

#EXCEPTION HANDLING
from django.core.exceptions import ObjectDoesNotExist
#EXCEPTION HANDLING

#ONLINE PAYMENT
import razorpay
#ONLINE PAYMENT

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

class activate(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if(user is not None and TokenGenerator().check_token(user,token)):
            user.is_active=True
            user.save()
            cus=customer.objects.create(user=user,name=user.username)
            messages.info(request,'Account Is Created Successfully')
            return redirect('LOGIN')
        return render(request,'activatefail.html')


# Create your views here.
def index(request):
    featureobj=list(product.objects.filter(feature=True))
    newarrivalsobj=list(product.objects.filter(newarrivals=True))
    random.shuffle(featureobj)
    random.shuffle(newarrivalsobj)
    if(request.user.is_authenticated):
        return render(request,'index.html',{'featproduct':featureobj,'newarri':newarrivalsobj,'bool':True})
    else:
        return render(request,'index.html',{'featproduct':featureobj,'newarri':newarrivalsobj,'bool':False})    

def shop(request):
    proobj=list(product.objects.all())
    random.shuffle(proobj)
    return render(request,'shop.html',{'product':proobj})

def singleproduct(request,id):
    pro=product.objects.all()
    sproduct=product.objects.get(id=id)
    return render(request,'sproduct.html',{'pro':sproduct,'product':pro[:5]})

def addcart(request):
    if(request.user.is_authenticated):
        id=request.POST.get('product_id')
        size=request.POST.get('size')
        pro=product.objects.get(id=id)
        cus=customer.objects.get(user=request.user)
        if(cartitem.objects.filter(order=cus,product=pro,size=size).exists()):
            return JsonResponse({'msg':'Product Exists'})
        else:
            if(cartitem.objects.filter(order=cus).exists()):
                orderid=cartitem.objects.filter(order=cus).first()
                obj=cartitem(order=cus,product=pro,size=size,orderid=orderid.orderid,subtotal=pro.price)
                obj.save()
            else:
                orderid=random.randint(10000,99999)
                obj=cartitem(order=cus,product=pro,size=size,orderid=orderid,subtotal=pro.price)
                obj.save()
    return JsonResponse({'success':True})

def showcart(request):
    form=shippdet()
    if(request.user.is_authenticated==False):
        messages.info(request,'Please Login To See Your Cart.')
        return render(request,'cart.html',{'bool':False})
    else:
        cust=customer.objects.get(user=request.user)
        if(cartitem.objects.filter(order=cust).exists()==False):
            messages.info(request,'Your Cart Is Empty.')
            return render(request,'cart.html',{'bool':False})
        else:
            cartitems=cartitem.objects.filter(order=cust)
            total,subtotal=moneycalc(request)
            return render(request,'cart.html',{'cart':cartitems,'total':total,'subtotal':subtotal,'form':form,'bool':True})
            
def deletecart(request):
    id=request.POST.get('item_id')
    try:
        cust=customer.objects.get(user=request.user)
        cartitem(id=id).delete()
        total,subtotal=moneycalc(request)
        return JsonResponse({'success':True,'total':total,'subtotal':subtotal})
    except cartitem.DoesNotExist:
        return JsonResponse({'success':False,'error':'Cart item does not exist'})

def incq(request):
    id=request.POST.get('item_id')
    proc=request.POST.get('operation')
    cobj=cartitem.objects.get(id=id)
    cobj.quantity+=1
    cobj.subtotal=cobj.quantity*cobj.product.price
    cobj.save()
    total,subtotal=moneycalc(request)
    return JsonResponse({'success':True,'total':total,'subtotal':subtotal})

def decq(request):
    id=request.POST.get('item_id')
    proc=request.POST.get('operation')
    cobj=cartitem.objects.get(id=id)
    if(cobj.quantity==1):
        return JsonResponse({'msg':'1'})
    else:
        cobj.quantity-=1
        cobj.subtotal=cobj.quantity*cobj.product.price
        cobj.save()
        total,subtotal=moneycalc(request)
        return JsonResponse({'success':True,'total':total,'subtotal':subtotal})

def moneycalc(request):
    cust=customer.objects.get(user=request.user)
    cobj=cartitem.objects.filter(order=cust)
    subtotal=0
    for item in cobj:
        subtotal+=item.quantity*item.product.price
    total=subtotal+30
    money=(total,subtotal)
    return money

def contact(request):
    return render(request,'contact.html')

def msg(request):
    name=request.POST['name']
    mail=request.POST['email']
    subject=request.POST['subject']
    msg=request.POST['content']
    num=request.POST['number']
    message(name=name,email=mail,subject=subject,message=msg,number=num).save()
    messages.info(request,'We Received Your Response, We Will Contact You Soon.')
    return render(request,'contact.html')

def about(request):
    return render(request,'aboutus.html')

def log_in(request):
    if(request.method=='POST'):
        global username
        username=request.POST['username']
        password=request.POST['password']
        try:
            checkuser=User.objects.get(username=username)
            if(checkuser.is_active==False):
                messages.info(request,'Activate Your Account By Clicking The Link Send To Your Mail.')
                return render(request,'login.html',{'bool':True})
            else:
                user=authenticate(request,username=username,password=password)
                if(user is not None):
                    login(request,user)
                    return redirect('INDEX')
                else:
                    messages.info(request,'Invalid Credentials')
        except ObjectDoesNotExist:
            messages.info(request,'Create Account First.')
    return render(request,'login.html',{'bool':False})

def log_out(request):
    logout(request)
    return redirect('INDEX')

def forgetpassword(request):
    if(request.method=='POST'):
        mail=request.POST['email']
        username=request.POST['username']
        try:
            usermail=User.objects.get(username=username,email=mail)
            if(mail==usermail.email):
                global otp
                global mail1
                mail1=usermail.email
                otp=str(random.randint(10000,99000))
                subject="Reset Password Of Your Account"
                message="Your One Time Password For Reseting Your Account is: "+otp
                send_mail(subject,message,settings.EMAIL_HOST_USER,[usermail.email])
                return render(request,'forgetpassword.html',{'otpmsg':'OTP is successfully sent to your Email.','bool':True,'bool1':False})
        except ObjectDoesNotExist:
            return render(request,'forgetpassword.html',{"otpmsg":"Provide Correct Details",'bool':False,'bool1':True})
    return render(request,'forgetpassword.html',{"otpmsg":"",'bool':False,'bool1':True})

def redirectpg(request):
    if(request.method=='POST'):
        uotp=request.POST['otp']
        if(uotp==otp):
            return render(request,'resetpassword.html',{'vmsg':''})
        else:
            return render(request,'forgetpassword.html',{'otpmsg':'Incorrect OTP','bool':True})

def resetpassword(request):
    if(request.method=='POST'):
        pattern=r'^.{8,}$'
        pass1=request.POST['password']
        pass2=request.POST['repassword']
        if(pass1!=pass2):
            messages.info(request,'Password Is Not Matching.')
            return render(request,'resetpassword.html')
            print("matching problem")
        elif(bool(re.match(pattern,pass1))==False):
            print("character problem")
            messages.info(request,'Your Password Must Be Atleast 8 Characters Long.')
            return render(request,'resetpassword.html')
        else:
            uobj=User.objects.get(email=mail1)
            uobj.password=make_password(pass1)
            uobj.save()
            return redirect('LOGIN')

def create_ac(request):
    form=userform()
    if(request.method=='POST'):
        form=userform(request.POST)
        if(form.is_valid()):
            form.save()
            global loginer
            loginer=User.objects.get(username=form.cleaned_data['username'])
            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
                'user':loginer,
                'domain':'http://127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(loginer.pk)),
                'token':TokenGenerator().make_token(loginer)
            })
            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,
                                       [loginer.email])
            EmailThread(email_message).start()
            messages.success(request,'ACTIVATE YOUR ACCOUNT BY CLICKING LINK SEND TO YOUR MAIL')
            return redirect('LOGIN')
    return render(request,'accreate.html',{'form':form})

def resendlink(request):
    loginer=User.objects.get(username=username)
    email_subject="Activate Your Account"
    message=render_to_string('activate.html',{
                'user':loginer,
                'domain':'http://127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(loginer.pk)),
                'token':TokenGenerator().make_token(loginer)
            })
    email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,
                                       [loginer.email])
    EmailThread(email_message).start()
    messages.success(request,'ACTIVATE YOUR ACCOUNT BY CLICKING LINK SEND TO YOUR MAIL')
    return redirect('LOGIN')

def resetcart(request):
    cust=customer.objects.get(user=request.user)
    ordid=orderdescription.objects.get(cust=cust).transaction_id
    email=User.objects.get(username=request.user.username).email
    subject="Thank You For Shopping With Us."
    message="We have received your order ID: #"+str(ordid)+", and will be delivered\nwithing 7-15 days\nThank You for shopping with us"
    send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
    cartobjs=cartitem.objects.filter(order=cust)
    cartobjs.delete()
    return redirect('INDEX')
                
def payment(request):
    if(request.user.is_authenticated):
        form=shippdet()
        if(request.method=='POST'):
            val=request.POST['by']
            form=shippdet(request.POST)
            if(form.is_valid()):
                cus=customer.objects.get(user=request.user)
                ship,bool=address.objects.get_or_create(cust=cus)
                ods,boo=orderdescription.objects.get_or_create(cust=cus)
                cart=cartitem.objects.filter(order=cus)
                location=""
                ship.name=form.cleaned_data['name']
                ship.number=form.cleaned_data['number']
                ship.d_s_a=location=form.cleaned_data['doorno_street_area']
                ship.landmark=form.cleaned_data['landmark']
                location=location+" near "+form.cleaned_data['landmark']
                ship.pincode=form.cleaned_data['pincode']
                location=location+"\n"+form.cleaned_data['pincode']
                ods.address=location
                ship.save()

                orderdes=""
                for i in cart:
                    orderdes+=f'{i.product.product_id}---{i.size}---{i.quantity}\n'
                ods.items=orderdes
                total,subtotal=moneycalc(request)
                ods.amount=total
                if(val=='OP'):
                    ods.payment_type='ONLINE PAYMENT'
                    client=razorpay.Client(auth=('rzp_test_pX8GliFg8F8TDt','imIPZ0GJZCd9XM6kJhfXyCIS'))
                    razorpay_order=client.order.create(
                        {'amount':total*100,'currency':'INR','payment_capture':'1'}
                    )
                    porder=order.objects.create(
                        cus=cus,name=cus.name,amount=total,provider_order_id=razorpay_order["id"]
                    )
                    tid=random.randint(100000,999999)
                    ods.transaction_id=porder.trans_id=tid
                    ods.save()
                    porder.save()
                    callback_url = "http://" + "127.0.0.1:8000" + "/paysf/"
            
                    context = {}
                    context['razorpay_order_id'] = razorpay_order['id']
                    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                    context['currency'] = 'INR'
                    context['callback_url'] = callback_url
                    context['order']=porder
                    context['email']=User.objects.get(username=request.user.username).email
                    # context['name']=customer.objects.get(user=request.user).name
                    return render(request,'payhandler.html',context)
                elif(val=='COD'):
                    date=datetime.datetime.now()
                    ods.transaction_id=random.randint(100000,999999)
                    ods.payment_type="Cash On Delivery"
                    ods.save()
                    return render(request,'invoice.html',{'obj':ods,'date':date,'name':customer.objects.get(user=request.user).name,'cart':cart})
            else:
                return render(request,'cart.html',{'form':form})
    else:
        return redirect('CART')

@csrf_exempt
def paysf(request):
    def verify_signature(response_data):
        client=razorpay.Client(auth=('rzp_test_pX8GliFg8F8TDt','imIPZ0GJZCd9XM6kJhfXyCIS'))
        return client.utility.verify_payment_signature(response_data)
    
    if('razorpay_signature' in request.POST):
        pid=request.POST['razorpay_payment_id']
        poid=request.POST['razorpay_order_id']
        signid=request.POST['razorpay_signature']
        ord=order.objects.get(provider_order_id=poid)
        obj=orderdescription.objects.get(transaction_id=ord.trans_id)
        cusobj=obj.cust
        ord.payment_id=pid
        ord.signature_id=signid
        ord.save()
        if verify_signature(request.POST):
            ord.status='PAYMENT SUCCESS'
            date=datetime.datetime.now()
            name=ord.name
            cart=cartitem.objects.filter(order=cusobj)
            ord.is_paid=True
            obj.complete=True
            ord.save()
            return render(request,'invoice.html',{'obj':obj,'name':name,'date':date,'cart':cart})
        else:
            ord.status='PAYMENT FAILURE'
            ord.save()
            return render(request,'payfail.html')
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        ord = order.objects.get(provider_order_id=provider_order_id)
        ord.payment_id = payment_id
        ord.status = 'PAYMENT FAILURE'
        ord.save()
        return render(request, "payfail.html")