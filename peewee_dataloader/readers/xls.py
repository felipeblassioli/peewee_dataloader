from contextlib import contextmanager
from xlrd import open_workbook


class XLSReader(object):
	def __init__(self,filename, skip_headers=True):
		self.workbook = open_workbook(filename)
		self.nr = 0
		self.nrows = 0
		for sheet in self.workbook.sheets():
			self.nrows += sheet.nrows
		self.rows = self._gen(skip_headers)

	def _gen(self, skip_headers):
		for sheet in self.workbook.sheets():
			start = 1 if skip_headers else 0
			for row in range(start,sheet.nrows):
				values = [ sheet.cell(row,col).value for col in range(sheet.ncols) ]
				yield values

	def __iter__(self):
		return self

	def next(self):
		if self.nr > self.nrows:
			raise StopIteration
		else:
			return next(self.rows)

	def __enter__(self):
		print '__enter__'
		return self

	def __exit__(self,*args,**kwargs):
		print '__exit__', args, kwargs

if __name__ == '__main__':
	filename='/home/melladric/dev/repo/vtx-2014/pontofrio/pontofrio_sku_locator/data/MKT_Estoque.xls'
	reader = XLSReader(filename)

	for row in reader:
		print row