
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

_G=':memory:'
_F='template1'
_E='postgres'
_D='sqlite'
_C=False
_B='postgresql'
_A=None
import os
from copy import copy
import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError,ProgrammingError
def _set_url_database(url,database):
	'Set the database of an engine URL.\n\n    :param url: A SQLAlchemy engine URL.\n    :param database: New database to set.\n\n    ';C=database;A=url
	if hasattr(sa.engine,'URL'):B=sa.engine.URL.create(drivername=A.drivername,username=A.username,password=A.password,host=A.host,port=A.port,database=C,query=A.query)
	else:A.database=C;B=A
	assert B.database==C,B;return B
def _get_scalar_result(engine,sql):
	with engine.connect()as A:return A.scalar(sql)
def _sqlite_file_exists(database):
	A=database
	if not os.path.isfile(A)or os.path.getsize(A)<100:return _C
	with open(A,'rb')as B:C=B.read(100)
	return C[:16]==b'SQLite format 3\x00'
def database_exists(url,connect_args=_A):
	"Check if a database exists.\n\n    :param url: A SQLAlchemy engine URL.\n\n    Performs backend-specific testing to quickly determine if a database\n    exists on the server. ::\n\n        database_exists('postgresql://postgres@localhost/name')  #=> False\n        create_database('postgresql://postgres@localhost/name')\n        database_exists('postgresql://postgres@localhost/name')  #=> True\n\n    Supports checking against a constructed URL as well. ::\n\n        engine = create_engine('postgresql://postgres@localhost/name')\n        database_exists(engine.url)  #=> False\n        create_database(engine.url)\n        database_exists(engine.url)  #=> True\n\n    ";E=connect_args;A=url;A=copy(make_url(A));C=A.database;F=A.get_dialect().name;B=_A
	try:
		if F==_B:
			D="SELECT 1 FROM pg_database WHERE datname='%s'"%C
			for G in (C,_E,_F,'template0',_A):
				A=_set_url_database(A,database=G);B=sa.create_engine(A,connect_args=E)
				try:return bool(_get_scalar_result(B,D))
				except (ProgrammingError,OperationalError):pass
			return _C
		elif F=='mysql':A=_set_url_database(A,database=_A);B=sa.create_engine(A,connect_args=E);D="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'"%C;return bool(_get_scalar_result(B,D))
		elif F==_D:
			A=_set_url_database(A,database=_A);B=sa.create_engine(A,connect_args=E)
			if C:return C==_G or _sqlite_file_exists(C)
			else:return True
		else:
			D='SELECT 1'
			try:B=sa.create_engine(A,connect_args=E);return bool(_get_scalar_result(B,D))
			except (ProgrammingError,OperationalError):return _C
	finally:
		if B:B.dispose()
def create_database(url,encoding='utf8',template=_A,connect_args=_A):
	"Issue the appropriate CREATE DATABASE statement.\n\n    :param url: A SQLAlchemy engine URL.\n    :param encoding: The encoding to create the database as.\n    :param template:\n        The name of the template from which to create the new database. At the\n        moment only supported by PostgreSQL driver.\n\n    To create a database, you can pass a simple URL that would have\n    been passed to ``create_engine``. ::\n\n        create_database('postgresql://postgres@localhost/name')\n\n    You may also pass the url from an existing engine. ::\n\n        create_database(engine.url)\n\n    Has full support for mysql, postgres, and sqlite. In theory,\n    other database engines should be supported.\n    ";K='mssql';I=connect_args;H=encoding;G=template;A=url;A=copy(make_url(A));E=A.database;C=A.get_dialect().name;J=A.get_dialect().driver
	if C==_B:A=_set_url_database(A,database=_E)
	elif C==K:A=_set_url_database(A,database='master')
	elif not C==_D:A=_set_url_database(A,database=_A)
	if C==K and J in{'pymssql','pyodbc'}or C==_B and J in{'asyncpg','pg8000','psycopg2','psycopg2cffi'}:B=sa.create_engine(A,isolation_level='AUTOCOMMIT',connect_args=I)
	else:B=sa.create_engine(A,connect_args=I)
	if C==_B:
		if not G:G=_F
		F="CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(quote(B,E),H,quote(B,G))
		with B.connect()as D:D.execute(F)
	elif C=='mysql':
		F="CREATE DATABASE {0} CHARACTER SET = '{1}'".format(quote(B,E),H)
		with B.connect()as D:D.execute(F)
	elif C==_D and E!=_G:
		if E:
			with B.connect()as D:D.execute('CREATE TABLE DB(id int);');D.execute('DROP TABLE DB;')
	else:
		F='CREATE DATABASE {0}'.format(quote(B,E))
		with B.connect()as D:D.execute(F)
	B.dispose()
from sqlalchemy.orm.session import object_session
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm.exc import UnmappedInstanceError
def quote(mixed,ident):
	'\n    Conditionally quote an identifier.\n    ::\n\n\n        from sqlalchemy_utils import quote\n\n\n        engine = create_engine(\'sqlite:///:memory:\')\n\n        quote(engine, \'order\')\n        # \'"order"\'\n\n        quote(engine, \'some_other_identifier\')\n        # \'some_other_identifier\'\n\n\n    :param mixed: SQLAlchemy Session / Connection / Engine / Dialect object.\n    :param ident: identifier to conditionally quote\n    ';A=mixed
	if isinstance(A,Dialect):B=A
	else:B=get_bind(A).dialect
	return B.preparer(B).quote(ident)
def get_bind(obj):
	'\n    Return the bind for given SQLAlchemy Engine / Connection / declarative\n    model object.\n\n    :param obj: SQLAlchemy Engine / Connection / declarative model object\n\n    ::\n\n        from sqlalchemy_utils import get_bind\n\n\n        get_bind(session)  # Connection object\n\n        get_bind(user)\n\n    ';A=obj
	if hasattr(A,'bind'):B=A.bind
	else:
		try:B=object_session(A).bind
		except UnmappedInstanceError:B=A
	if not hasattr(B,'execute'):raise TypeError('This method accepts only Session, Engine, Connection and declarative model objects.')
	return B