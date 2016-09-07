from django.shortcuts import render
from .models import UserMsg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def messages(request):
    messages = UserMsg.objects.order_by('receivedDate')
    return render(request, "messages.html", {'messages': messages})

@csrf_exempt
def incomingMessage(request):
    print("\nINCOMINGMESSAGE\n")
    if request.method == 'POST':
        print("\nPOST:\n")
        print(request.POST)
        print("\nBody:\n")
        print(request.body)
        print("\nParams:\n")
        print(request.content_params)

    return HttpResponse(status=200)
