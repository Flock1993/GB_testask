from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers


class WriteSensorValuesView(GenericAPIView):
    serializer_class = serializers.WriteSensorValuesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data)
        return Response()
