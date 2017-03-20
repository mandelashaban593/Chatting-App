'''
network extentions
'''


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    def __getattr__(self, attr):
        return self.get(attr)
    _setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

COUNTRY = {}
COUNTRY['UGANDA'] = 256
COUNTRY['KENYA'] = 254
COUNTRY['RWANDA'] = 250
COUNTRY = dotdict(COUNTRY)

NETWORK = {}
NETWORK['MTN_UGANDA'] = ['78', '77']
NETWORK['AIRTEL_UGANDA'] = ['75', '70']
NETWORK['MPESA'] = ['70', '71', '72', '79']
NETWORK['AIRTEL_KENYA'] = ['73', '78']
NETWORK['MTN_RWANDA'] = ['78', ]
NETWORK = dotdict(NETWORK)


COUNTRY_CODES = {}
COUNTRY_CODES[COUNTRY.UGANDA] = (
    NETWORK.MTN_UGANDA,
    NETWORK.AIRTEL_UGANDA
)

COUNTRY_CODES[COUNTRY.KENYA] = (
    NETWORK.MPESA,
    NETWORK.AIRTEL_KENYA
)


COUNTRY_CODES[COUNTRY.RWANDA] = (
    NETWORK.MTN_RWANDA,
)
