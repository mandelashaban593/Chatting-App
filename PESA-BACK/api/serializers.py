'''
serializers for API
'''
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


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

class TransactionStatusSerializer(serializers.HyperlinkedModelSerializer):
    transaction_id = serializers.CharField()
    #transaction_type = serializers.CharField()

    def validate(self,attrs):
        transaction_id = attrs.get('transaction_id')

        #transaction_type = attrs.get('transaction_type')

        if not transaction_id:
            msg = _('You Must include "transaction_id"')
            raise
            serializers.ValidationError(msg)

        return attrs
