from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from api.models import Channel

HttpResponseRedirect.allowed_schemes.append("rtmp")


class Validate(View):
    def post(self, request, *args, **kwargs):
        if "name" not in request.POST:
            return HttpResponse("Bad Request", status=400)
        try:
            channel = Channel.objects.get(streaming_key=request.POST["name"])
        except Channel.DoesNotExist:
            return HttpResponse("Not valid", status=404)
        return HttpResponseRedirect(f"rtmp://127.0.0.1/redirect/{channel.meeting_id}", status=302)
