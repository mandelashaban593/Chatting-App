'''remitapi status'''


class MyDict(dict):
	'''
	Dummy Dict
	'''
	pass


TRANSACTION = MyDict()
TRANSACTION.PENDING = 2
TRANSACTION.SUCCESS = 1
TRANSACTION.FAILED = 3