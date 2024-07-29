from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import caches
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.contrib.auth.models import Group, User
from django.db.models import Q

from rest_framework import generics, filters, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from alertservice.models import Alert
from alertservice.serializers import UserSerializer, AlertSerializer

from django_redis import get_redis_connection
import redis

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Alert.objects.filter(created_by=user)
        status_query = self.request.query_params.get('status', None)
        if status_query is not None:
            queryset = queryset.filter(status=status_query)
        symbol_query = self.request.query_params.get('symbol', None)
        if symbol_query is not None:
            queryset = queryset.filter(symbol=symbol_query)
        return queryset

    def perform_create(self, serializer):
        # price_cache = caches["default"]
        con = get_redis_connection("default")
        price_dict = con.hgetall(':1:binance_data')
        if price_dict:
            price_dict = {k.decode('utf-8'): v.decode('utf-8') for k, v in price_dict.items()}
        else:
            price_dict = {}
        symbol = serializer.validated_data['symbol']
        price = price_dict[symbol]
        serializer.save(created_by=self.request.user,set_price=price)

    @action(detail=False, methods=['post'], url_path='create')
    def create_alert(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['delete'], url_path='delete/<int:alert_pk>')
    def delete_alert(self, request, alert_pk):
        try:
            alert = Alert.objects.get(id=alert_pk)
            alert.status = 'Cancelled'
            alert.save()
            return Response({'status': 'Alert cancelled'}, status=200)
        except Alert.DoesNotExist:
            return Response({'status': 'Alert not found'}, status=404)