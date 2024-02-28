# Third party imports
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Project imports
from shared.helpers import DefaultPaginationClass
from . import serializers


class HealthAuthView(generics.GenericAPIView):
    serializer_class = serializers.HealthSerializer
    pagination_class = DefaultPaginationClass

    @swagger_auto_schema(operation_summary="API Health")
    def get(self, request):
        return Response(
            data={"message": "API Health OK"},
            status=status.HTTP_200_OK
        )


class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a User")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
