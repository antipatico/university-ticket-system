from django.urls import path
from uts_report import views

app_name = "uts_report"
urlpatterns = [
    path('ticket/<int:pk>', views.generate_ticket_report, name="generate_ticket_report"),
]
