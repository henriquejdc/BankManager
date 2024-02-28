# Django imports
import django_filters.rest_framework
from drf_yasg.utils import swagger_auto_schema

# Third party imports
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.filters import AccountFilter
from manager.models import Account
from manager.serializers import AccountSerializer, AccountCreateSerializer
from shared.views import BaseCollectionViewSet
from shared.http.responses import (
    api_exception_response
)


class AccountViewSet(BaseCollectionViewSet):
    """ A ViewSet for account. """
    model_class = Account
    queryset = model_class.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ('get', 'post')
    search_fields = ('name',)
    serializers = {
        'default': serializer_class,
        'create': AccountCreateSerializer,
    }
    permission_classes = [IsAuthenticated]
    filterset_class = AccountFilter
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
    )

    @swagger_auto_schema(operation_summary="Create object")
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if Account.objects.filter(id=serializer.validated_data.get('conta_id')):
                return Response({'conta_id': 'Conta já existente!'}, status=status.HTTP_400_BAD_REQUEST)

            account = Account.objects.create(
                id=serializer.validated_data.get('conta_id'),
                balance=serializer.validated_data.get('valor')
            )
            headers = self.get_success_headers(serializer.data)
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED, headers=headers)

        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)

    @swagger_auto_schema(operation_summary="List objects")
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        if request.GET.get('conta_id') or request.GET.get('id'):
            return Response(response_data[0] if len(response_data) else {})

        return Response(response_data)
