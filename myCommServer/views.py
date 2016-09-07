from django.shortcuts import render
from .models import UserMsg

def messages(request):
    messages = UserMsg.objects.order_by('receivedDate')
    return render(request, "messages.html", {'messages': messages})
