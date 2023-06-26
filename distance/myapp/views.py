from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import math
from myapp.models import booking




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
   city_array = ['Mumbai, Maharashtra, India', 'Silvassa, Dadra and Nagar Haveli and Daman and Diu, India',
              'Vapi, Gujarat, India', 'Valsad, Gujarat, India',
              'Navsari, Gujarat, India',
              'Surat, Gujarat, India',
              'Bharuch, Gujarat, India',
              'Ankleshwar, Gujarat, India',
              'Vadodara, Gujarat, India',
              'Anand, Gujarat, India',
              'Nadiad, Gujarat, India',
              'Ahmedabad, Gujarat, India',
              'Gandhinagar, Gujarat, India',
              'Udaipur, Rajasthan, India',
              'Chittorgarh, Rajasthan, India',
              'Ajmer, Rajasthan, India',
              'Jaipur, Rajasthan, India',
              'Gurgaon, Haryana, India',
              'Delhi, India']

   if request.method == 'POST':
       source = request.POST.get('source')
       destination = request.POST.get('destination')
       date = request.POST.get('date')
       time = request.POST.get('time')
       per_km_price = 10  # Change this value according to your requirement

       distance = calculate_distance(source, destination)
       toll_tax = distance

       base_fare = distance * per_km_price + toll_tax

       if source in city_array and destination in city_array:
          base_fare = base_fare  # Base fare when both source and destination are in the array
       elif source in city_array or destination in city_array:
          base_fare += 1500  # Base fare + additional fare when either source or destination is in the array
       else:
          base_fare += 3000  # Base fare + additional fare when neither source nor destination is in the array



       gst = base_fare * 0.05  # Add 5% GST amount

       total_fare = base_fare + gst # Add 5% GST amount

       fare = total_fare * 0.15
       dis_fare = fare + total_fare




       distance = round(distance)
       total_fare = math.ceil(total_fare)
       gst = math.ceil(gst)
       base_fare = math.ceil(base_fare)
       dis_fare = math.ceil(dis_fare)

       context = {
          'source': source,
          'destination': destination,
          'distance': distance,
          'total_fare': total_fare,
          'date': date,
          'time': time,
          'gst': gst,
          'base_fare': base_fare,
           'dis_fare':dis_fare
       }


       request.session['source'] = source
       request.session['destination'] = destination
       request.session['distance'] = distance
       request.session['total_fare'] = total_fare
       request.session['date'] = date
       request.session['time'] = time
       request.session['gst'] = gst
       request.session['base_fare'] = base_fare
       request.session['dis_fare'] = dis_fare

       return redirect('cab_list')

   return redirect('index')


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


    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare': total_fare,
        'date': date,
        'time': time,
        'gst': gst
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
        remark = request.POST.get('remark')
        pickup_city = request.POST.get('pickup_city')
        drop_city = request.POST.get('drop_city')

        en = booking(name=name, email=email, pickup_city=pickup_city, drop_city=drop_city, mobile=mobile, gst=gst, pickup_address=pickup_address, drop_address=drop_address, altmobile=altmobile, remark=remark)
        en.save()



    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    total_fare = request.session.get('total_fare')
    date = request.session.get('date')
    time = request.session.get('time')

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
        'drop_address': drop_address
    }

    return render(request, 'cab-booking.html', context)


def CONFIRM(request):
   return render(request, 'confirm.html')










