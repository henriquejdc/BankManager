from rest_framework.routers import SimpleRouter

from manager.views.transaction import TransactionViewSet
from manager.views.account import AccountViewSet


router = SimpleRouter()
router.register(r'transacao', TransactionViewSet, basename='transaction')
router.register(r'conta', AccountViewSet, basename='account')
urlpatterns = router.urls
