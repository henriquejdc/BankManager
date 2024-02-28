# Django imports
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema

# Third party imports
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Project imports
from manager.models import Transaction
from manager.serializers import AccountSerializer, TransactionSerializer
from manager.services import create_transaction
from shared.views import BaseCollectionViewSet
from shared.http.responses import (
    api_exception_response,
)


class TransactionViewSet(BaseCollectionViewSet):
    """ A ViewSet for transaction. """
    model_class = Transaction
    queryset = model_class.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ('post',)
    search_fields = ('name',)
    serializers = {
        'default': serializer_class,
    }
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Create object")
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            created, account = create_transaction(
                serializer.validated_data
            )

            if created:
                headers = self.get_success_headers(serializer.data)
                return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED, headers=headers)

            return Response('Saldo insuficiente', status=status.HTTP_404_NOT_FOUND)

        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)
        except IntegrityError as validation_exception:
            return api_exception_response(
                exception=validation_exception,
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exception:
            return api_exception_response(exception=exception)
