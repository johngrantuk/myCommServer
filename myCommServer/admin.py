from django.contrib import admin
from .models import UserMsg, MyCommDevice, MyCommMsg

admin.site.register(UserMsg)
admin.site.register(MyCommDevice)
admin.site.register(MyCommMsg)
