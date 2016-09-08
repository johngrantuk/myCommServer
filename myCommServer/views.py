from django.shortcuts import render
from .models import UserMsg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import binascii


def messages(request):
    messages = UserMsg.objects.order_by('receivedDate')
    return render(request, "messages.html", {'messages': messages})

@csrf_exempt
def incomingMessage(request):
    print("\nINCOMINGMESSAGE\n")
    if request.method == 'POST':
        u = User.objects.get(username='scotsat')
        postDict = request.POST
        data = binascii.unhexlify(postDict.get("data"))
        userMessage = UserMsg(user=u, message=data, destinationId="jack", receivedDate=timezone.now())
        userMessage.save()

    return HttpResponse(status=200)
