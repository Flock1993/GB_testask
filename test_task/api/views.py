from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers


class WriteSensorValuesView(GenericAPIView):
    serializer_class = serializers.WriteSensorValuesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        difference = serializer.save()
        data = {
            "status": "Success",
            "desc": ""
        }
        if difference:
            data["desc"] = (
                f"Data for the following sensors was not inserted: {difference}."
                "Reason: mentioned sensors are not in the system.")
        return Response(status=status.HTTP_200_OK, data=data)
