from django.urls import path

from api.views import *


urlpatterns = [
    path("openChannel", OpenChannelView.as_view()),
    path("closeChannel", CloseChannelView.as_view()),
]
