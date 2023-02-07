from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import render, get_object_or_404
from django import forms

from mysite import settings
from user import models
from django.shortcuts import render, HttpResponse, redirect

from user.models import User, Order

TypeOfVehicle = {
        ('SUV','SUV'),
        ('Sedan','Sedan'),
        ('Sports Car','Sports Car'),
    }
class SharerSearchForm(forms.Form):
    destination = forms.CharField(label="destination", max_length=128,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    earliest_time = forms.DateTimeField(
        label="earliest time",
        input_formats=['%m/%d/%y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    latest_time = forms.DateTimeField(
        label="latest time",
        input_formats=['%m/%d/%y %H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    passenger_number = forms.IntegerField(label="passenger number", validators=[
        MinValueValidator(1), MaxValueValidator(10)
    ])


class OwnerRideForm(forms.Form):

    destination = forms.CharField(label="destination", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrival_time = forms.DateTimeField(label="arrival time",
    input_formats = ['%m/%d/%y %H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    passenger_number = forms.IntegerField(label="passenger number",validators=[
            MinValueValidator(1), MaxValueValidator(10)
        ])
    CHOICES = [('False', 'False'),('True', 'True')]
    is_shared = forms.BooleanField()
    special_request = forms.CharField(label="special request", max_length=128, required = False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_vehicle_type = forms.CharField(label="special vehicle type", max_length=128,required = False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class OwnerModelForm(forms.ModelForm):
    class Meta:
        model=models.Order
        fields=['destination','arrival_time','passenger_number','is_shared','special_request','special_vehicle_type']
        widgets = {'arrival_time': forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M')}

class ShareModelForm(forms.ModelForm):
    class Meta:
        model=models.Order
        fields=['passenger_number']
class OrderModelForm(forms.ModelForm):
    class Meta:
        model=models.Order
        fields=['destination','arrival_time','passenger_number','is_shared','special_request','special_vehicle_type']
        widgets = {'arrival_time': forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M')}
class UserModelFormDriver(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['username','email','sex','full_name','vehicle_type','plate_num','max_passenger','special_vehicle_info']
class UserModelFormNotDriver(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['username','email','sex']


class DriverModelForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['full_name','vehicle_type','plate_num','max_passenger','special_vehicle_info']

class LoginForm(forms.Form):
    username=forms.CharField(label="Username",widget=forms.TextInput,required=True)
    password = forms.CharField(label="password",widget=forms.PasswordInput,required=True)

class LoginModelForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['username','password','email']

# Create your views here.
def welcome(request):
    info=request.session.get("info")
    if info:
        return redirect('/main/')
    return render(request, 'welcome.html')

def login(request):
    if request.method =="GET":
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    form=LoginForm(data=request.POST)
    if form.is_valid():
        info_object = models.User.objects.filter(**form.cleaned_data).first()
        if not info_object:
            form.add_error("password", "There is something wrong with your Username or Password!")
            return render(request,'login.html',{'form':form})

        request.session["info"] = {'id': info_object.id, 'name': info_object.username}
        request.session['user_id'] = info_object.id
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/main/')
    else:
        return render(request,'login.html',{'form':form})


def creataccount(request):
    if request.method =="GET":
        form=LoginModelForm()
        return render(request,'creataccount.html',{'form':form})
    form = LoginModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'creataccount.html', {'form': form})

def main(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    orders = Order.objects.filter(completed=False).order_by("id")

    return render(request,'main.html',locals())
def ViewOwner(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    orders=Order.objects.filter(owner__username=user.username).order_by("id")

    return render(request,'ViewOwner.html',locals())


def ViewSharer(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    All = Order.objects.order_by("id")
    orders=[]
    for temporder in All.all():
        for tempshare in temporder.sharer.all():
            if tempshare.username==user.username:
                orders.append(temporder)
                break
    return render(request, 'ViewSharer.html', locals())
def EditOrder(request, nid):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    row_object=Order.objects.filter(id=nid).first()
    mark = False
    for temp in row_object.sharer.all():
        if temp.username == user.username:
            mark = True
    if request.method=="GET":
        if row_object.is_comfirmed:
            message = "You cannot edit this order! It has been comfirmed!"
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(completed=False).order_by("id")
            return render(request, 'main.html', locals())

        if row_object.owner.username!=user.username and not mark :
            message = "You cannot edit this order!"
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(completed=False).order_by("id")
            return render(request, 'main.html', locals())
        elif row_object.owner.username==user.username:
            open_ride_form = OrderModelForm(instance=row_object)
            return render(request, 'EditOrder.html', locals())
        elif mark:
            return render(request,'ShareEdit.html')
    if request.method == 'POST':
        if mark and row_object.owner.username!=user.username:
            AddPassenger=int (request.POST.get("passenger"))

            Order.objects.filter(id=nid).update(passenger_number=row_object.passenger_number+AddPassenger)
            return redirect('/main/')
        open_ride_form = OrderModelForm(data=request.POST,instance=row_object)
        message = "please check the input!"
        if open_ride_form.is_valid():
            open_ride_form.save()
            return redirect('/main/')
        return render(request, 'EditOrder.html', locals())



def DriverReg(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method=="GET":
        if user.is_driver:
            message = "You are a driver right now!"
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(completed=False).order_by("id")
            return render(request, 'main.html', locals())
        driver_form = DriverModelForm(instance=user)
        return render(request, 'DriverReg.html', locals())

    if request.method == 'POST':
        driver_form=DriverModelForm(request.POST,instance=user)
        print("s")
        if driver_form.is_valid():
            driver_form.save()
            user.is_driver=True
            user.save()
            return redirect('/main/')
        message="invalid input!"
        return render(request, 'DriverReg.html', locals())

# condsider to use modelform to edit
def DriverEdit(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if user.is_driver==False:
        return redirect('/DriverReg/')
    if request.method == 'POST':
        driver_form = DriverModelForm(request.POST,instance=user)
        message = "please check the input!"
        if driver_form.is_valid():
            driver_form.save()
            return redirect('/main/')
        return render(request, 'DriverEdit.html', locals())
    driver_form = DriverModelForm(instance=user)
    return render(request, 'DriverEdit.html', locals())

def ViewInfo(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    return render(request,'ViewInfo.html',locals())

def EditInfo(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method=='GET':
        if user.is_driver:
            ChangeModel=UserModelFormDriver(instance=user)
            return render(request,'EditInfo.html',locals())
        else:
            ChangeModel = UserModelFormNotDriver(instance=user)
            return render(request, 'EditInfo.html', locals())

    if request.method=='POST':
        if user.is_driver:
            Receive=UserModelFormDriver(data=request.POST,instance=user)
            if Receive.is_valid():
                Receive.save()
                return redirect('/main/')
            return render(request, 'EditInfo.html', locals())
        else:
            Receive=UserModelFormNotDriver(data=request.POST,instance=user)
            if Receive.is_valid():
                Receive.save()
                return redirect('/main/')
            return render(request, 'EditInfo.html', locals())
## need to be changed
def RideReq(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == "GET":
        open_ride_form = OwnerModelForm()
        return render(request, 'RideReq.html', locals())
    if request.method=="POST":
        order=Order()
        open_ride_form = OwnerModelForm(request.POST,instance=order)
        message = "please check the input!"

        if open_ride_form.is_valid():
            passenger_number = open_ride_form.cleaned_data.get('passenger_number')
            if passenger_number > 10 or passenger_number < 1:
                message = "input time is invalid!"
                return render(request, 'RideReq.html', locals())

            open_ride_form.save()

            order.owner=user
            order.save()
            return redirect('/main/')
        return render(request, 'RideReq.html', locals())
def FindDrive(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method=="GET":
        if not user.is_driver:
            message = "Sorry you are not a drive, register as a driver right now!"
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(completed=False).order_by("id")
            return render(request, 'main.html', locals())
        else:
            orders=Order.objects.filter(is_comfirmed=False).filter(passenger_number__lte=user.max_passenger).filter().exclude(owner__username=user.username)
            return render(request, 'FindDrive.html', locals())

def BeDriver(request,nid):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    row_object = Order.objects.filter(id=nid).first()
    Order.objects.filter(id=nid).update(driver=user)
    Order.objects.filter(id=nid).update(is_comfirmed=True)
    temporder=Order.objects.filter(id=nid).first()
    email_title = 'Your order has been confirmed!'
    email_body = 'Your order ('+ str(temporder.owner.username) +')'+' to '+str(temporder.destination)+' at '+str(temporder.arrival_time)+' has been confirmed.'
    email = temporder.owner.email
    send_mail(email_title, email_body, settings.EMAIL_FROM,[email])
    for temp in temporder.sharer.all():
        tempemail=temp.email
        temp_email_body = 'your order (' + str(temp.owner.username) + ')' + ' to ' + str(
            temporder.desination) + ' at ' + str(temporder.arrival_time) + ' has been confirmed.'
        send_mail(email_title, temp_email_body, settings.EMAIL_FROM, [tempemail])


    return redirect('/FindDrive/')
def ViewDrive(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    orders = Order.objects.filter(driver__username=user.username).filter(completed=False).order_by("id")
    return render(request, 'ViewDrive.html', locals())

def Complete(request,nid):
    Order.objects.filter(id=nid).update(completed=True)

    return redirect('/ViewDrive/')
def JoinIt(request,nid):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    Order.objects.filter(id=nid).first().sharer.add(user)
    temp=Order.objects.filter(id=nid).first().passenger_number
    global Full_passenger_number
    Order.objects.filter(id=nid).update(passenger_number=temp+Full_passenger_number)
    return redirect('/main/')
def History(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    orders = Order.objects.filter(driver__username=user.username).order_by("id")
    return render(request, 'History.html', locals())

Full_passenger_number=0
def Join(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method=="GET":

        SearchFrom=SharerSearchForm()
        return render(request,'Join.html',locals())
    if request.method=="POST":
        SearchForm=SharerSearchForm(request.POST)
        if SearchForm.is_valid():
            global Full_passenger_number
            Full_passenger_number=SearchForm.cleaned_data.get('passenger_number')

            orders=Order.objects.filter(destination=SearchForm.cleaned_data.get('destination')).filter(arrival_time__gte=SearchForm.cleaned_data.get('earliest_time')).filter(arrival_time__lte=SearchForm.cleaned_data.get('latest_time'))\
                    .filter(passenger_number__lte=10-SearchForm.cleaned_data.get('passenger_number')).filter(is_comfirmed=False).filter(is_shared=True).filter().exclude(owner__username=user.username).filter().exclude(driver__username=user.username)

            target=[]

            for temp in orders:
                isAlready = False
                for tempsharer in temp.sharer.all():
                    if tempsharer.username!=user.username:
                        isAlready=True
                        break
                if not isAlready:
                    target.append(temp)

            return render(request,"ShowAvailable.html",locals())




def logout(request):

    request.session.clear()

    return redirect('/')

