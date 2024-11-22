from django.shortcuts import render,  redirect
from .forms import CreateUserForm, LoginForm,Hotel_Booking_Form, Zoo_Booking_Form

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


from .models import HotelBooking, ZooBooking

def home(request):
    return render(request, 'website/index.html')

# register a user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form  = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, "Account created successfully!")
            return redirect('my-login')
    
    context = {'form':form}

    return render(request,'website/register.html', context=context)


# login a user

def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('')

    context = {'login_form':form}
    return render(request,'website/my-login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect("website/my-login")

@login_required(login_url='my-login')
def hotel(request):
    
    form = Hotel_Booking_Form()

    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'hotel_user_id_id': request.user})
      
        form  = Hotel_Booking_Form(updated_request)


        if form.is_valid():
            obj = form.save(commit=False) # Return an object without saving to the DB

            # Calculate the number of days
            arrive = obj.hotel_booking_date_arrive
            depart = obj.hotel_booking_date_leave
            result = depart - arrive
            print ("Number of days: ", result.days)


            hotel_total_cost = int(obj.hotel_booking_adults) * 65 \
                                    + int(obj.hotel_booking_children) * 35 \
                                    + int(obj.hotel_booking_oap) * 40
            
            hotel_total_cost *= int(result.days)
            
            hotel_points = int(hotel_total_cost / 20)
            print("Hotel Points: ", hotel_points)
            print("printing booking costs: ", hotel_total_cost)


            #set the values in the data
            obj.hotel_points = hotel_points
            obj.hotel_total_cost = hotel_total_cost
            obj.hotel_user_id = request.user # Add the hotel_user_id field with the user object

            obj.save() # Save to database
            
            messages.success(request, "Hotel booked successfully!")
            return redirect('')
        else:
            print("there was a problem with the form")
            return redirect('hotel')

    
    context = {'form': form}

    return render(request, 'website/hotel.html', context=context)


def education(request):
    return render(request, 'website/education.html')

def test(request):
    return render(request,'website/test.html')

@login_required(login_url='my-login')
def dashboard(request):

    if request.method == "POST":
        icon = request.POST['icon']
        request.user.updateIcon(icon)


    # get the bookings made by the loged in user
    my_hotel_bookings = HotelBooking.objects.filter(hotel_user_id = request.user.id)
    my_zoo_bookings = ZooBooking.objects.filter(zoo_user_id = request.user.id)
    context = {'hotel_records': my_hotel_bookings,
               'zoo_records': my_zoo_bookings,}

    return render(request, 'website/dashboard.html',context=context )


@login_required(login_url='my-login')
def zoo(request):
    
    form = Zoo_Booking_Form()

    if request.method == "POST":
      
        updated_request = request.POST.copy()
        updated_request.update({'zoo_user_id_id': request.user})
      
        form  = Zoo_Booking_Form(updated_request)


        if form.is_valid():
            obj = form.save(commit=False) # Return an object without saving to the DB

            # Calculate the number of days
            arrive = obj.zoo_booking_date_arrive
            depart = obj.zoo_booking_date_leave
            result = depart - arrive
            print ("Number of days: ", result.days)
            #note the days have not been validated yet
            #option for single day bookings may be better
            #if arrive date and end date are the same days = 0

            #work out the cost
            zoo_total_cost = int(obj.zoo_booking_adults) * 12 \
                                    + int(obj.zoo_booking_children) * 8 \
                                    + int(obj.zoo_booking_oap) * 9
            zoo_total_cost *= int(result.days)
                       
            #has the user requested to pay with points ?
            #suplimenting their payment 
            checkbox_points =  request.POST.get("use_points")
            saving = 0
            if checkbox_points == "yes":
                saving = request.user.spendPoints(zoo_total_cost)

            #get additional points and add them to the user
            zoo_points = int(zoo_total_cost / 20)
            request.user.addPoints(zoo_points)

            #set the values in the data
            obj.zoo_points = zoo_points
            obj.zoo_total_cost = zoo_total_cost
            obj.zoo_user_id = request.user # Add the hotel_user_id field with the user object

            

            obj.save() # Save to database
            
            messages.success(request, "Zoo booked successfully! Saveing £" + str(saving))
            return redirect('')
        else:
            print("there was a problem with the form")
            return redirect('zoo')

    
    context = {'form': form}

    return render(request, 'website/zoo.html', context=context)