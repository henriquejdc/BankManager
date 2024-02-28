# Base imports
import django_filters.rest_framework

# Project imports
from manager.models import Account


class AccountFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(
        field_name='id',
        lookup_expr='exact'
    )
    conta_id = django_filters.NumberFilter(
        field_name='id',
        lookup_expr='exact'
    )

    class Meta:
        model = Account
        fields = []
