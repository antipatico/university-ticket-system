from django.contrib import admin
from .models import *


admin.site.register(Ticket)
admin.site.register(Tag)
admin.site.register(TicketEvent)
admin.site.register(TicketEventAttachment)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Individual)
admin.site.register(Organization)
