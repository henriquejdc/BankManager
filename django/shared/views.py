# Django imports
import django_filters.rest_framework
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http.response import Http404
from drf_yasg.utils import swagger_auto_schema

# Third party imports
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

# Project imports
from shared.helpers import (
    DefaultPaginationClass,
)
from shared.http.responses import (
    api_exception_response,
    not_found_response
)


class BaseCollectionViewSet(viewsets.ModelViewSet):
    """ Base ModelViewSet class. """
    model_class = None
    protected_error_message = None
    pagination_class = DefaultPaginationClass
    serializer_class = None
    serializers = None
    open_actions = []
    http_method_names = (
        'options',
        'get',
        'post',
        'put',
        'patch',
        'delete',
    )
    ignore_paginator_actions = []
    ignore_ordering_actions = []
    ignore_search_filter_actions = []
    ignore_viewset_filters_actions = []

    @property
    def paginator(self):
        paginator = super().paginator
        if self.action in self.ignore_paginator_actions:
            paginator = None
        return paginator

    @property
    def filter_backends(self):
        filter_backends = [
            OrderingFilter,
            SearchFilter,
            django_filters.rest_framework.DjangoFilterBackend,
        ]
        search_filter_index = 1
        viewset_filters_index = 2
        if self.action in self.ignore_ordering_actions:
            filter_backends.pop(0)
            search_filter_index = 0
            viewset_filters_index = 1
        if self.action in self.ignore_search_filter_actions:
            filter_backends.pop(search_filter_index)
            viewset_filters_index = 0
        if self.action in self.ignore_viewset_filters_actions:
            filter_backends.pop(viewset_filters_index)
        return filter_backends

    def get_serializer_class(self):
        return self.serializers.get(
            self.action,
            self.serializers['default']
        )

    def get_permissions(self):
        if self.action in self.open_actions:
            self.permission_classes = [permissions.AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            if getattr(self, 'swagger_fake_view', False):
                return self.model_class.objects.none()  # pragma: no cover

        except FieldDoesNotExist:
            pass
        return queryset.distinct()

    @swagger_auto_schema(operation_summary="List objects")
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Retrieve a object")
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404 as exception:
            return not_found_response(exception)
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Create object")
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)
        except IntegrityError as validation_exception:
            return api_exception_response(
                exception=validation_exception,
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Update object")
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Http404 as exception:
            return not_found_response(exception)
        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)
        except IntegrityError as validation_exception:
            return api_exception_response(
                exception=validation_exception,
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Partial update object")
    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Http404 as exception:
            return not_found_response(exception)
        except RestFrameworkValidationError as validation_exception:
            return api_exception_response(exception=validation_exception)
        except Exception as exception:
            return api_exception_response(exception=exception)

    @swagger_auto_schema(operation_summary="Delete object")
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404 as exception:
            return not_found_response(exception)
        except ProtectedError as exception:
            return api_exception_response(
                exception=exception,
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exception:
            return api_exception_response(exception=exception)
