from django.conf.urls import url
from .views import *

urlpatterns = [
               url('v1/initiate_request/', InitiateRequestView.as_view(), name='initiate request'),
               ]
