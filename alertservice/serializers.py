from rest_framework import serializers

from django.contrib.auth.models import User
from alertservice.models import Alert

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'name', 'symbol', 'price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'status', 'set_price']