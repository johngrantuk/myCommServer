from django.shortcuts import render
from .models import UserMsg, MyCommMsg, MyCommDevice
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import binascii


def messages(request):
    messages = MyCommMsg.objects.order_by('receivedTime').reverse()
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
    Message received from Iridium via API.
    """
    print("\nINCOMING IRIDIUM MESSAGE\n")

    if request.method == 'POST':                                                    # Confirm it is a POST
        u = User.objects.get(username='scotsat')
        postDict = request.POST
        data = binascii.unhexlify(postDict.get("data"))
        userMessage = UserMsg(user=u, message=data, destinationId="jack", receivedDate=timezone.now())
        userMessage.save()

    return HttpResponse(status=200)
