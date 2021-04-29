import uuid

from django.http import JsonResponse

from api.models import Channel
from bbb_common_api.views import PostApiPoint


class CloseChannelView(PostApiPoint):

    endpoint = "closeChannel"
    required_parameters = ["meeting_id"]

    def safe_post(self, request, parameters, *args, **kwargs):
        try:
            channel = Channel.objects.get(meeting_id=parameters["meeting_id"])
            channel.delete()
        except Channel.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Channel does not exist"}, status=400
            )
        return JsonResponse({"success": True, "message": "Channel was deleted"})


class OpenChannelView(PostApiPoint):

    endpoint = "openChannel"
    required_parameters = ["meeting_id"]

    def safe_post(self, request, parameters, *args, **kwargs):
        channel, created = Channel.objects.get_or_create(meeting_id=parameters["meeting_id"])
        if not created:
            return JsonResponse(
                {"success": False, "message": "Channel already exists"}, status=304
            )
        channel.streaming_key = str(uuid.uuid4())
        channel.save()

        return JsonResponse(
            {"success": True, "message": "New Channel was created", "content": {"streaming_key": channel.streaming_key}}
        )
