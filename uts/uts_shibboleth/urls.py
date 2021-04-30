from django.urls import path
from . import views

app_name = "uts_shibboleth"
urlpatterns = [
    path('login/', views.shibboleth_login, name="login"),
#    path('test/', views.shibboleth_test, name="test")
]
