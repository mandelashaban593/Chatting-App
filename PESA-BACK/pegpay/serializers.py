from rest_framework import serializers
from accounts.models import UserProfile
from models import WaterTransaction,ElectricityTransaction
from django.contrib.auth.models import User


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    #user_data = serializers.RelatedField(source='user')

    class Meta:
        model = User
        fields = (
            'email',
        )

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    #serialize user object
    user = UserInfoSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user','firstname','lastname'
        )

class WaterTransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WaterTransaction
        fields = (
            'customer_ref',
            'customer_name',
            'customer_phone',
            'paid_by',
            'amount',
            'sender_message',
            'company_code',
            'area',
        )

class ElectricityTransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ElectricityTransaction
        fields = (
            #
            'customer_type',
            'payment_type',
            'sender_message',
            'customer_ref',
            'customer_name',
            'customer_phone',
            'paid_by','amount',
            'customer_email',
            'company_code'
        )
