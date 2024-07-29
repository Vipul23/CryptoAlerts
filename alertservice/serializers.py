from rest_framework import serializers

from django.contrib.auth.models import User
from alertservice.models import Alert

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'name', 'symbol', 'price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'status', 'set_price']