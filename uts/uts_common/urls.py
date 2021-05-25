from django.urls import path
from uts_common import views

app_name = "uts_common"
urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.new_ticket_form, name="new_ticket"),
    path('settings', views.profile_settings_form, name="profile_settings"),
    path('organizations', views.organizations_list, name="organizations_list"),
    path('ticket/<int:pk>', views.ticket_details, name="ticket_details"),
    path('ticket/<int:pk>/report', views.generate_ticket_report, name="generate_ticket_report"),
    path('s3cr3tl0g1n', views.local_login, name="local_login"),
    path('logout', views.logout, name="logout")
]
