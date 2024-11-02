from rest_framework.views import APIView
from rest_framework.response import Response
from event.constants.constants_event import REGIONS

class RegionListView(APIView):
    def get(self, request):
        return Response([{"value": code, "label": name} for code, name in REGIONS])
    