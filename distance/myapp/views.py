import random

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import math
from myapp.models import booking, Profile
from myapp.mixins import MessaHandler




def calculate_distance(source, destination):
    # Initialize Google Maps API client
    gmaps = googlemaps.Client(key='AIzaSyAX0OjsvGZFaLvdaYyOvaWvRmSpnEqVNIo')

    # Make API request to calculate distance
    response = gmaps.distance_matrix(source, destination, mode='driving')

    # Extract distance value from response
    distance = response['rows'][0]['elements'][0]['distance']['value']

    # Convert distance from meters to kilometers
    distance_km = distance / 1000

    return distance_km


def INDEX(request):
   return render(request, 'index.html')


def calculate_fare(request):
    places = ['Mumbai, Maharashtra, India',
                   'Silvassa, Dadra and Nagar Haveli and Daman and Diu, India',
                   'Vapi, Gujarat, India', 'Valsad, Gujarat, India',
                   'Navsari, Gujarat, India',
                   'Surat, Gujarat, India',
                   'Bharuch, Gujarat, India',
                   'Ankleshwar, Gujarat, India',
                   'Vadodara, Gujarat, India',
                   'Udaipur, Rajasthan, India']

    if request.method == 'POST' :
        source = request.POST.getlist ( 'source' )  # Get the source as a string, not a list
        destination = request.POST.getlist ( 'destination' )  # Get the destination as a string, not a list
        date = request.POST.getlist ( 'date' )
        time = request.POST.getlist ( 'time' )
        per_km_price = 10  # Change this value according to your requirement

        distance = calculate_distance ( source , destination )
        toll_tax = distance

        base_fare = distance * per_km_price + toll_tax

        if any ( place in source for place in places ) and any ( place in destination for place in places ) :
            base_fare = base_fare  # Base fare when both source and destination are in the array
        elif any ( place in source for place in places ) or any ( place in destination for place in places ) :
            base_fare += 1500  # Base fare + additional fare when either source or destination is in the array
        else :
            base_fare += 3000  # Base fare + additional fare when neither source nor destination is in the array

        gst = base_fare * 0.05  # Add 5% GST amount

        total_fare = base_fare + gst  # Add 5% GST amount

        fare = total_fare * 0.15
        dis_fare = fare + total_fare

        distance = round ( distance )
        total_fare = math.ceil ( total_fare )
        gst = math.ceil ( gst )
        base_fare = math.ceil ( base_fare )
        dis_fare = math.ceil ( dis_fare )

        context = {
            'source' : source ,
            'destination' : destination ,
            'distance' : distance ,
            'total_fare' : total_fare ,
            'date' : date ,
            'time' : time ,
            'gst' : gst ,
            'base_fare' : base_fare ,
            'dis_fare' : dis_fare
        }

        request.session [ 'source' ] = source
        request.session [ 'destination' ] = destination
        request.session [ 'distance' ] = distance
        request.session [ 'total_fare' ] = total_fare
        request.session [ 'date' ] = date
        request.session [ 'time' ] = time
        request.session [ 'gst' ] = gst
        request.session [ 'base_fare' ] = base_fare
        request.session [ 'dis_fare' ] = dis_fare

        return redirect ( 'cab_list' )

    return redirect ( 'index' )


def CAB(request):
    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    total_fare = request.session.get('total_fare')
    date = request.session.get('date')
    time = request.session.get('time')
    gst = request.session.get('gst')
    base_fare = request.session.get('base_fare')
    dis_fare = request.session.get('dis_fare')

    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare': total_fare,
        'date': date,
        'time': time,
        'gst': gst,
        'base_fare': base_fare,
        'dis_fare': dis_fare
    }

    return render(request, 'cab-list.html',context)



def CAB_DETAIL(request):
    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    total_fare = request.session.get('total_fare')
    date = request.session.get('date')
    time = request.session.get('time')
    gst = request.session.get('gst')
    base_fare = request.session.get('base_fare')


    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare': total_fare,
        'date': date,
        'time': time,
        'gst': gst,
        'base_fare': base_fare
    }

    return render(request, 'cab-detail.html',context)


def CAB_BOOKING(request):
    if request.method == "POST":
        pickup_address = request.POST.get('pickup_address')
        drop_address = request.POST.get('drop_address')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        altmobile = request.POST.get('altmobile')
        gst = request.POST.get('gst')

        pickup_city = request.POST.get('pickup_city')
        drop_city = request.POST.get('drop_city')
        selected_option = request.POST.get('discountOptions')

        en = booking(name=name, email=email, pickup_city=pickup_city, drop_city=drop_city, mobile=mobile, gst=gst, pickup_address=pickup_address, drop_address=drop_address, altmobile=altmobile)
        en.save()




    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    total_fare = request.session.get('total_fare')
    date = request.session.get('date')
    time = request.session.get('time')


    total_payment = total_fare
    payment_amount = 0

    if selected_option == 'option1':
        payment_amount = total_payment * 0.2
    elif selected_option == 'option2':
        payment_amount = total_payment
    else:
        payment_amount = 0

    payment_amount = math.ceil(payment_amount)


    rem_amount = total_payment - payment_amount

    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare': total_fare,
        'date': date,
        'time': time,
        'name': name,
        'mobile': mobile,
        'email': email,
        'pickup_address': pickup_address,
        'drop_address': drop_address,
        'payment_amount': payment_amount,
        'rem_amount': rem_amount
    }

    return render(request, 'cab-booking.html', context)


def CONFIRM(request):
   return render(request, 'confirm.html')



def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        user = User.objects.create(username=username)
        profile = Profile.objects.create(user = user, phone_number=phone_number)

        return redirect('login')
    return render(request, 'register.html')



def LOGIN(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        profile = Profile.objects.filter(phone_number = phone_number)
        if not profile.exists():
            return redirect('register')

        profile[0].otp = random.randint(1000, 9999)
        profile[0].save()
        message_handler = MessaHandler(phone_number, profile[0].otp).send_otp_on_phone()

        return redirect(f'/otp/{profile[0].uid}', message_handler)


    return render(request, 'login.html')



def PASSWORD(request):
   return render(request, 'forgot-password.html')


def PROFILE(request):
   return render(request, 'profile.html')




def otp(request, uid):
    return render(request, 'otp.html')














