from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'recentactivities', views.RecentActivitiesView, basename="RecentActivity")
router.register(r'tickets', views.TicketsView, basename="Ticket")
router.register(r'organizations', views.OrganizationsView, basename="Organizations")
app_name = "uts_rest"
urlpatterns = [
        path('', include(router.urls), name='router'),
]
