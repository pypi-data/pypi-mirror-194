
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

_v='config-true-seq-nodes'
_u='config-false-prefixes'
_t='table-name-map'
_s='table-keys'
_r='app_ns'
_q='sztpd_meta'
_p='SELECT schema_name FROM information_schema.schemata;'
_o='postgresql'
_n='Cannot delete: '
_m='[^/]*=[^/]*'
_l='[^:]*:'
_k='yang-library'
_j='" does not exist.'
_i=':tenants/tenant'
_h='global-root'
_g='db_ver'
_f='sqlite'
_e=':memory:'
_d='key'
_c='first'
_b='Parent node ('
_a='.singletons'
_Z='mysql'
_Y='" already exists.'
_X='Node "'
_W='sort-by'
_V='.*/'
_U='last'
_T=') does not exist.'
_S='_idx'
_R='_key'
_Q='after'
_P='before'
_O='insert'
_N='ssl'
_M='row_id'
_L=':'
_K='point'
_J='pid'
_I='jsob'
_H='obu_idx'
_G='singletons'
_F='=[^/]*'
_E=True
_D='='
_C=False
_B='/'
_A=None
import os,re,sys,json,base64,pickle,yangson,binascii,pkg_resources,sqlalchemy as sa
from enum import IntFlag
from urllib.parse import quote
from urllib.parse import unquote
from sqlalchemy.sql import and_
from dataclasses import dataclass
from sqlalchemy.sql import bindparam
from sqlalchemy.schema import CreateTable
from .  import db_utils
'\nSQL-based DAL\n\nFirstly, note that the entire persistent store is an facade for a arbitrary hierarchical N-ary tree\nof data, accessed by HTTP operations on URLs.\n\nInternally, this DAL maps the tree to tables as follows:\n\n    1) there is one table called \'singletons\' which contains things that are known to only occur\n       once: metadata (db_ver, key-test, table-defs.), the global root of the data tree (and all\n       descendants up nodes up to the point they\'ve been fanned out to a distinct database table).\n       Each row of this table is its own distinct thing of data, unrelated to any other row in\n       the table.  There are just two columns: \'name\' and \'jsob\' (json object).\n\n       this JSOB has the format:\n\n            {\n                "namespace:node-1" : {-or-[ ... ]-or-},\n                "namespace:node-1" : {-or-[ ... ]-or-},\n                "namespace:node-1" : {-or-[ ... ]-or-}\n                ...\n            }\n\n    2) there is a database table for each node in the YANG model of type \'list\'.  That is, the\n       list is a table and each entry in the list is a row in the table.\n\n       A SQL table is created with its name being the schema_path of the \'list\' node.  This \n       results in some surprisingly long table names, but leads to many benefits in the code.\n\n       Each \'list\' table contains at least one column: \'id\' (a sequential row identifier).\n       \n       If the table is a descendent of another table, then the table will contain another column:\n       \'parent-id\' (the \'id\' of the row in the parent table to which this row is a child).  Note\n       that this construct can support arbitrarily nested tables.\n\n       If the list node is "config true", then the table will contain two more columns: \'key\'\n       and \'jsob\'.   The \'key\' column contains the list\'s key value as a string, allowing for\n       fast lookups.  Typically the table\'s primary key would be the 2-tuple \'parent-id + key\',\n       so that uniqueness per list instance (matching YANG semantics), but if the key node\n       contains the \'globally-unique\' extension contains, then the primary key only includes\n       the \'key\' column (excluding the \'parent-id\' column).  The \'jsob\' (JSON Object) contains\n       a JSON document containing all the node\'s data, including the \'key\' field, but excluding\n       any data belonging to a descendent list/table.\n\n       If the list node is "config false", then the table will contain a column for each descendent\n       node of the \'list\' node.  Each column is appropriately typed (string, integer, datetime,\n       json, etc.), and all simple-typed columns are indexed.  Currently, the "globally-unqiue"\n       extension on the \'key\' node is not supported.\n\n       These JSOBs have the format:  (note that there may be more than one top-level \'dict\')\n            {\n                "namespace:node-1" : { ... },   # prefix always exists, as the DS-root is namespaceless\n                "namespace:node-2" : { ... },   # ditto\n                "namespace:node-3" : { ... }    # ditto\n                ...\n            } \n                         FIXME: how to support top-level lists?  (do they not show up at all in singleton\'s JSOB?)\n\n       For instance, for /wn-sztpd-0:transport/listen/endpoint (this is a \'list\'), each list-entry\n       (i.e., table row) is like:   (note that there may be only one top-level \'dict\')\n\n            {\n                "endpoint" : { ... }\n            }\n\n       In another example, for /admin-accounts/admin-account (this is a \'list\'), each list-entry\n       (i.e., table row) is like:   (note that there may be only one top-level \'dict\')\n\n            {\n                "admin-account" : { ... }\n            }\n\n    \n\n\n    === IGNORE FOR NOW ===\n    3) there is a database table called \'ref-stats\' that contains a row for each node in\n       the YANG model that has been tagged with the special "ref-stats" extension.  This row\n       counts the number of \'leafref\' instances to it or to any of its descendant nodes, as\n       well as tracks when references are added/removed (a single timestamp, not a log).  The\n       tracking of ref-counts to descendant nodes is rather common, as leafrefs are many times\n       to a list\'s "key" field(s) (e.g., a descendant node called "name").  There may exist\n       nested \'ref-stats\' node (e.g., the "certificate" list inside the "assymetric-key" list),\n       in such case it is expected that the ancestor ref-count includes the sum of all the\n       descendant counts plus any additional references to it.  Be aware that while it is most\n       common for a list element to have a \'ref-stats\', it is entirely reasonable for a scaler\n       element to be ref-counted too.\n\n       Side note: the ref counts and timestamps are primarily used by the system itself (not\n       end users) to detect when certain nodes are no longer referenced (i.e., orphaned) and\n       hence can be auto-deleted.  That said, exposing said values to users is goodness too.\n\n\n    FUTURE THOUGHTS\n    ---------------\n    A super-clever implementation would have no \'db-table\' annotations and would simply\n    initialize with just monster-sized top-level jsobs - and then use runtime statistics\n    to evaluate how the database is typically used and dyanamically reset tables as needed.\n\n    But that sounds hard (and perhaps somewhat stupid), perhaps a better idea is to analyze\n    the schema more to find logical break points (e.g., lists with large subtrees, lists\n    with *lots* of elements (i.e., config false), anything that collects ref-stats, etc.?\n\n\n\n\n\n\n\n'
known_text=b'a secret message'
jsob_type=sa.JSON
class ContentType(IntFlag):CONFIG_TRUE=1;CONFIG_FALSE=2;CONFIG_ANY=3
@dataclass
class DatabasePath:data_path:str=_A;schema_path:str=_A;jsob_data_path:str=_A;jsob_schema_path:str=_A;table_name:str=_A;row_id:int=_A;inside_path:str=_A;path_segments:list=_A;jsob:dict=_A;node_ptr:dict=_A;prev_ptr:dict=_A
class AuthenticationFailed(Exception):0
class NodeAlreadyExists(Exception):0
class NodeNotFound(Exception):0
class ParentNodeNotFound(Exception):0
class TooManyNodesFound(Exception):0
class InvalidResourceTarget(Exception):0
class CreateCallbackFailed(Exception):0
class ChangeCallbackFailed(Exception):0
class CreateOrChangeCallbackFailed(Exception):0
class DataAccessLayer:
	'\n    This class contains a five "handle" routines having the signature:\n\n        async def handle_<operation>_<context>_request(self, request)\n\n    Where:\n\n        <operation> is an HTTP operations: get, post, put, and delete.\n                    [FIXME: add support for \'patch\' too!]\n\n        <context> is one of "opstate" or "config"\n                  [Note: the "opstate" context only supports "get"]\n\n    As can be seen from the signature, each of these routines are "async"\n    and take as a parameter a "request" object, the aiohttp-based HTTP\n    request from the RestconfServer layer.\n\n    These routines are only called from higher-level layers are, in\n    particular, as never recursive.  As such, each routine opens a\n    database connection (via a context manager) used by all the DB\n    calls throughout its processing.  Furthermore, for routines\n    that *write* data to the database, a transaction is started\n    using this connection, which is subsequently committed or\n    rollbacked when the routine exits, respectively whether\n    successful or not (e.g., an exception is raised).\n\n    Note that, due to the nature of working with arbitrary trees, these\n    top-level routines often times call on a supporting recursive method.\n    '
	def __init__(A,db_url,cacert_param=_A,cert_param=_A,key_param=_A,yl_obj=_A,app_ns=_A,opaque=_A):
		'\n        db_url:        a SqlAlchemy URL string\n        cacert_param:  path to PEM file containing a list of X.509 certificate\n        cert_param:    path to PEM file containing the client certificate (FIXME: must be a single cert, MySQL-only?)\n        key_param:     path to PEM file containing a key for the client certificate\n        yl_obj:        a Python object containing the yang-library instance used\n                       to initialize a new database with.\n        opaque:        an app-specific python object that can be persisted when\n                       the database is created and returned thereafter.\n        ';F=yl_obj;E=key_param;D=cert_param;C=cacert_param;B=db_url;A.app_ns=_A;A.engine=_A;A.metadata=_A;A.leafrefs=_A;A.referers=_A;A.ref_stat_collectors=_A;A.global_root_id=_A;A.table_keys=_A;A.schema_path_to_real_table_name=_A;A.config_false_prefixes=_A;A.post_dal_callbacks=_A;A.config_true_obu_seq_nodes=_A
		if F is _A:A._init(B,C,D,E)
		else:A.app_ns=app_ns;A._create(B,C,D,E,F,opaque)
		assert A.app_ns!=_A;assert A.engine!=_A;assert A.metadata!=_A;assert A.leafrefs!=_A;assert A.referers!=_A;assert A.ref_stat_collectors!=_A;assert A.global_root_id!=_A;assert A.table_keys!=_A;assert A.schema_path_to_real_table_name!=_A;assert A.config_false_prefixes!=_A;assert A.config_true_obu_seq_nodes!=_A;A.len_app_ns=len(A.app_ns)
	async def num_elements_in_list(A,data_path):
		" Returns the number of elements in the list specified by the passed data-path.\n            The data-path must be for the 'list' node (not its parent node).\n    \n            Note: this is a very special routine that is currently only used to detect if\n                  any admins have been configured, so as to enable/disable auth testing!\n        ";B=data_path;C=re.sub(_F,'',B)
		if C!=B:assert NotImplementedError("Nested listed arren't supported yet.")
		D=A.schema_path_to_real_table_name[C];E=A.metadata.tables[D]
		with A.engine.connect()as F:G=F.execute(sa.select(sa.func.count()).select_from(E));H=G.first()[0];return H
	async def get_tenant_name_for_admin(A,email_address):
		" Returns tenant's name or None (for root)\n            raise NodeNotFound if admin doesn't exist.\n            Only works for mode-'x'.  Calling code must ensure this.\n        ";I='email-address';G=email_address;B=A.schema_path_to_real_table_name[_B+A.app_ns+':tenants/tenant/admin-accounts/admin-account'];C=A.metadata.tables[B]
		with A.engine.connect()as E:
			D=E.execute(sa.select(C.c.pid).where(C.c[I]==G));F=D.first()
			if F!=_A:J=F[0];B=A.schema_path_to_real_table_name[_B+A.app_ns+_i];H=A.metadata.tables[B];D=E.execute(sa.select(H.c.name).where(H.c.row_id==J));K=D.first()[0];return K
		B=A.schema_path_to_real_table_name[_B+A.app_ns+':admin-accounts/admin-account'];C=A.metadata.tables[B]
		with A.engine.connect()as E:
			D=E.execute(sa.select(C.c.pid).where(C.c[I]==G));F=D.first()
			if F!=_A:return _A
		raise NodeNotFound('Admin "'+G+_j)
	async def get_tenant_name_for_global_key(A,table_name,k):
		" Returns tenant's name for the record in table_name having matching key 'k'\n            raise NodeNotFound if k doesn't exist.  Only works for mode-'x'.\n            Calling code must ensure this.\n        ";B=table_name;C=A.schema_path_to_real_table_name[B];E=A.metadata.tables[C]
		with A.engine.connect()as F:
			D=F.execute(sa.select(E.c.pid).where(getattr(E.c,A.table_keys[B])==k));G=D.first()
			if G==_A:raise NodeNotFound('key "'+k+'" in table "'+B+_j)
			I=G[0];C=A.schema_path_to_real_table_name[_B+A.app_ns+_i];H=A.metadata.tables[C];D=F.execute(sa.select(H.c.name).where(H.c.row_id==I));J=D.first()[0];return J
	async def handle_get_opstate_request(B,data_path,query_dict={}):
		'\n        Pretty much a pass-thru to _handle_get_data_request()\n        ';C=query_dict;A=data_path;assert A!='';assert not(A!=_B and A[-1]==_B)
		if A=='/ietf-yang-library:yang-library':
			F=B.schema_path_to_real_table_name[_G];D=B.metadata.tables[F]
			with B.engine.connect()as G:H=G.execute(sa.select(D.c.jsob).where(D.c.name==_k));return H.first()[0]
		E=re.sub(_F,'',A)
		if 0:return await B._handle_get_data_request(A,E,ContentType.CONFIG_FALSE,C)
		else:return await B._handle_get_data_request(A,E,ContentType.CONFIG_ANY,C)
	async def handle_get_config_request(B,data_path,query_dict={}):
		'\n        Fetches data using ContentType.CONFIG_TRUE, but that only prevents data from\n        opstate-tables (which could be huge) from being included. However, the result\n        still contains non-list opstate data, which needs to be cherry-picked out...\n        ';E=data_path;A=re.sub(_F,'',E);F=await B._handle_get_data_request(E,A,ContentType.CONFIG_TRUE,query_dict);C=re.sub(_V,'',A)
		if not C.startswith(B.app_ns+_L):C=B.app_ns+_L+C
		for D in B.config_false_prefixes:
			if D.startswith(A):
				if A==_B:G=D[1:]
				else:G=D.replace(A,C,1)
				I=_A;J=F
				def H(prev_ptr,curr_ptr,remainder_path):
					D=prev_ptr;B=remainder_path;A=curr_ptr;E=B.split(_B)
					for C in E:
						if type(A)==list:
							for F in A:H(A,F,B)
							return
						elif C in A:D=A;A=A[C];B=B.replace(C+_B,'',1)
						else:return
					D.pop(C)
				H(I,J,G)
			else:0
		return F
	async def _handle_get_data_request(A,data_path,schema_path,content_type,query_dict):
		'\n        Recursion strategy:\n          - extract node from appropriate DB-table to create JSOB\n          - then recursively descend jsob/sub-tables, adding into JSOB as it goes\n          - for each JSON, prune out CONFIG FALSE nodes if not wanting them\n          - any failure due to object not existing only occurs at top\n        ';N='Node (';I=content_type;G=schema_path;F=data_path
		if I is ContentType.CONFIG_TRUE and any((G.startswith(B)for B in A.config_false_prefixes)):raise NodeNotFound(N+F+_T)
		with A.engine.connect()as J:
			B=A._get_dbpath_for_data_path(F,I,J)
			if B==_A:raise NodeNotFound(N+F+_T)
			if F!=_B and B.schema_path in A.schema_path_to_real_table_name:
				K,O=F.rsplit(_B,1)
				if _D not in O:
					if K=='':L=_B
					else:L=re.sub(_F,'',K)
					E={};await A._recursively_attempt_to_get_data_from_subtable(B.schema_path,B.row_id,L,B.jsob_data_path,E,I,query_dict,J)
					if E!={}:
						C=next(iter(E))
						if not C.startswith(A.app_ns+_L):E[A.app_ns+_L+C]=E[C];E.pop(C)
					else:
						C=G.rsplit(_B,1)[1]
						if not C.startswith(A.app_ns+_L):C=A.app_ns+_L+C
						E[C]=[]
					return E
			D=re.sub(_V,'',G);P=D
			if D=='':H=B.node_ptr
			else:
				if not D.startswith(A.app_ns+_L):D=A.app_ns+_L+D
				H={}
				if B.table_name!=_G and P==B.inside_path:H[D]=[];H[D].append(B.node_ptr);B.node_ptr=H[D][0]
				else:H[D]=B.node_ptr
			Q=A._get_list_of_direct_subtables_for_schema_path(G)
			for M in Q:R=F+M[len(G):];await A._recursively_attempt_to_get_data_from_subtable(M,B.row_id,G,R,B.node_ptr,I,{},J)
		return H
	async def _recursively_attempt_to_get_data_from_subtable(D,subtable_name,pid,jsob_schema_path,jsob_data_path,jsob_iter,content_type,query_dict,conn):
		'\n        This routine supports the top-level _handle_get_data_request() routine.\n\n        subtable_name: the name of the sub-table to check if data from\n        pid: the parent table\'s "id"\n        jsob_schema_path: an arbitrary schema path (mapped from HTTP client\'s data_path).  Must begin with \'/\' (commonly "/wn-sztpd-?:")\n        jsob_data_path: an arbitrary data_path\n        jsob_iter: a pointer into a DOM being constructed at the spot pointed to by \'jsob_schema_path\'.  It\'s top-node is NOT the path\'s tail segment.\n        conn: the database connection to use (no transaction for \'get\')\n\n        NOTE TO FUTURE SELF:\n          - a "keys-only" query parameter will be added to enable clients to obtain more manageable responses\n             - "off" by default (backwards compatible add)\n             - for "config true" tables, return just the keys\n             - for "config false" tables, return either an empty list, metadata w/ a count, or a remediation msg\n                - metadata?: https://tools.ietf.org/html/rfc7952#section-5.2.2\n        ';K=query_dict;J=content_type;I=jsob_schema_path;C=subtable_name
		if not ContentType.CONFIG_FALSE in J:
			if any((C.startswith(A)for A in D.config_false_prefixes)):return
			else:0
		else:0
		if C in D.config_true_obu_seq_nodes:assert _W not in K;K[_W]=_H
		S=D._find_rows_in_table_having_pid(C,pid,K,conn);L=S.fetchall()
		if len(L)==0:return
		B=jsob_iter
		if I==_B:O=C[1:]
		else:assert I.startswith(_B+D.app_ns);O=C.replace(I+_B,'')
		E=re.sub(_V,'',C);G=re.sub(E+'$','',O)
		if G!='':
			G=G[:-1];T=G.split(_B)
			for M in T:
				try:B=B[M]
				except KeyError as X:assert ContentType.CONFIG_FALSE in J;B[M]={};B=B[M]
		U=D.schema_path_to_real_table_name[C];P=D.metadata.tables[U]
		if any((C.startswith(A)for A in D.config_false_prefixes)):
			B[E]=[]
			for F in L:
				H={}
				for A in P.c:
					if A.name!=_M and A.name!=_J:
						if type(A.type)is sa.sql.sqltypes.DateTime:H[A.name]=F[A.name].strftime('%Y-%m-%dT%H:%M:%SZ')
						elif type(A.type)is sa.sql.sqltypes.JSON or type(A.type)is sa.sql.sqltypes.PickleType:
							if F[A.name]is not _A and not(type(F[A.name])is list and len(F[A.name])==0):H[A.name]=F[A.name]
						elif F[A.name]is not _A:H[A.name]=F[A.name]
				B[E].append(H)
		else:
			Q=0
			for N in L:
				R=N[_I];E=next(iter(R))
				if E not in B:B[E]=[]
				B[E].append(R.pop(E));V=D._get_list_of_direct_subtables_for_schema_path(C)
				for W in V:await D._recursively_attempt_to_get_data_from_subtable(W,N[_M],C,jsob_data_path+_D+N[P.c[2].name],B[E][Q],J,{},conn)
				Q+=1
	async def handle_post_config_request(A,data_path,query_dict,request_body,create_callbacks,change_callbacks,opaque):
		'\n        Parameters:\n          self: dal\n          data_path: the data_path of the node to create\n          request_body: the data definition\n          create_callbacks: a dict, keyed by schema paths, mapping to a list of callbacks\n          change_callbacks: a dict, keyed by schema paths, mapping to a list of callbacks (only called for this object)\n          opaque: an opaque object that is passed into the callback\n\n        Recursion strategy:\n          - recursively descend into jsob/sub-tables (pro-tip: recursive calls only occur at DB-table boundaries)\n          - on exit, extract from JSOB and insert into DB-table\n          - note that any failure due to object already existing will only ever occur at top\n        ';E=request_body;B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B);assert'?'not in B;assert type(E)==dict
		with A.engine.begin()as C:
			F=A._get_dbpath_for_data_path(B,ContentType.CONFIG_TRUE,C)
			if F==_A:raise ParentNodeNotFound(_b+B+_T)
			await A._handle_post_config_request(F,query_dict,E,create_callbacks,change_callbacks,opaque,C)
			if A.post_dal_callbacks is not _A:
				for D in A.post_dal_callbacks:
					try:await D[0](D[1],C,D[2])
					except Exception as G:A.post_dal_callbacks=_A;raise G
				A.post_dal_callbacks=_A
	async def _handle_post_config_request(B,parent_dbpath,query_dict,request_body,create_callbacks,change_callbacks,opaque,conn):
		"\n        Similar to handle_post_config_request() but:\n          - no input validation\n          - no starting of a new transaction\n          - parent node dbpath opened (caller MUST save it out)\n\n        This routine is used by:\n          - handle_post_config_request()   [for obvious reasons]\n          - handle_put_config_request()    [for when PUT implcitily creates (i.e., acts like a POST)]\n          - _handle_put_config_request()   [for when PUT creates internal nodes within itself]\n\n        Parameters:\n          - self: DAL\n          - parent_dbpath: the 'dbpath' for the parent node\n          - request_body: the descendent node to create\n          - create_callbacks: dict containing 'create' callbacks\n          - opaque: arbitrary type passed into callbacks\n          - conn: current database connection\n        ";a=change_callbacks;V=opaque;U=create_callbacks;K=conn;J=query_dict;F=request_body;A=parent_dbpath;O=A.data_path;b=re.sub(_F,'',O);E=next(iter(F))
		if O==_B:C=E;L=_B+C
		else:C=re.sub(_l,'',E);L=O+_B+C
		M=re.sub(_F,'',L);H=B._get_table_name_for_schema_path(M);assert H!=_A
		if H==A.table_name:
			if C in A.node_ptr:
				if type(A.node_ptr[C])!=list:raise NodeAlreadyExists(_X+C+_Y)
				assert len(F[E])==1
				if F[E][0]in A.node_ptr[C]:raise NodeAlreadyExists(_X+F[E][0]+_Y)
				if M not in B.config_true_obu_seq_nodes:A.node_ptr[C].append(F[E][0])
				else:
					G=_U
					if _O in J:G=J[_O]
					if G==_c:assert _K not in J;A.node_ptr[C].insert(0,F[E][0])
					elif G==_U:assert _K not in J;A.node_ptr[C].append(F[E][0])
					else:
						assert G in(_P,_Q);assert _K in J;P=J[_K].rsplit(_D,1)[1];P=unquote(P);D=A.node_ptr[C].index(P)
						if G==_P:0
						elif G==_Q:D=D+1
						A.node_ptr[C].insert(D,F[E][0])
				if M in U:
					for Y in U[M]:await Y(L+_D+F[E][0],A.jsob,A.jsob_data_path,V)
			else:A.node_ptr[C]=F.pop(E);c=await B._recursively_post_subtable_data(A.row_id,L,A.node_ptr[C],A.jsob,A.jsob_data_path,U,V,K)
			B._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,K)
		else:
			assert M in B.table_keys
			if C not in A.node_ptr:A.node_ptr[C]=[];B._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,K)
			Q=F[E][0][B.table_keys[H]]
			if M in B.config_true_obu_seq_nodes:I=B._get_obu_idx_list_for_list_path(L,K)
			W={};assert len(F[E])==1;W[C]=F[E][0];R={};R[_J]=A.row_id;R[B.table_keys[H]]=Q
			if M in B.config_true_obu_seq_nodes:R[_H]=-1
			R[_I]={};S=B.schema_path_to_real_table_name[H];N=B.metadata.tables[S]
			try:Z=K.execute(N.insert().values(**R))
			except sa.exc.IntegrityError:raise NodeAlreadyExists(_X+C+_Y)
			L+=_D+str(Q);c=await B._recursively_post_subtable_data(Z.inserted_primary_key[0],L,W[C],W,L,U,V,K);S=B.schema_path_to_real_table_name[H];N=B.metadata.tables[S];K.execute(N.update().where(N.c.row_id==Z.inserted_primary_key[0]).values(jsob=W))
			if M in B.config_true_obu_seq_nodes:
				if O==_B:d=_B+C
				else:d=O+_B+C
				G=_U
				if _O in J:G=J[_O]
				if G==_c:D=0;T=[(B.table_keys[H],Q),(_H,D)];I.insert(0,T)
				elif G==_U:D=len(I);T=[(B.table_keys[H],Q),(_H,D)];I.append(T)
				else:
					assert G in(_P,_Q);P=J[_K].rsplit(_D,1)[1];D=0
					for X in I:
						if X[0][1]==P:break
						D+=1
					if G==_P:0
					elif G==_Q:D=D+1
					T=[(B.table_keys[H],Q),(_H,D)];I.insert(D,T)
				for X in range(D+1,len(I)):I[X][1]=_H,I[X][1][1]+1
				S=B.schema_path_to_real_table_name[H];N=B.metadata.tables[S];e=B.table_keys[H];f=N.update().where(and_(N.c.pid==A.row_id,getattr(N.c,e)==bindparam(_R))).values(obu_idx=bindparam(_S));Z=K.execute(f,[{_R:A[0][1],_S:A[1][1]}for A in I[D:len(I)]])
			else:0
		g=re.sub(_F,'',O)
		if g in a:
			for Y in a[b]:await Y(O,A.jsob,A.jsob_data_path,V)
	async def _recursively_post_subtable_data(B,pid,data_path,req_body_iter,jsob,jsob_data_path,create_callbacks,opaque,conn):
		"\n        Prune incoming req_body_iter, extracting subtable data out.\n        Calling routine MUST handle saving out any parent data.\n\n        Extract and persist req_body_iter into subtables\n          - will open and save jsobs on table boundaries\n          - req_body_iter is pruned in-place (i.e., the parts put into subtables are removed)\n          - jsob: the parent jsob or None, if this call creates a new list entry (i.e., on a list boundary)\n          - jsob_data_path: the data_path for the parent jsob or None, if this call creates a new list entry (i.e., on a list boundary)\n          - data_path tracking isn't needed for persisting, but is needed for inline callbacks...\n\n        Parameters:\n          - pid: parent table's row-id\n          - data_path: data_path in the request_body tree \n          - req_body_iter: pointer to this place in the request_body tree\n          - (OLD) prev_req_body_iter: pointer to 'req_body_iter' parent node (for inline callbacks)\n          - jsob: pointer to 'jsob' this node is inside (for inline callbacks)\n          - jsob_data_path: the 'data_path' for the 'jsob' passed\n          - create_callbacks: a dictionary (keyed by schema_path) of callbacks to execute when matching nodes are created\n          - opaque: an arbitrary Python object passed into the create callbacks.\n          - conn: the currently opened sqlalchemy database connection\n\n        Returns True if a list, False otherwise (enables caller to trim dict as needed)\n        ";P=pid;M=jsob_data_path;L=jsob;I=conn;H=opaque;E=create_callbacks;D=data_path;A=req_body_iter;C=re.sub(_F,'',D)
		if type(A)==dict:
			'\n            simple recursion, but need to handle case where child is a list\n            '
			if C in E:
				for Q in E[C]:await Q(D,L,M,H)
			for N in A.copy():
				if N.startswith(B.app_ns):F=D+_B+N[B.len_app_ns+1:]
				else:F=D+_B+N
				R=await B._recursively_post_subtable_data(P,F,A[N],L,M,E,H,I)
		elif type(A)==list:
			if C in B.table_keys:
				if C in B.config_true_obu_seq_nodes:S=0
				while A:
					J=A.pop(0);assert type(J)==dict;V=re.sub(_V,'',C);O={};O[V]=J;K=B.table_keys[C];G={};G[_J]=P;G[K]=J[K]
					if C in B.config_true_obu_seq_nodes:G[_H]=S;S+=1
					G[_I]=O;W=B.schema_path_to_real_table_name[C];X=B.metadata.tables[W]
					try:T=I.execute(X.insert().values(**G))
					except sa.exc.IntegrityError as Y:raise NodeAlreadyExists(_X+K+'" with value "'+G[K]+_Y)
					F=D+_D+str(J[K]);R=await B._recursively_post_subtable_data(T.inserted_primary_key[0],F,J,O,F,E,H,I);B._update_jsob_for_row_id_in_table(C,T.inserted_primary_key[0],O,I)
				assert type(A)==list;assert len(A)==0
			else:
				assert type(A)==list
				if not(len(A)==1 and A[0]==_A):
					for U in A:F=D+_D+str(U);R=await B._recursively_post_subtable_data(P,F,A[A.index(U)],L,M,E,H,I)
				else:0
		elif C in E:
			for Q in E[C]:await Q(D,L,M,H)
		if C in B.table_keys:return _E
		return _C
	async def handle_post_opstate_request(A,data_path,request_body):
		"\n        This routine is only used to support internal application logic.\n          - it does NOT support RESTCONF's POST!\n\n        Parameters:\n            data_path: the table name.\n            request_body: the jsob to insert\n\n        This routine is only handles one use case: inserting a new row into an \n        'opstate' table (e.g., audit log, alarms).\n       \n        This routine is NOT expected to insert an opstate node into into a heirarchy\n        of (config) nodes.\n        \n        Note that the parent config-false container is assumed to already exist.\n        That is, even before any entries have been inserted into the opstate\n        table, a GET (opstate) on the parent container should SUCCEED with an\n        empty response.  As such, this routine does NOT test for or auto-create\n        the parent container.\n\n        Recursion strategy: None - all and any sub-lists (or whatever) are\n        stored as JSOBs.\n        ";M='Unrecognized resource schema path: ';I=request_body;E=data_path;B=re.sub(_F,'',E);F=next(iter(I))
		if B==_B:G=F;C=_B+G
		else:G=re.sub(_l,'',F);C=B+_B+G
		J=A._get_table_name_for_schema_path(C)
		if J!=C:raise NodeNotFound(M+C)
		D=I[F];K=re.findall(_m,E)
		if len(K)==0:D[_J]=A.global_root_id
		else:
			L=A._get_table_name_for_schema_path(B)
			if L==_A:raise ParentNodeNotFound(M+B)
			N=K[-1].split(_D)
			with A.engine.connect()as H:D[_J]=A._get_row_id_for_key_in_table(L,N[1],H)
			if D[_J]==_A:raise ParentNodeNotFound('Nonexistent parent resource: '+E)
		O=A.schema_path_to_real_table_name[J];P=A.metadata.tables[O]
		with A.engine.begin()as H:Q=H.execute(P.insert().values(**D))
	async def handle_put_config_request(A,data_path,query_dict,request_body,create_callbacks={},change_callbacks={},delete_callbacks={},opaque=_A):
		'\n        Parameters:\n          self: dal\n          data_path: the data_path of the node to change\n          request_body: the new definition (WARNING: modified by call, as lists are stripped out!)\n          callbacks: dicts, may be empty\n          opaque: an object that DAL passes into the callback\n\n          returns boolean for if PUT acted like a POST (i.e., implicit create)\n        ';B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B)
		with A.engine.begin()as D:
			E=await A._handle_put_config_request(B,query_dict,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,D)
			if A.post_dal_callbacks is not _A:
				for C in A.post_dal_callbacks:
					try:await C[0](C[1],D,C[2])
					except Exception as F:A.post_dal_callbacks=_A;raise F
				A.post_dal_callbacks=_A
			return E
	async def _handle_put_config_request(B,data_path,query_dict,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		"\n        Same as handle_put_config_request() but with the following differences:\n          - no input validation\n          - no starting of a new transaction\n\n        Algorithm:\n          - determine what table it's in\n          - if list, remove row from table (don't need dbpath for this)\n          - else, pop node off jsob and save\n\n          returns boolean for if PUT acted like a POST (i.e., implicit create)\n        ";U=delete_callbacks;S=create_callbacks;P=opaque;L=change_callbacks;I=data_path;F=query_dict;D=request_body;C=conn;K=re.sub(_F,'',I);assert type(D)==dict
		if I==_B:A=B._get_dbpath_for_data_path(_B,ContentType.CONFIG_ANY,C);assert A!=_A;await B.recursive_compare_and_put(A.row_id,_B,D,A.node_ptr,_A,A,S,L,U,P,C);M=B.schema_path_to_real_table_name[A.table_name];J=B.metadata.tables[M];C.execute(J.update().where(J.c.row_id==A.row_id).values(jsob=A.jsob));return _C
		assert len(D)==1;assert K!=_B;A=B._get_dbpath_for_data_path(I,ContentType.CONFIG_ANY,C)
		if A==_A:
			assert I!=_B;G,X=I.rsplit(_B,1)
			if G=='':G=_B
			A=B._get_dbpath_for_data_path(G,ContentType.CONFIG_ANY,C)
			if A==_A:raise ParentNodeNotFound(_b+G+_T)
			await B._handle_post_config_request(A,F,D,S,L,P,C);B._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,C);return _E
		Y=next(iter(D));D=D[Y]
		if type(D)==list:assert len(D)==1;D=D[0]
		await B.recursive_compare_and_put(A.row_id,I,D,A.node_ptr,A.prev_ptr,A,S,L,U,P,C)
		if K in B.config_true_obu_seq_nodes and F!=_A and _O in F:
			if type(A.prev_ptr)==list:A.prev_ptr.remove(A.node_ptr)
			else:assert type(A.prev_ptr)==dict;Z,Q=I.rsplit(_D,1);H=B._get_obu_idx_list_for_list_path(Z,C);H=[A for A in H if A[0][1]!=Q]
			N=F[_O]
			if N==_c:
				assert _K not in F
				if type(A.prev_ptr)==list:A.prev_ptr.insert(0,A.node_ptr)
				else:E=0;O=[(B.table_keys[K],Q),(_H,E)];H.insert(0,O)
			elif N==_U:
				assert _K not in F
				if type(A.prev_ptr)==list:A.prev_ptr.append(A.node_ptr)
				else:E=len(H);O=[(B.table_keys[K],Q),(_H,E)];H.append(O)
			else:
				assert N in(_P,_Q);assert _K in F;V=unquote(F[_K].rsplit(_D,1)[1])
				if type(A.prev_ptr)==list:E=A.prev_ptr.index(V)
				else:
					E=0
					for R in H:
						if R[0][1]==V:break
						E+=1
				if N==_P:0
				elif N==_Q:E=E+1
				if type(A.prev_ptr)==list:A.prev_ptr.insert(E,A.node_ptr)
				else:O=[(B.table_keys[K],Q),(_H,E)];H.insert(E,O)
			if type(A.prev_ptr)!=list:
				for R in range(len(H)):H[R][1]=_H,R
				M=B.schema_path_to_real_table_name[K];J=B.metadata.tables[M];a=B.table_keys[K];b=B._get_row_data_for_list_path(I,C);c=J.update().where(and_(J.c.pid==b[_J],getattr(J.c,a)==bindparam(_R))).values(obu_idx=bindparam(_S));e=C.execute(c,[{_R:A[0][1],_S:A[1][1]}for A in H])
		M=B.schema_path_to_real_table_name[A.table_name];J=B.metadata.tables[M];C.execute(J.update().where(J.c.row_id==A.row_id).values(jsob=A.jsob))
		if K in B.config_true_obu_seq_nodes and F!=_A and _O in F:
			G,X=I.rsplit(_B,1)
			if G=='':G=_B
			W=re.sub(_F,'',G)
			if W in L:
				T=B._get_dbpath_for_data_path(G,ContentType.CONFIG_TRUE,C);assert T!=_A
				for d in L[W]:await d(G,T.jsob,T.jsob_data_path,P)
		return _C
	async def recursive_compare_and_put(C,pid,data_path,req_body_iter,dbpath_curr_ptr,dbpath_prev_ptr,dbpath,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		"\n        Compare the incoming request against what is in the database\n          - anything in the request not in the database is added to dbpath_curr_ptr\n          - anything in the database not in the request is removed from dbpath_curr_ptr\n          - terminal values are replace by request's value\n\n        Parameters:\n          - pid: parent table's row-id\n          - data_path: current data_path in tree (MAY not be on a subtable boundary)\n          - req_body_iter: pointer to this place in the path in the request tree\n          - dbpath_curr_ptr: pointer to this place in the path in the database tree\n          - dbpath_prev_ptr: pointer to the previous node in the database tree (only used when 'dbpath_curr_ptr' is a terminal value)\n          - create_callbacks: dict containing 'create' callbacks\n          - change_callbacks: dict containing 'change' callbacks\n          - (NOTE: 'delete_callbacks' not executing inline only because they cannot affect the persisted jsob)\n          - opaque: arbitrary type passed into callbacks\n          - response: (poorly named) dict containing the paths added/changed/deleted\n          - conn: current database connection\n\n        Assumes caller opens dpath and saves remaining jsob as needed.\n\n        Returns a boolean to indicate if the call changed list contents, and hence tells\n        the recursive caller to execute the change callbacks.\n        ";Y=dbpath_prev_ptr;P=pid;N=delete_callbacks;M=change_callbacks;L=create_callbacks;J=opaque;I=conn;H=dbpath;F=dbpath_curr_ptr;D=req_body_iter;B=data_path;assert type(D)==type(F);E=re.sub(_F,'',B)
		if B==_B:0
		if type(D)==dict:
			S=set(list(D.keys()));T=set(list(F.keys()))
			for A in [A for A in S if A not in T]:
				if type(D[A])==list:
					U=_B+A if B==_B else B+_B+A;V=re.sub(_F,'',U)
					if V in C.table_keys:await C.recursive_compare_and_put(P,U,D[A],[],_A,H,L,M,N,J,I);F[A]=[]
					else:F[A]=[];await C.recursive_compare_and_put(P,U,D[A],F[A],F,H,L,M,N,J,I)
				else:
					E=re.sub(_F,'',B);V=_B+A if E==_B else E+_B+A;assert type(D)!=list;G=_B+A if B==_B else B+_B+A;F[A]=D[A];d=await C._recursively_post_subtable_data(P,G,D[A],H.jsob,H.jsob_data_path,L,J,I)
					if d==1:assert type(D)==dict;assert type(D[A])==list;assert len(D[A])==0;D.pop(A);F.pop(A)
			for A in T-S:
				if _C:U=_B+A if B==_B else B+_B+A;await C.recursive_compare_and_put(P,U,[],F[A],F,H,L,M,N,J,I);del F[A]
				else:
					V=_B+A if E==_B else E+_B+A
					if V in C.config_false_prefixes:0
					else:G=_B+A if B==_B else B+_B+A;await C._recursively_delete_subtable_data(H.row_id,G,F[A],N,J,I);del F[A]
			Z=_C
			for A in T&S:
				G=_B+A if B==_B else B+_B+A;V=re.sub(_F,'',G);e=await C.recursive_compare_and_put(P,G,D[A],F[A],F,H,L,M,N,J,I)
				if e==_E:Z=_E
			if T-S or(S-T or Z==_E):
				if E in M:
					for R in M[E]:await R(B,H.jsob,H.jsob_data_path,J)
			return _C
		elif type(D)==list:
			if E in C.table_keys:
				W=[A[C.table_keys[E]]for A in D];O=set(W);K=set([A[0]for A in C._get_keys_in_table_having_pid(E,P,I)])
				for A in [A for A in W if A not in K]:assert B!=_B;G=B+_D+A;f=[B for B in D if B[C.table_keys[E]]==A][0];g=[f];n=await C._recursively_post_subtable_data(P,B,g,_A,_A,L,J,I)
				for A in K-O:G=B+_D+A;o,a=B.rsplit(_B,1);assert a!='';await C._recursively_delete_subtable_data(H.row_id,G,Y[a],N,J,I)
				for A in K&O:G=B+_D+A;Q=C._get_dbpath_for_data_path(G,ContentType.CONFIG_TRUE,I);assert Q!=_A;h=[B for B in D if B[C.table_keys[E]]==A][0];await C.recursive_compare_and_put(Q.row_id,G,h,Q.node_ptr,Q.prev_ptr,Q,L,M,N,J,I);C._update_jsob_for_row_id_in_table(Q.table_name,Q.row_id,Q.jsob,I)
				b=_C
				if E in C.config_true_obu_seq_nodes:
					i=C._get_obu_idx_list_for_list_path(B,I);c=[[(_d,A),(_H,W.index(A))]for A in W]
					if c!=i:j=C.schema_path_to_real_table_name[E];X=C.metadata.tables[j];k=C.table_keys[E];l=X.update().where(and_(X.c.pid==P,getattr(X.c,k)==bindparam(_R))).values(obu_idx=bindparam(_S));p=I.execute(l,[{_R:A[0][1],_S:A[1][1]}for A in c]);b=_E
				if O-K or K-O or b==_E:return _E
				return _C
			else:
				O=set(D);K=set(F);F.clear();F.extend(D)
				for A in O-K:
					G=B+_D+unquote(A)
					if E in L:
						for R in L[E]:await R(G,H.jsob,H.jsob_data_path,J)
				for A in K-O:
					G=B+_D+unquote(A)
					if E in N:
						for R in N[E]:await R(G,J)
				if O-K or K-O:return _E
				return _C
		else:
			if F!=D:
				m=re.sub('^.*/','',B);Y[m]=D
				if E in M:
					for R in M[E]:await R(B,H.jsob,H.jsob_data_path,J)
			else:0
			return _C
		raise NotImplementedError('logic never reaches this point')
	async def handle_put_opstate_request(D,data_path,request_body):
		'\n        Parameters:\n          - the data_path MUST point to a CONFIG FALSE node.\n          - the data_path immediate ancestor (CT or CF) node MUST exist.\n          - the request_body MUST NOT contain any subtable data.\n\n        This routine is expected to handle just one use case: to\n        update/create a single JSOB-bound CONFIG FALSE subtree.\n        \n        It is NOT expected to append a row into an \'opstate\' table (e.g.,\n        audit log, alarms), as the POST-OPSTATE call is used for that.\n\n        The implementations simply inserts or replaces the request_body\n        at the location in the JSOB specified by data_path.\n\n        This routine may be used to create a new/empty parent container\n        for an CONFIG FALSE \'list\' node, which itself would be persisted\n        in another SQL table.\n\n          Comments:\n             - the need to create the parent CONFIG FALSE container\n               would only happen once, as there is no need to ever\n               "update" it thereafter.\n             - perhaps there is a more direct way to create these\n               parent containers?  (DUNNO)\n             - FIXME:\n                 - seems like the change-callback may need to take\n                   a parameter indicating if the change was due to\n                   a POST/PUT/DELETE op\n                 - otherwise these parent containers may be PUT-ed\n                   over and over again\n                     - we only want to create them the FIRST TIME ONLY!!!\n\n        This routine is provided for internal access only.  It is not\n        accessible via the public RESTCONF interface.\n\n        Recursion strategy: None - all nodes must exist in the JSOB.\n        ';F=request_body;B=data_path;assert B!='';assert not(B!=_B and B[-1]==_B)
		with D.engine.begin()as G:
			C,E=B.rsplit(_B,1);assert E!=''
			if C=='':C=_B
			A=D._get_dbpath_for_data_path(C,ContentType.CONFIG_ANY,G)
			if A==_A:raise ParentNodeNotFound(_b+C+_T)
			assert type(A.node_ptr[E])==type(F);A.node_ptr[E]=F;D._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,G)
	async def handle_delete_config_request(A,data_path,delete_callbacks,change_callbacks,opaque):
		'\n        Parameters:\n          self: dal\n          data_path: the data_path of the node to create\n          delete_callbacks: a dict, keyed by schema paths, mapping to a list of callbacks\n          change_callbacks: a dict, keyed by schema paths, mapping to a list of callbacks (only called for parent object)\n        ';B=data_path;assert B!='';assert B!=_B;assert B[-1]!=_B
		with A.engine.begin()as D:
			await A._handle_delete_config_request(B,delete_callbacks,change_callbacks,opaque,D)
			if A.post_dal_callbacks is not _A:
				for C in A.post_dal_callbacks:
					try:await C[0](C[1],D,C[2])
					except Exception as E:A.post_dal_callbacks=_A;raise E
				A.post_dal_callbacks=_A
	async def _handle_delete_config_request(C,data_path,delete_callbacks,change_callbacks,opaque,conn):
		I=opaque;H=change_callbacks;F=conn;D=data_path;E,G=D.rsplit(_B,1)
		if E=='':E=_B
		A=C._get_dbpath_for_data_path(E,ContentType.CONFIG_TRUE,F)
		if A==_A:raise NodeNotFound(_n+D)
		if _D in G:B,O=G.rsplit(_D,1)
		else:B=G
		assert type(A.node_ptr)==dict
		if B not in A.node_ptr:raise NodeNotFound('Cannot delete '+D+'.')
		await C._recursively_delete_subtable_data(A.row_id,D,A.node_ptr[B],delete_callbacks,I,F)
		if type(A.node_ptr[B])==list:
			J=re.sub(_F,'',D)
			if J in C.table_keys:
				L=C._find_rowids_in_table_having_pid(J,A.row_id,F);M=L.fetchall()
				if len(M)==0:assert type(A.node_ptr[B])==list;assert len(A.node_ptr[B])==0;A.node_ptr.pop(B)
			elif len(A.node_ptr[B])==0:A.node_ptr.pop(B)
		else:A.node_ptr.pop(B)
		C._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,F);K=re.sub(_F,'',E)
		if K in H:
			for N in H[K]:await N(E,A.jsob,A.jsob_data_path,I)
	async def _recursively_delete_subtable_data(A,pid,data_path,curr_data_iter,delete_callbacks,opaque,conn):
		'\n        If it weren\'t for executing delete_callbacks, this routine could be (actually "was") much simpler.\n        However, to execute callbacks, we walk the entire data tree, opening sub-jsobs on list boundaries.\n\n        *** delete callbacks are NEVER called on any OPSTATE nodes! ***\n\n        The recursion strategy, on list boundaries, is to iterate descendants before deleting the row \n        (or all rows matching the pid) from a table.\n        \n        Calling routine MUST handle saving out any parent data.\n\n        Parameters:\n          - pid: parent table\'s row-id\n          - data_path: data_path in the request_body tree \n          - curr_data_iter: pointer to this place in the in-database tree\n          - (OLD) prev_data_iter: pointer to \'curr_data_iter\' parent node (for inline callbacks)\n          - delete_callbacks: a dictionary (keyed by schema_path) of callbacks to execute when matching nodes are deleted\n          - opaque: an arbitrary Python object passed into the delete callbacks.delete\n          - conn: the currently opened sqlalchemy database connection\n\n        Returns 1 if a list, 0 otherwise (enables caller to trim dict as needed)\n        ';J=opaque;G=conn;F=delete_callbacks;E=pid;C=data_path;B=curr_data_iter;H=re.sub(_F,'',C)
		if type(B)==list:
			if H in A.table_keys:
				assert B==[];O,K=C.rsplit(_B,1)
				async def L(pid,data_path,delete_callbacks,opaque,conn):
					D=conn;C=data_path;F=re.sub(_F,'',C);B=A._get_dbpath_for_data_path(C,ContentType.CONFIG_TRUE,D)
					if B==_A:raise NodeNotFound(_n+C)
					G=next(iter(B.jsob));H=B.jsob[G];await A._recursively_delete_subtable_data(B.row_id,C,H,delete_callbacks,opaque,D);I=A.schema_path_to_real_table_name[F];E=A.metadata.tables[I];J=D.execute(sa.delete(E).where(E.c.row_id==B.row_id));assert J.rowcount==1
				if _D in K:await L(E,C,F,J,G)
				else:
					P=[B[0]for B in A._get_keys_in_table_having_pid(H,E,G)]
					for D in P:I=C+_D+D;await L(E,I,F,J,G)
			elif any((H.startswith(B)for B in A.config_false_prefixes)):assert B==[];Q=A.schema_path_to_real_table_name[H];M=A.metadata.tables[Q];S=G.execute(sa.delete(M).where(M.c.pid==E))
			else:
				O,K=C.rsplit(_B,1)
				if _D in K:D=unquote(K.rsplit(_D)[1]);assert D in B;I=C;await A._recursively_delete_subtable_data(E,I,D,F,J,G);B.remove(D)
				else:
					while len(B)!=0:
						D=B[0]
						if D is _A:break
						I=C+_D+D;await A._recursively_delete_subtable_data(E,I,D,F,J,G);B.pop(0)
		elif type(B)==dict:
			for N in B.keys():assert C!=_B;I=C+_B+N;await A._recursively_delete_subtable_data(E,I,B[N],F,J,G)
		else:0
		if not type(B)==list and not any((H.startswith(B)for B in A.config_false_prefixes)):
			if H in F:
				for R in F[H]:await R(C,J)
	def _find_rows_in_table_having_pid(E,table_name,pid,query_dict,conn):
		H='limit';G='offset';F='direction';B=query_dict;I=E.schema_path_to_real_table_name[table_name];C=E.metadata.tables[I];A=sa.select(C).where(C.c.pid==pid)
		if _W in B:D=getattr(C.c,B[_W])
		else:D=C.c.row_id
		if F in B and B[F]=='backwards':A=A.order_by(D.desc())
		else:A=A.order_by(D.asc())
		if G in B:A=A.offset(int(B[G]))
		if H in B:A=A.limit(int(B[H]))
		J=conn.execute(A).mappings();return J
	def _find_rowids_in_table_having_pid(B,table_name,pid,conn):C=B.schema_path_to_real_table_name[table_name];A=B.metadata.tables[C];D=conn.execute(sa.select(A.c.row_id).where(A.c.pid==pid).order_by(A.c.row_id));return D
	def _get_keys_in_table_having_pid(A,table_name,pid,conn):B=table_name;D=A.schema_path_to_real_table_name[B];C=A.metadata.tables[D];E=conn.execute(sa.select(getattr(C.c,A.table_keys[B])).where(C.c.pid==pid));return E
	def _get_list_of_direct_subtables_for_schema_path(D,schema_path):
		A=schema_path
		if A!=_B:assert A[-1]!=_B;A+=_B
		C=[]
		for B in sorted(D.schema_path_to_real_table_name.keys()):
			if str(B).startswith(A):
				if not any((A for A in C if str(B).startswith(A+_B))):
					if str(B)!=_B:C.append(str(B))
					else:0
				else:0
		return C
	def _get_row_id_for_key_in_table(B,table_name,key,conn):
		C=table_name;E=B.schema_path_to_real_table_name[C];D=B.metadata.tables[E];F=conn.execute(sa.select(D.c.row_id).where(getattr(D.c,B.table_keys[C])==key));A=F.fetchall();assert A is not _A
		if len(A)==0:return _A
		if len(A)>1:raise TooManyNodesFound()
		return A[0][0]
	def _get_jsob_iter_for_path_in_jsob(D,jsob,path):
		B=path;assert jsob!=_A;assert B[0]!=_B;A=jsob
		if B!='':
			for C in B.split(_B):
				if C!=''and C not in A:return _A
				A=A[C]
				if type(A)==list:assert len(A)==1;A=A[0]
		return A
	def _get_jsob_for_row_id_in_table(C,table_name,row_id,conn):
		'\n          This routine is heavily used by pytests!\n          ...but it\'s also called by _get_dbpath_for_data_path()\n\n          Modified on June 24, 2020 to also return a pseudo "jsob" for pytests\n            - hopefully doesn\'t break other code depending on the assertion for protection\n                - can\'t be the case currently!\n        ';F=row_id;D=table_name;K=C.schema_path_to_real_table_name[D];A=C.metadata.tables[K]
		if D in C.table_keys:E=conn.execute(sa.select(A.c.jsob).where(A.c.row_id==F));G=E.first();assert G!=_A;return G[0]
		else:
			E=conn.execute(sa.select(A).where(A.c.row_id==F)).mappings();H=E.first();assert H!=_A;I=D.rsplit(_B,1)[1];J={I:{}}
			for B in A.c:
				if B.name!=_M and B.name!=_J:J[I][B.name]=H[B.name]
			return J
	def _insert_jsob_into_table(B,pid,table_name,new_jsob,conn,obu_idx=_A):
		'\n          THIS ROUTINE IS ONLY USED BY PYTEST!\n\n          - works for both "config true" and "config false" tables\n        ';F=obu_idx;D=table_name;C=new_jsob;H=B.schema_path_to_real_table_name[D];I=B.metadata.tables[H];E=next(iter(C));A={};A[_J]=pid
		if D in B.table_keys:
			A[B.table_keys[D]]=C[E][B.table_keys[D]]
			if F!=_A:A[_H]=F
			A[_I]=C
		else:
			for G in C[E].keys():A[G]=C[E][G]
		J=conn.execute(I.insert().values(**A));return J.inserted_primary_key[0]
	def _update_jsob_for_row_id_in_table(A,table_name,row_id,new_jsob,conn):C=A.schema_path_to_real_table_name[table_name];B=A.metadata.tables[C];D=conn.execute(sa.update(B).where(B.c.row_id==row_id).values(jsob=new_jsob))
	def _get_table_name_for_schema_path(D,schema_path):
		'\n        Finds closest "config true" or "config false" YANG "list".\n\n        Return the "long" table name that must contain the node identified\n        by "schema_path".  The returned table_name is either shorter or\n        equal to the specified path.  Scans for the longest prefix match.\n        ';B=len(_B);C=_G
		for A in D.schema_path_to_real_table_name.keys():
			if schema_path.startswith(A)and len(A)>B:B=len(A);C=A
		return C
	def _get_obu_idx_list_for_list_path(B,list_path,conn):
		"\n            - a 'list_path' is a data_path that points to a YANG 'list' (not a list entry)\n            - Returns None if not found.\n        ";D=list_path;assert D[0]==_B;assert D!=_B;assert D[-1]!=_B;C='';E=B.global_root_id;K=D[1:].split(_B)
		for F in K:
			if _D in F:
				L,M=F.split(_D);C+=_B+L;I=B._get_table_name_for_schema_path(C);G=B.schema_path_to_real_table_name[I];A=B.metadata.tables[G];J=conn.execute(sa.select(A.c.row_id,A.c.pid).where(and_(A.c.pid==E,getattr(A.c,B.table_keys[I])==M))).mappings();H=J.fetchone()
				if H==_A:return _A
				assert J.fetchone()==_A;assert E==H[_J];E=H[_M]
			else:C+=_B+F
		G=B.schema_path_to_real_table_name[C];A=B.metadata.tables[G];N=conn.execute(sa.select(getattr(A.c,B.table_keys[C]),A.c.obu_idx).where(A.c.pid==E).order_by(A.c.obu_idx));O=N.fetchall();P=[A._mapping.items()._items for A in O];return P
	def _get_row_data_for_list_path(A,data_path,conn):
		"\n            - a 'list_path' is a data_path that points to a YANG 'list' entry.\n            - Returns None if not found.\n        ";B=data_path;assert B[0]==_B;assert B!=_B;assert B[-1]!=_B;G=B[1:].split(_B);assert _D in G[-1];D='';H=A.global_root_id
		for E in G:
			if _D in E:
				K,L=E.split(_D);D+=_B+K;I=A._get_table_name_for_schema_path(D);M=A.schema_path_to_real_table_name[I];C=A.metadata.tables[M];J=conn.execute(sa.select(C.c.row_id,C.c.pid).where(and_(C.c.pid==H,getattr(C.c,A.table_keys[I])==L))).mappings();F=J.fetchone()
				if F==_A:return _A
				assert J.fetchone()==_A;H=F[_M]
			else:D+=_B+E
		return F
	def _get_dbpath_for_data_path(B,data_path,content_type,conn):
		"\n        Returns a DatabasePath object for the data_path, if the item exists\n\n        Calling routine MUST ensure a CONFIG request isn't asking for a CONFIG FALSE node!\n          - test factored out of here for speed\n\n        Calling routine MUST be aware that CONFIG requests will potentially return JSOB with CONFIG FALSE data\n\n        Opstate Considerations:\n          - config false nodes exist in JSOBs too\n          - put the work onto POST operations, as they're relatively rare and don't need to be as performant\n          - all opstate nodes (including non-presence containers) need to be:\n              - created via initial database creation script (e.g. /audit-logs + /alarms)\n              - auto-created via on-change callbacks (e.g., <node>/ref-stats, <device>/lifecycle-stats, <device>/bootstrapping-log, etc.)\n\n        The DatabasePath object:\n          - table_name:  the name of the table\n          - row_id:      the 'id' of the row containing the data\n          - node_ptr:    pointer to the obj addressed by data_path.  for lists, it is the list entry\n          - prev_ptr:    pointer to node_ptr's parent.  used by list-handling logic, as node_ptr is not a python 'list' obj...\n          - inside_path: the path inside the JSOB containing the data\n\n                         ex: '' for the entire object\n                             `GET /` --> ''\n                         ex: 'foo' for a first-level sub-obj\n                             `GET /transport --> 'transport'\n                             `GET /admin-accounts --> 'admin-accounts'\n                         ex: 'foo/bar' for a second-level sub-obj\n                             `GET /transport/listen --> 'transport/listen'\n                             `GET /admin-accounts/admin-account=foo --> 'admin-account' (as it's the top-level of it's jsob)\n\n        ";D=conn;C=data_path;A=DatabasePath();A.data_path=C;A.schema_path=re.sub(_F,'',C);A.table_name=B._get_table_name_for_schema_path(A.schema_path)
		if A.table_name==_A:return _A
		if C!=_B and A.table_name==A.schema_path:
			G,N=C.rsplit(_B,1)
			if _D not in N:
				if G=='':H=_B
				else:H=re.sub(_F,'',G)
				A.table_name=B._get_table_name_for_schema_path(H);assert A.table_name!=_A
		if A.table_name==_G:A.jsob_data_path=_B;A.jsob_schema_path=_B
		else:
			A.jsob_data_path=C;A.jsob_schema_path=re.sub(_F,'',A.jsob_data_path)
			while A.jsob_schema_path!=A.table_name and A.jsob_schema_path!=_B:O=A.jsob_data_path;A.jsob_data_path=re.sub('(.*=[^/]*)/.*','\\g<1>',A.jsob_data_path);assert A.jsob_data_path!=O;A.jsob_schema_path=re.sub(_F,'',A.jsob_data_path)
			assert A.jsob_schema_path!=_B
		if ContentType.CONFIG_FALSE in content_type and any((A.table_name.startswith(C)for C in B.config_false_prefixes)):raise InvalidResourceTarget("RFC 8040 does not allow queries on lists directly and, because SZTPD doesn't support keys on 'config false' lists, it is never possible to query for 'dbpath.table_name' to be returned.  The 'val' layer should've rejected this query... ")
		if A.jsob_schema_path==_B:A.row_id=B.global_root_id
		else:
			assert A.jsob_schema_path in B.table_keys;assert _D in A.jsob_data_path;I=A.jsob_data_path.split(_B);assert _D in I[-1];E=I[-1].split(_D)
			try:A.row_id=B._get_row_id_for_key_in_table(A.table_name,E[1],D)
			except TooManyNodesFound:
				J=B._get_row_data_for_list_path(A.jsob_data_path,D)
				if J is _A:A.row_id=_A
				else:A.row_id=J[_M]
			if A.row_id==_A:return _A
		assert A.data_path.startswith(A.jsob_data_path);K=A.data_path[len(A.jsob_data_path):];assert A.schema_path.startswith(A.jsob_schema_path);L=A.schema_path[len(A.jsob_schema_path):]
		if A.table_name==_G:A.inside_path=A.schema_path[1:]
		else:M=re.findall(_m,A.jsob_data_path);assert len(M)!=0;E=M[-1].split(_D);A.inside_path=E[0];P=re.sub('^'+A.table_name,'',A.schema_path);assert P==L;A.inside_path+=L
		assert A.inside_path==''or A.inside_path[0]!=_B;A.jsob=B._get_jsob_for_row_id_in_table(A.table_name,A.row_id,D);A.node_ptr=A.jsob;A.prev_ptr=_A
		if A.inside_path=='':A.path_segments=[''];return A
		A.path_segments=A.inside_path.split(_B);Q=''
		for F in A.path_segments:
			Q+=_B+F
			if type(A.node_ptr)==list:raise NotImplementedError('is this path used?');A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[0]
			if F not in A.node_ptr:return _A
			else:A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[F]
		if type(A.node_ptr)==list:
			if _D in K:
				R=unquote(K.rsplit(_D,1)[1])
				try:S=A.node_ptr.index(R)
				except:return _A
				A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[S]
		return A
	def _init(A,url,cacert_param,cert_param,key_param):
		K=key_param;J=cert_param;I=cacert_param;G=url
		if not(G.startswith('sqlite:///')or G.startswith(_Z)or G.startswith(_o)):raise SyntaxError('The database url contains an unrecognized dialect.')
		F={}
		if I is not _A:
			F[_N]={};F[_N]['ca']=I
			if J is not _A:F[_N]['cert']=J
			if K is not _A:F[_N][_d]=K
		A.engine=sa.create_engine(G,connect_args=F);A.db_schema=_A;A.table_keys={};A.config_false_prefixes={};A.config_true_obu_seq_nodes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		try:
			if A.engine.url.database==_e or not db_utils.database_exists(A.engine.url,connect_args=F):A.engine=_A;raise NotImplementedError
		except sa.exc.OperationalError as H:
			if H.orig and'Access denied'in str(H.orig):N=re.sub('^.*"','',re.sub('")$','',str(H.orig)));raise AuthenticationFailed('Authentication failed: '+N)
			else:raise H
		if A.engine.dialect.name==_f:A.schema_path_to_real_table_name[_B]=_G;A.schema_path_to_real_table_name[_G]=_G
		else:
			A.db_schema=A.engine.url.database;A.schema_path_to_real_table_name[_B]=A.db_schema.join(_a);A.schema_path_to_real_table_name[_G]=A.db_schema+_a;O=A.engine.execute(_p);L=O.fetchall();P=[L[A][0]for A in range(len(L))]
			if A.db_schema not in P:A.engine.execute(sa.schema.CreateSchema(A.db_schema));raise NotImplementedError
		A.metadata=sa.MetaData(bind=A.engine,schema=A.db_schema);A.metadata.reflect()
		for Q in A.metadata.tables.values():
			for D in Q.c:
				if type(D.type)is sa.sql.sqltypes.BLOB or type(D.type)is sa.sql.sqltypes.PickleType:D.type=sa.PickleType()
				if A.engine.dialect.name==_Z and type(D.type)is sa.dialects.mysql.types.LONGTEXT:D.type=sa.JSON()
				elif type(D.type)is sa.sql.sqltypes.JSON:D.type=sa.JSON()
		B=A.metadata.tables[A.schema_path_to_real_table_name[_G]]
		with A.engine.connect()as E:
			C=E.execute(sa.select(B.c.jsob).where(B.c.name==_q));M=C.first()[0]
			if M[_g]!=1:raise AssertionError('The database version ('+M[_g]+') is unexpected.')
			C=E.execute(sa.select(B.c.jsob).where(B.c.name==_r));A.app_ns=C.first()[0];C=E.execute(sa.select(B.c.row_id).where(B.c.name==_h));A.global_root_id=C.first()[0];C=E.execute(sa.select(B.c.jsob).where(B.c.name==_s));A.table_keys=C.first()[0];C=E.execute(sa.select(B.c.jsob).where(B.c.name==_t));A.schema_path_to_real_table_name=C.first()[0];C=E.execute(sa.select(B.c.jsob).where(B.c.name==_u));A.config_false_prefixes=C.first()[0];C=E.execute(sa.select(B.c.jsob).where(B.c.name==_v));A.config_true_obu_seq_nodes=C.first()[0]
	def _create(A,url,cacert_param,cert_param,key_param,yl_obj,opaque):
		Q='default startup endpoint';P='endpoint';O='SZTPD_TEST_PATH';N='_sztp_ref_stats_stmt';M='_sztp_globally_unique_stmt';J=key_param;I=cert_param;H=cacert_param;G=yl_obj;C='name';F={}
		if H is not _A:
			F[_N]={};F[_N]['ca']=H
			if I is not _A:F[_N]['cert']=I
			if J is not _A:F[_N][_d]=J
		A.engine=sa.create_engine(url,connect_args=F)
		if A.engine.url.database!=_e and db_utils.database_exists(A.engine.url,connect_args=F):raise AssertionError('Database already exists (call init() first).')
		if A.engine.url.database!=_e:
			if A.engine.dialect.name==_Z:db_utils.create_database(A.engine.url,encoding='utf8mb4',connect_args=F)
			else:db_utils.create_database(A.engine.url,connect_args=F)
		A.db_schema=_A
		if A.engine.dialect.name in(_Z,_o):
			A.db_schema=str(A.engine.url.database);E=A.engine.execute(_p);K=E.fetchall();R=[K[A][0]for A in range(len(K))]
			if A.db_schema not in R:A.engine.execute('CREATE SCHEMA IF NOT EXISTS %s;'%A.db_schema)
		A.metadata=sa.MetaData(schema=A.db_schema);D=sa.Table(_G,A.metadata,sa.Column(_M,sa.Integer,primary_key=_E),sa.Column(_J,sa.Integer,unique=_E),sa.Column(C,sa.String(250),unique=_E),sa.Column(_I,jsob_type));A.metadata.create_all(bind=A.engine)
		with A.engine.begin()as B:B.execute(D.insert(),{C:_q,_I:{_g:1}});B.execute(D.insert(),{C:_r,_I:A.app_ns});B.execute(D.insert(),{C:_k,_I:G});B.execute(D.insert(),{C:'opaque',_I:opaque})
		A.table_keys={_G:C,_B:C};A.config_true_obu_seq_nodes={};A.config_false_prefixes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		if A.engine.dialect.name==_f:A.schema_path_to_real_table_name[_B]=_G;A.schema_path_to_real_table_name[_G]=_G
		else:A.schema_path_to_real_table_name[_B]=A.db_schema+_a;A.schema_path_to_real_table_name[_G]=A.db_schema+_a
		def S(self,stmt,sctx):self.globally_unique=stmt.argument
		setattr(yangson.schemanode.SchemaNode,M,S);yangson.schemanode.SchemaNode._stmt_callback['wn-app:globally-unique']=M
		def T(self,stmt,sctx):self.ref_stats=stmt.argument
		setattr(yangson.schemanode.SchemaNode,N,T);yangson.schemanode.SchemaNode._stmt_callback['wn-app:ref-stats']=N;U=re.sub('\\..*','',__name__);L=pkg_resources.resource_filename(U,'yang/')
		if os.environ.get(O):A.dm=yangson.DataModel(json.dumps(G),[os.environ.get(O),L])
		else:A.dm=yangson.DataModel(json.dumps(G),[L])
		A._gen_tables(A.dm.schema,_G)
		with A.engine.begin()as B:E=B.execute(D.insert(),{C:_t,_I:A.schema_path_to_real_table_name});E=B.execute(D.insert(),{C:_s,_I:A.table_keys});E=B.execute(D.insert(),{C:_u,_I:A.config_false_prefixes});E=B.execute(D.insert(),{C:_v,_I:A.config_true_obu_seq_nodes})
		if os.environ.get('SZTPD_TEST_DAL'):
			with A.engine.begin()as B:E=B.execute(D.insert().values(name=_h,jsob={}))
			A.global_root_id=E.inserted_primary_key[0]
		else:
			with A.engine.begin()as B:E=B.execute(D.insert().values(name=_h,jsob={A.app_ns+':transport':{'listen':{P:[]}},A.app_ns+':audit-log':{'log-entry':[]}}))
			A.global_root_id=E.inserted_primary_key[0];V=A.schema_path_to_real_table_name[_B+A.app_ns+':transport/listen/endpoint'];W=A.metadata.tables[V]
			with A.engine.begin()as B:X=B.execute(W.insert().values(pid=A.global_root_id,name=Q,jsob={P:{C:Q,'use-for':'wn-app:native-interface','http':{'tcp-server-parameters':{'local-address':os.environ.get('SZTPD_INIT_ADDR','127.0.0.1')}}}}))
	def _gen_tables(D,node,parent_table_name):
		"\n        Creates a SQL table for *every* YANG 'list' node.\n          - analysis shows that this leads to about a 25% increase over the number of hand-coded tables,\n            but is simpler than using lots of custom annotations...\n\n        ";N='ref_stats';G=parent_table_name;B=node
		if issubclass(type(B),yangson.schemanode.ListNode):
			C=[];C.append(sa.Column(_M,sa.Integer,primary_key=_E));O=D.schema_path_to_real_table_name[G];C.append(sa.Column(_J,sa.Integer,sa.ForeignKey(O+'.row_id'),index=_E,nullable=_C))
			if B.config==_E:
				if len(B.keys)>1:raise NotImplementedError('Only supports lists with at most one key.')
				E=B.get_child(*B.keys[0]);D.table_keys[B.data_path()]=E.name
				if type(E.type)==yangson.datatype.StringType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.Uint32Type:C.append(sa.Column(E.name,sa.Integer,nullable=_C))
				elif type(E.type)==yangson.datatype.IdentityrefType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.UnionType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.LeafrefType:C.append(sa.Column(E.name,sa.String(250),nullable=_C))
				else:raise Exception('Unsupported key node type: '+str(type(E.type)))
				if hasattr(E,'globally_unique'):C.append(sa.UniqueConstraint(E.name))
				else:C.append(sa.UniqueConstraint(E.name,_J))
				if B.user_ordered==_E:C.append(sa.Column(_H,sa.Integer,index=_E,nullable=_C))
				C.append(sa.Column(_I,jsob_type,nullable=_C))
			else:
				assert B.config==_C;assert hasattr(B,N)==_C
				for A in B.children:
					if issubclass(type(A),yangson.schemanode.LeafNode):
						if type(A.type)==yangson.datatype.StringType:
							if str(A.type)=='date-and-time(string)':C.append(sa.Column(A.name,sa.DateTime,index=_E,nullable=A.mandatory==_C or A.when!=_A))
							else:C.append(sa.Column(A.name,sa.String(250),index=_E,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.Uint16Type:C.append(sa.Column(A.name,sa.SmallInteger,index=_E,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.InstanceIdentifierType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.LeafrefType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.IdentityrefType:C.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.EnumerationType:C.append(sa.Column(A.name,sa.String(250),index=_E,nullable=A.mandatory==_C or A.when!=_A))
						elif type(A.type)==yangson.datatype.UnionType:
							J=0;S=_E
							for K in A.type.types:
								if issubclass(type(K),yangson.datatype.StringType):J+=1
								else:raise Exception('Unhandled union type: '+str(type(K)))
							if J==len(A.type.types):C.append(sa.Column(A.name,sa.String(250),index=_E,nullable=A.mandatory==_C or A.when!=_A))
							else:raise Exception('FIXME: not all union subtypes are stringafiable')
						else:raise Exception('Unhandled leaf type: '+str(type(A.type)))
					elif issubclass(type(A),yangson.schemanode.ChoiceNode):
						H=_E
						for I in A.children:
							assert type(I)==yangson.schemanode.CaseNode
							if len(I.children)>1:H=_C;break
							else:
								for P in I.children:
									if type(P)!=yangson.schemanode.LeafNode:H=_C;break
						if H==_E:C.append(sa.Column(A.name,sa.String(250),index=_E,nullable=A.mandatory==_C or A.when!=_A))
						else:C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.AnydataNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.LeafListNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.ListNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.ContainerNode):C.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_A))
					elif issubclass(type(A),yangson.schemanode.NotificationNode):0
					else:raise Exception('Unhandled list child type: '+str(type(A)))
			Q=re.sub('^/.*:','',B.data_path()).split(_B)
			if D.engine.dialect.name==_f:F=''
			else:F=D.db_schema+'.'
			for R in Q:F+=R[0]
			while F in D.schema_path_to_real_table_name.values():F+='2'
			D.schema_path_to_real_table_name[B.data_path()]=F
			if D.db_schema is _A:L=sa.Table(F,D.metadata,*(C))
			else:L=sa.Table(re.sub('^'+D.db_schema+'.','',F),D.metadata,*(C))
			L.create(bind=D.engine);G=B.data_path()
		if B.config==_C and issubclass(type(B),yangson.schemanode.DataNode):
			M=B.data_path()
			if not any((M.startswith(A)for A in D.config_false_prefixes)):D.config_false_prefixes[M]=_E
		if B.config==_E and issubclass(type(B),yangson.schemanode.SequenceNode)and B.user_ordered==_E:D.config_true_obu_seq_nodes[B.data_path()]=_A
		if hasattr(B,N):D.ref_stat_collectors[B.data_path()]=_A
		if issubclass(type(B),yangson.schemanode.InternalNode):
			if not(type(B)==yangson.schemanode.ListNode and B.config==_C)and not type(B)==yangson.schemanode.RpcActionNode and not type(B)==yangson.schemanode.NotificationNode:
				for A in B.children:D._gen_tables(A,G)