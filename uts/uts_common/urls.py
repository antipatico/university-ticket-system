from django.urls import path
from . import views

app_name = "uts_common"
urlpatterns = [
    path('', views.index, name="index")
]
