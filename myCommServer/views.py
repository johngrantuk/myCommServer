from django.shortcuts import render, redirect
from .models import UserMsg, MyCommMsg, MyCommDevice
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import binascii
from itertools import chain
from operator import attrgetter
from datetime import datetime
from . import settings
import urllib
from urllib.request import urlopen
from django.contrib.auth import authenticate, login, logout
from ratelimit.decorators import ratelimit


def messages(request):
    """
    Main view that shows message stream of messages sent from MyComm device and to MyComm device by registered users.
    """
    myCommMessages = MyCommMsg.objects.order_by('receivedTime').reverse()                           # Retrieve all messages received from the MyComm device.
    userMessages = UserMsg.objects.order_by('receivedTime').reverse()                               # Retrieve all messages sent by registered users to the MyComm device.
    messages = sorted(chain(myCommMessages, userMessages),key=attrgetter('receivedTime'),reverse=True) # Sorts the messages in reverse date order.
    return render(request, "messages.html", {'messages': messages})                                 # Render main message stream view.

@csrf_exempt
def incomingMessage(request):
    """
    Message received from Iridium via API.
    """
    print("\nINCOMING IRIDIUM MESSAGE\n")

    if request.method == 'POST':                                                    # Confirm it is a POST
        postDict = request.POST
        deviceImei = postDict.get("imei")                                           # Iridium IMEI is used to confirm message is genuine.

        try:
            myCommSender = MyCommDevice.objects.get(imei=deviceImei)                # Check if the IMEI of device is registered. If not return Forbidden
        except MyCommDevice.DoesNotExist:
            print("Incorrect IMEI.")
            return HttpResponse(status=403)

        message = binascii.unhexlify(postDict.get("data"))
        longitude = postDict.get("iridium_longitude")
        latitude = postDict.get("iridium_latitude")
        iridium_cep = postDict.get("iridium_cep")
        transmit_time = postDict.get("transmit_time")

        myCommMsg = MyCommMsg(deviceImei=myCommSender, message=message, destinationId="HackadayFans", longitude=longitude, latitude=latitude, iridium_cep=iridium_cep, transmit_time=transmit_time, receivedTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        myCommMsg.save()                                                            # Save new message in database.

    return HttpResponse(status=200)


@csrf_exempt
@ratelimit(key='user_or_ip', rate='3/d')
def outgoingMessage(request):
    """
    Message to send from web to Iridium via API.
    """
    print("\nOUTGOING IRIDIUM MESSAGE\n")

    was_limited = getattr(request, 'limited', False)

    print(was_limited)
    if was_limited:
        return render(request, "rateLimit.html")                                    # User has sent too many messages.

    if request.method == 'POST':                                                    # Confirm it is a POST
        message = request.POST["message"]                                           # Gets message from POST.
        device = "myCommHackaday"                                                   # For now we only have demo MyComm device.

        print(request.user.username + " Sending message: " + message + " to device: " + device)

        if request.user.is_authenticated():                                         # Only logged in users can send a message.

            try:                                                                    # Check if the IMEI of reveiving device is registered. If not return Forbidden
                myCommDevice = MyCommDevice.objects.get(deviceId=device)
            except MyCommDevice.DoesNotExist:
                print("No Device found.")
                return HttpResponse(status=403)

            #userMessage = UserMsg(user=request.user, message=message, destinationId="myCommHackaday", receivedTime=timezone.now())
            userMessage = UserMsg(user=request.user, message=message, destinationId="myCommHackaday", receivedTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            userMessage.save()                                                      # Save user message in database.

            post_data = [('imei', myCommDevice.imei),('username', settings.rockBlockUsername),('password', settings.rockBlockPassword),('data', binascii.hexlify(str.encode(message)))]     # a sequence of two element tuples
            result = urlopen(settings.iridiumApi, urllib.parse.urlencode(post_data).encode("utf-8")) # Creates a POST request and sends to the Iridium API.
            content = result.read()
            print(content)

    return redirect('/')

@csrf_exempt
def testSendMessage(request):
    """
    Test sending to API. UNUSED.
    """

    if request.method == 'POST':                                                    # Confirm it is a POST
        print("Spoof Iridium API: ")
        print(request.POST["imei"])
        print(request.POST["username"])
        print(request.POST["password"])
        print(request.POST["data"])
        return HttpResponse(status=200)

    return HttpResponse(status=403)

def loginUser(request):
    """
    Login user to send messages, etc.
    """

    if request.method == 'POST':                                                    # Confirm it is a POST
        print("Login:")
        username = request.POST["user"]
        password = request.POST["pass"]
        user = authenticate(username=username, password=password)                   # Authenticates user using Django.

        if user is not None:                                                        # The password verified for the user
            if user.is_active:
                login(request, user)                                                # Logs user in.
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

        return redirect('/')
    else:
        return redirect('/')

def logoutUser(request):
    """
    Logout user.
    """
    logout(request)
    return redirect('/')

def registerUser(request):
    """
    Register a new user.
    """
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    user = User.objects.create_user(username, email, password)                          # Creates new users using Django.
    user.save()                                                                         # Save new user to database.

    user = authenticate(username=username, password=password)                           # Logs user in so they can send messages, etc.
    if user is not None:                                                                # the password verified for the user
        if user.is_active:
            login(request, user)
            print("User is valid, active and authenticated")
        else:
            print("The password is valid, but the account has been disabled!")
    else:                                                                               # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")
    return redirect('/')

def location(request):
    """
    Shows location on Google Maps.
    """
    lat = request.GET['lat']
    lng = request.GET['lng']
    text = request.GET['text']
    print("Lat: " + lat)

    return render(request, "location.html", {'lat': lat, 'lng':lng, 'text':text, 'API_KEY':settings.GOOGLE_API_KEY})
