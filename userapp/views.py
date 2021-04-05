from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserModelSerializerReadOnly, UserModelSerializerWriteOnly
from rest_framework.viewsets import ModelViewSet
from .models import User


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializerReadOnly

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UserModelSerializerReadOnly
        return UserModelSerializerWriteOnly

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
