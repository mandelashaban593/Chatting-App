from rest_framework import serializers
from mtn.models import MtnTransaction
from django.utils.translation import ugettext_lazy as _


class MtnTransactionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MtnTransaction
        fields = (
        'amount', 'phonenumber',
        )
        #read_only_fields = ('uid',)


class TransactionStatusSerializer(serializers.Serializer):
    amount = serializers.CharField()
    phonenumber = serializers.CharField()

    def validate(self, attrs):
        amount = attrs.get('amount')
        phonenumber = attrs.get('phonenumber')

        if amount and phonenumber:
            '''proceed with the translation'''
            balance = 0
            if amount > balance:
                msg = _(
                    'Account balance is too low, you neeed a minimum of %s.'
                % balance
                )
                raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "amount" and "phonenumber".')
        raise serializers.ValidationError(msg)
        return attrs

class WithdrawMoneySerializer(serializers.Serializer):
    amount = serializers.CharField()
    phonenumber = serializers.CharField()

    def validate(self, attrs):
        amount = attrs.get('amount')
        phonenumber = attrs.get('phonenumber')

        if amount and phonenumber:
        	'''proceed with the translation'''
    		balance = 0
    		if amount > balance:
    			msg = _(
                    'Account balance is too low, you neeed a minimum of %s.'
    			% balance
    			)
    			raise serializers.ValidationError(msg)
    		else:
    			msg = _('Unable to log in with provided credentials.')
    			raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "amount" and "phonenumber".')
        raise serializers.ValidationError(msg)
        return attrs


class DepositMoneySerializer(serializers.Serializer):
    amount = serializers.CharField()
    phonenumber = serializers.CharField()

    def validate(self, attrs):
        amount = attrs.get('amount')
        phonenumber = attrs.get('phonenumber')
        if not phonenumber or not amount:
            msg = _('You Must include "amount" and "phonenumber".')
            raise serializers.ValidationError(msg)
        """"
        if amount and phonenumber:
            '''proceed with the translation'''
            balance = 0
            if amount > balance:
                msg = _(
                    'Account balance is too low, you neeed a minimum of %s.'
                % balance
                )
                raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "amount" and "phonenumber".')
            raise serializers.ValidationError(msg)
        """
        return attrs
