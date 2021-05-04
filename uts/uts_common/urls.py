from django.urls import path
from . import views

app_name = "uts_common"
urlpatterns = [
    path('', views.index, name="index"),
    path('ticket/<int:pk>', views.ticket_details, name="ticket_details"),
    path('s3cr3tl0g1n', views.local_login, name="local_login"),
    path('logout', views.logout, name="logout")
]
