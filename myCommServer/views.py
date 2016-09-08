from django.shortcuts import render, redirect
from .models import UserMsg, MyCommMsg, MyCommDevice
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import binascii
from itertools import chain
from operator import attrgetter


def messages(request):
    myCommMessages = MyCommMsg.objects.order_by('receivedTime').reverse()
    userMessages = UserMsg.objects.order_by('receivedTime').reverse()
    messages = sorted(chain(myCommMessages, userMessages),key=attrgetter('receivedTime'),reverse=True)
    return render(request, "messages.html", {'messages': messages})

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

        myCommMsg = MyCommMsg(deviceImei=myCommSender, message=message, destinationId="HackadayFans", longitude=longitude, latitude=latitude, iridium_cep=iridium_cep, transmit_time=transmit_time)
        myCommMsg.save()                                                            # Save new message in database.

    return HttpResponse(status=200)


@csrf_exempt
def outgoingMessage(request):
    """
    Message to send from web to Iridium via API.
    """
    print("\nOUTGOING IRIDIUM MESSAGE\n")

    if request.method == 'POST':                                                    # Confirm it is a POST
        print(request.POST)
        message = request.POST["message"]
        if request.user.is_authenticated():
            print("Sending message")
            print(message)
            print(request.user.username)
            userMessage = UserMsg(user=request.user, message=message, destinationId="myCommHackaday", receivedTime=timezone.now())
            userMessage.save()

        """
        u = User.objects.get(username='scotsat')
        postDict = request.POST
        data = binascii.unhexlify(postDict.get("data"))
        userMessage = UserMsg(user=u, message=data, destinationId="myCommHackaday", receivedDate=timezone.now())
        userMessage.save()
        """

    return redirect('/')
