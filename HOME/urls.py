from django.urls import path
from . import views

urlpatterns=[
                path('',views.index,name='INDEX'),
                path('shop/',views.shop,name='SHOP'),
                path('contact/',views.contact,name='CONTACT'),
                path('product/<int:id>/',views.singleproduct,name='SINGLEPRO'),
                path('aboutus/',views.about,name='ABOUT'),
                path('login/',views.log_in,name='LOGIN'),
                path('logout/',views.log_out,name='LOGOUT'),
                path('activate/<uidb64>/<token>',views.activate.as_view(),name='ACTIVATE'),
                path('accreate/',views.create_ac,name='CREATEACC'),
                path('addcart/',views.addcart,name='ADDCART'),
                path('forgetpassword/',views.forgetpassword,name='FORGETPASSWORD'),
                path('resetpassword/',views.resetpassword,name='RESET'),
                path('otpverification/',views.redirectpg,name='REDIRECTPG'),
                path('showcart/',views.showcart,name='SHOWCART'),
                path('deletecart/',views.deletecart,name='DELETE'),
                path('incq/',views.incq,name='INCQ'),
                path('decq/',views.decq,name='DECQ'),
                path('payment/',views.payment,name='PAYMENT'),
                path('paysf/',views.paysf,name='PAYSF'),
                path('message/',views.msg,name='MESSAGE'),
                path('recar/',views.resetcart,name='RESETCART'),
                path('resendlink/',views.resendlink,name='RESENDL')
]