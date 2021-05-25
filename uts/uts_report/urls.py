from django.urls import path
from uts_report import views

app_name = "uts_report"
urlpatterns = [
    path('ticket/<int:pk>', views.generate_ticket_report, name="generate_ticket_report"),
    path('closed', views.generate_closed_tickets_report, name="generate_closed_tickets_report"),
    path('opened/lastyear', views.generate_opened_lastyear_tickets_report, name="generate_opened_lastyear_tickets_report"),
    path('opened/lastyear/stillopen', views.generate_opened_lastyear_stillopen_tickets_report, name="generate_opened_lastyear_stillopen_tickets_report"),
]
