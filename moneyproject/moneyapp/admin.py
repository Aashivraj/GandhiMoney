from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(PaymentType)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Balance)
admin.site.register(Credit)