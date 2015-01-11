from contextlib import contextmanager

import bson
class BSONReader(object):
	def __init__(self,filename):
		self.bs = open(filename, 'rb').read()
		self.bs_data = bson.decode_all( self.bs )
		self.stop = False
		self.rows = self._gen()

	def _gen(self):
		for row in self.bs_data:
			yield row
		self.stop = True

	def __iter__(self):
		return self

	def next(self):
		if self.stop:
			raise StopIteration
		else:
			return next(self.rows)

	def __enter__(self):
		print '__enter__'
		return self

	def __exit__(self,*args,**kwargs):
		print '__exit__', args, kwargs

if __name__ == '__main__':
	filename='/home/melladric/dev/repo/vtx-2014/pontofrio/pontofrio_sku_locator/data/dump/pontofrio/pontofrio.bson'
	reader = BSONReader(filename)
	print dir(bson)

	for row in reader:
		print row