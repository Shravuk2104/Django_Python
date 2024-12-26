from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from estoreapp.models import product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def index(request):
    #userid=request.user.id
    #print(userid)
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    print(p)
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)  

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)  


def pdetails(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'productdetails.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(userid)
        #print(pid)
        u=User.objects.filter(id=userid)
        print(u)
        print(u[0])
        p=product.objects.filter(id=pid)
        print(p)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(len(c))
        context={}
        context['products']=p
        n=len(c)
        if n==1:
            context['errmsg']="Product already exists in the Cart!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context["success"]="Product Added to cart!"
        return render(request,'productdetails.html',context)
    else:
        return redirect("/login")


def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c)
    #print(c[0])
    #print(c[0].uid)
    #print(c[0].pid)
    #print(c[0].pid.name)
    #print(c[0].pid.price)
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    print(s)
    np=len(c)
    context={}
    context['data']=c
    context['total']=s
    context['items']=np
    return render(request,'viewcart.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password not matching"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['successmsg']="User Registered Successfully!!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User Already Exists, use another emailID"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,upass)
        context={}
        if uname=="" or upass=="" :
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="Invalid Username or Password!"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def ulogout(request):
    logout(request)
    return redirect('/index')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)

    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print("Order id is:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['items']=np
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders)
    s=0
    for  x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_wIRW5UcLnuojt3", "TAWQaJo7pF8PxWMwC5MwnOQg"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    return render(request,'pay.html')


def senduseremail(request):
    try:
        send_mail(
        "Subject here",
        "Here is the message.",
        "shravanikhandagale0382@gmail.com",
        ["shravanikhandagale2104@gmail.com"],
        fail_silently=False,
        )
        return HttpResponse("Mail sent")
    except Exception:
        return HttpResponse("Mail sent")
