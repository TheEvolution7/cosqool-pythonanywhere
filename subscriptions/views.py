from .serializers import SubscriptionSerializer, Subscription
from core.api.views import *
from dashboards.paypalAPI import cancelSubscription
class SubscriptionViewSet(CoreViewSet):  
    queryset = Subscription.objects.all()  
    serializer_class = SubscriptionSerializer
    
class AdminSubscriptionViewSet(AdminCoreViewSet, SubscriptionViewSet):  
    pass


    
class DashboardSubscriptionViewSet(DashboardCoreViewSet, SubscriptionViewSet):
    
    @action(detail=False, methods=['post'])
    def cancel_subscription(self, request, format=None):
        data = request.data

        res = cancelSubscription(data['id'], data['reason'])
        return Response(res)
        