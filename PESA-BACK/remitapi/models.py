'''remitapi models'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from remitapi.status import TRANSACTION
from django.core.exceptions import ValidationError


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class App(models.Model):
    '''
    model for Apps
    '''
    added = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=10)
    status = models.IntegerField(default=0)
    owner = models.ForeignKey(User)

    @property
    def transactionid(self):
        '''
        Transaction id hashed
        '''

        """
        int(name) ^  0xABCDEFAB
        """
        response1 = int(self.pk) ^ 0xABCDEFAB
        print 'formated id: ',str(response1)
        #return str(self.pk ^ 0xABCDEFAB)
        return response1

    def save(self, *args, **kwargs):
        '''Auto Save API Transaction'''
        if not self.pk:
            print '::Not Self.pk'
            super(App, self).save(*args, **kwargs)
            from remitapi.models import ApiTransaction
            try:
                transaction = ApiTransaction.objects.get(user=self.owner)
                transaction.app.add(self)
                transaction.last_transaction = timezone.now()
                transaction.save()
            except Exception:
                transaction = ApiTransaction(
                    user=self.owner
                )
                transaction.save()
                transaction.app.add(self)
                transaction.save()
        super(App, self).save(*args, **kwargs)


class ApiTransaction(models.Model):
    '''user profiles'''
    app = models.ManyToManyField(
        App,
        related_name="%(app_label)s_%(class)s_related",
    )
    user = models.ForeignKey(User)
    last_transaction = models.DateTimeField(
        default=timezone.now,
        blank=True
    )

    @property
    def balance(self):
        amount = 0.0
        for app in self.app.all():
            if app.amount and app.status == TRANSACTION.SUCCESS:
                amount += app.amount
        amount = float(amount)
        return amount

    @property
    def last_pk(self):
        previous_transaction = Transaction.objects.all().order_by('-id')[:1][0]

        return previous_transaction.pk



class Wallet(models.Model):
    user = models.ForeignKey(User)
    balance = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    currency = models.CharField(
        max_length=4,
    )
    credit = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    debit = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    added = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(
        User,
        related_name='modified_by',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        '''Auto Save Wallet'''
        add = not self.pk
        if add:
            self.balance = self.current_balance
            super(Wallet, self).save(*args, **kwargs)
        if float(self.debit) > float(self.balance):
            errors = {}
            errors.setdefault('balance',
                              []).append(u'You have insufficient balance')
            raise ValidationError(errors)
        else:
            credit = float(self.credit)
            debit = float(self.debit)
            balance = float(self.balance)
            balance = balance + credit
            balance = balance - debit
            self.balance = float(balance)
        super(Wallet, self).save(*args, **kwargs)

    @property
    def current_balance(self):
        obj = Wallet.objects.filter(user=self.user,
                                    currency=self.currency
                                    ).order_by('-id')[0]
        print "balance %s" % obj
        return float(obj.balance)

    @property
    def initial_balance(self):
        obj = Wallet.objects.filter(user=self.user,
                                    currency=self.currency
                                    ).order_by('id')[0]
        return float(obj.balance)


class USDWallet(Wallet):
    '''
    USD Wallet
    '''

    def save(self, *args, **kwargs):
        '''usd the wallet'''
        self.currency = 'USD'
        super(USDWallet, self).save(*args, **kwargs)


class UGXWallet(Wallet):
    '''
    UGX Wallet
    '''

    def save(self, *args, **kwargs):
        '''ugx wallet'''
        self.currency = 'UGX'
        super(UGXWallet, self).save(*args, **kwargs)


class KESWallet(Wallet):
    '''
    KES Wallet
    '''

    def save(self, *args, **kwargs):
        '''kes wallet'''
        self.currency = 'KES'
        super(KESWallet, self).save(*args, **kwargs)


class RWFWallet(Wallet):
    '''
    KES Wallet
    '''

    def save(self, *args, **kwargs):
        '''kes wallet'''
        self.currency = 'RWF'
        super(RWFWallet, self).save(*args, **kwargs)


class Country(models.Model):
    code = models.CharField(blank=False, max_length=4, unique=True)
    name = models.CharField(blank=False, max_length=40)
    currency = models.CharField(blank=False, max_length=4, unique=True)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=timezone.now, blank=True)
    dailing_code = models.CharField(blank=False, max_length=5, default=256)

    @models.permalink
    def admin_charges_limits_url(self):
        return ('admin_charges_limits', (str(self.code),),)

    @models.permalink
    def admin_rates_limits_url(self):
        return ('admin_rates', (str(self.code),),)

    @property
    def rates(self):
        charge = Charge.objects.get(country=self.pk)
        return charge


class Charge(models.Model):
    '''currency and exchange rates for each country'''
    country = models.ForeignKey(Country, null=True, blank=True)
    forex_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    transfer_fee_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    transfer_maximum_usd = models.DecimalField(
        default=500.00, decimal_places=2, max_digits=10)
    transfer_minimum_usd = models.DecimalField(
        default=100.00, decimal_places=2, max_digits=10)
    mtn_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    airtel_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    orange_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    tigo_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    safaricom_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    vodafone_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    general_network_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=timezone.now, blank=True)
    to_usd = models.DecimalField(
        default=2640.00, decimal_places=2, max_digits=10)
    to_gbp = models.DecimalField(
        default=3974.00, decimal_places=2, max_digits=10)
    to_eur = models.DecimalField(
        default=3256.00, decimal_places=2, max_digits=10)

    @property
    def last_update(self):
        epoch = int(time.mktime(self.added.timetuple()) * 1000)
        return epoch

    @property
    def currency(self):
        '''currency'''
        return str(self.country.currency)

    @property
    def hashid(self):
        '''
        invoice number
        '''
        return str(self.pk ^ 0xABCDEFAB)

    def get_default_rate(self, to_curr):
        '''return default rate , defaults to usd-ugx'''
        curr = 2500.00
        to_curr = to_curr.lower()
        if to_curr == 'usd':
            curr = self.to_usd
        if to_curr == 'gbp':
            curr = self.to_gbp
        if to_curr == 'eur':
            curr = self.to_eur
        return curr

    @property
    def extra_fees(self):
        '''extra network fees'''
        extra_fees = {}
        exts = country_extensions(self.country.code)
        this_charge = 0
        for key, value in exts.iteritems():
            if key == 'airtel':
                this_charge = self.airtel_charge
            elif key == 'safaricom':
                this_charge = self.safaricom_charge
            elif key == 'mtn':
                this_charge = self.mtn_charge
            elif key == 'tigo':
                this_charge = self.tigo_charge
            for x in value:
                extra_fees.update({x: '%s' % this_charge})
        return extra_fees

    def save(self, *args, **kwargs):
         # check if the charge already exists
        if not self.pk:
            if not Charge.objects.filter(country=self.country).exists():
                # continue with save, if necessary:
                super(Charge, self).save(*args, **kwargs)
            else:
                return
        else:
            super(Charge, self).save(*args, **kwargs)


class Rate(models.Model):

    '''Rates and Transaction limits'''

    class Meta:
        permissions = (
            ('view_rate', 'View Rates'),
            ('edit_rate', 'Edit Rates'),
        )

    '''fetch rates and store them'''
    usd_to_rwf = models.DecimalField(
        default=688.00, decimal_places=2, max_digits=10)
    gbp_to_rwf = models.DecimalField(
        default=1114.76, decimal_places=2, max_digits=10)
    usd_to_ugx = models.DecimalField(
        default=2640.00, decimal_places=2, max_digits=10)
    usd_to_kes = models.DecimalField(
        default=85.63, decimal_places=2, max_digits=10)
    usd_to_tzs = models.DecimalField(
        default=1623.00, decimal_places=2, max_digits=10)
    gbp_to_ugx = models.DecimalField(
        default=3974.19, decimal_places=2, max_digits=10)
    gpb_to_kes = models.DecimalField(
        default=129.47, decimal_places=2, max_digits=10)
    gpb_to_tzs = models.DecimalField(
        default=2453.00, decimal_places=2, max_digits=10)
    transfer_limit_usd = models.DecimalField(
        default=500.00, decimal_places=2, max_digits=10)
    transfer_minimum_usd = models.DecimalField(
        default=100.00, decimal_places=2, max_digits=10)
    our_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    percentage_from_forex = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=timezone.now, blank=True)

    def get_rate(self, amount, rate=usd_to_ugx):
        return amount * self[rate]

    def currency_to_usd(self):
        'return the default currency amount in ugx'
        return self.usd_to_ugx

    def currency_transfer_maximum(self):
        'return the default currency amount transfer limit defaults to usd'
        return self.transfer_limit_usd

    def currency_transfer_minimum(self):
        'return the default currency amount transfer limit defaults to usd'
        return self.transfer_minimum_usd

    def remit_charge(self):
        'return the remit chagre defaults to our percentage'
        return self.our_percentage

    def kenyan_fees(self):
        '''temp value for kenyan fees'''
        return 60

    def get_default_rate(self, from_curr, to_curr):
        '''return default rate , defaults to usd-ugx'''
        curr = 2500.00
        from_curr = from_curr.lower()
        to_curr = to_curr.lower()
        if from_curr == 'usd':
            if to_curr == 'ugx':
                curr = self.usd_to_ugx
            if to_curr == 'tzs':
                curr = self.usd_to_tzs
            if to_curr == 'kes':
                curr = self.usd_to_kes
        return curr

    def last_modified_by(self):
        return self.user.username

    @property
    def airtel_charge(self):
        return 300

    @property
    def mtn_charge(self):
        '''temp value'''
        return 390
        # return 0

    def clean(self):
        validate_only_one_instance(self)



class Smile_Session(models.Model):
    session =  models.CharField(blank=False, max_length=40)
    date_created = models.CharField(blank=False, max_length=40)
    expiry_date = models.CharField(blank=False, max_length=40)



