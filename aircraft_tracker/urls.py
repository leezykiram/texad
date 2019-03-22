"""aircraft_tracker URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns


import django.contrib.auth.views as django_views
import light_jets.views as light_jets_views

router = routers.DefaultRouter()
router.register(r'jets', light_jets_views.ProductViewSet)
router.register(r'tracking', light_jets_views.TrackingViewSet)

admin.autodiscover()

schema_view = get_schema_view(title='Aircraft API tracking')

urlpatterns = [
    url(r'api/v1/', include(router.urls)),
    url(r'^$', light_jets_views.tracking,name='home'),
    url(r'^jets/', light_jets_views.jets,name='jets'),
    url(r'^tracking/', light_jets_views.tracking,name='tracking'),
    url(r'^upload/', light_jets_views.upload,name='upload'),
    url(r'^maps/', light_jets_views.maps,name='maps'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth-api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'schema/', schema_view), # core-api yaml schema
]
