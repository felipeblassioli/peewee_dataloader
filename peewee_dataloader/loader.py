"""
Peewee helper for loading XLS data into a database.

Load the users CSV file into the database and return a Model for accessing
the data:

    from playhouse.csv_loader import load_csv
    db = SqliteDatabase(':memory:')
    User = load_csv(db, 'users.csv')

Provide explicit field types and/or field names:

    fields = [IntegerField(), IntegerField(), DateTimeField(), DecimalField()]
    field_names = ['from_acct', 'to_acct', 'timestamp', 'amount']
    Payments = load_csv(db, 'payments.csv', fields, field_names)
"""


from peewee import *
from peewee import Database
from readers import XLSReader, BSONReader

decode_value = True

class Loader(object):

	def __init__(self, db_or_model, filename, fields, field_names,
		has_header=True, db_table=None, ignore_fields=None, process_row=None, **reader_kwargs):
		self.filename = filename
		self.fields = fields
		self.field_names = field_names
		self.has_header = has_header
		self.process_row = process_row
		self.reader_kwargs = reader_kwargs

		if isinstance(db_or_model, Database):
			self.database = db_or_model
			self.model = None
			self.db_table = (
				db_table or
				os.path.splitext(os.path.basename(self.filename))[0])
		else:
			self.model = db_or_model
			self.database = self.model._meta.database
			self.db_table = self.model._meta.db_table
			self.fields = self.model._meta.get_fields()
			self.field_names = self.model._meta.get_field_names()

			if ignore_fields is not None:
				for fname in ignore_fields:
					self.field_names.remove(fname)
			# If using an auto-incrementing primary key, ignore it.
			if self.model._meta.auto_increment:
				self.fields = self.fields[1:]
				self.field_names = self.field_names[1:]

	def get_reader(self,filename,**reader_kwargs):
		raise NotImplementedError()

	def get_model_class(self, field_names, fields):
		if self.model:
			return self.model
		attrs = dict(zip(field_names, fields))
		attrs['_auto_pk'] = PrimaryKeyField()
		klass = type(self.db_table.title(), (Model,), attrs)
		klass._meta.database = self.database
		klass._meta.db_table = self.db_table
		return klass

	def load(self):
		with self.get_reader(self.filename, **self.reader_kwargs) as reader:
			if self.has_header:
				next(reader)

			ModelClass = self.get_model_class(self.field_names, self.fields)

			with self.database.transaction():
				ModelClass.create_table(fail_silently=True)
				for row in reader:
					if self.process_row is not None:
						row = self.process_row(row)
					insert = dict()
					for field_name, value in zip(self.field_names, row):
						insert[field_name] = value
					if insert:
						ModelClass.insert(**insert).execute()

			return ModelClass

class XLSLoader(Loader):
	def get_reader(self,filename,**reader_kwargs):
		return XLSReader(filename, **reader_kwargs)

class BSONLoader(Loader):
	def get_reader(self,filename,**reader_kwargs):
		return BSONReader(filename, **reader_kwargs)

def load_xls(db_or_model, filename, fields=None, field_names=None,
             has_header=True, db_table=None, ignore_fields=None, process_row=None, **reader_kwargs):
    loader = XLSLoader(db_or_model, filename, fields, field_names, has_header, db_table, ignore_fields, process_row, **reader_kwargs)
    return loader.load()

def load_bson(db_or_model, filename, fields=None, field_names=None,
         has_header=True, db_table=None, ignore_fields=None, process_row=None, **reader_kwargs):
	loader = BSONLoader(db_or_model, filename, fields, field_names, has_header, db_table, ignore_fields, process_row, **reader_kwargs)
	return loader.load()