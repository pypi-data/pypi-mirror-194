
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_A3=' found): '
_A2=b"this is some data I'd like to sign"
_A1='Unsupported "private-key-format" ('
_A0='cleartext-private-key'
_z='Parsing public key structure failed for '
_y='Unsupported "public-key-format" ('
_x='ietf-crypto-types:subject-public-key-info-format'
_w='should check to see if an alarm can be cleared...'
_v='admin-account'
_u='%Y-%m-%dT%H:%M:%SZ'
_t='password-last-modified'
_s='module'
_r='.plugins.'
_q="why wasn't this assertion caught by val? "
_p='operation-failed'
_o='data-exists'
_n='missing-attribute'
_m='Unable to parse "input" JSON document: '
_l='malformed-message'
_k='method'
_j='": '
_i='cert-data'
_h='public-key'
_g='\\g<1>'
_f='.*plugins/plugin=([^/]*).*'
_e='function'
_d='\\..*'
_c='application/yang-data+json'
_b='The asymmetric-key has a mismatched public/private key pair: '
_a='ietf-crypto-types:rsa-private-key-format'
_Z='ietf-crypto-types:ec-private-key-format'
_Y=') for '
_X='public-key-format'
_W='need to implement this code'
_V='SZTPD_INIT_MODE'
_U='plugin'
_T=False
_S='operation-not-supported'
_R='functions'
_Q='name'
_P='certificate'
_O='certificates'
_N=' ('
_M=True
_L='+'
_K='text/plain'
_J='password'
_I='unknown-element'
_H='sleep'
_G='private-key-format'
_F='invalid-value'
_E='application'
_D='protocol'
_C='asymmetric-key'
_B=None
_A='/'
import os,re,sys,json,base64,signal,asyncio,yangson,datetime,basicauth,importlib,pkg_resources
from enum import Enum
from aiohttp import web
from enum import IntFlag
from fifolock import FifoLock
from passlib.hash import sha256_crypt
from .dal import DataAccessLayer
from .val import ValidationLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from .  import dal
from .  import val
from .  import utils
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as decode_der
from pyasn1.error import PyAsn1Error
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc4055
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5480
from pyasn1_modules import rfc5915
from pyasn1_modules import rfc5652
from pyasn1.type import univ
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.x509.oid import ExtensionOID
class RefAction(IntFlag):ADDED=1;REMOVED=2
class TimeUnit(Enum):Days=2;Hours=1;Minutes=0
class Period:
	def __init__(A,amount,units):A.amount=amount;A.units=units
class PluginNotFound(Exception):0
class PluginSyntaxError(Exception):0
class FunctionNotFound(Exception):0
class FunctionNotCallable(Exception):0
class Read(asyncio.Future):
	@staticmethod
	def is_compatible(holds):return not holds[Write]
class Write(asyncio.Future):
	@staticmethod
	def is_compatible(holds):A=holds;return not A[Read]and not A[Write]
class BinaryTypePatcher:
	def __init__(A):A.save=yangson.datatype.BinaryType.from_raw
	async def __aenter__(B):
		def A(self,raw):
			'Override superclass method.'
			try:return base64.b64decode('BASE64VALUE=',validate=_M)
			except TypeError:return _B
		yangson.datatype.BinaryType.from_raw=A
	async def __aexit__(A,exc_type,exc,tb):yangson.datatype.BinaryType.from_raw=A.save
class NativeViewHandler(RouteHandler):
	"\n      Implements view handler for the SZTPD's Native NBI view (0, 1, or x)\n\n      Notes:\n        - there is a huge assumption that all DAL-native models are wnapp based!\n        - the default opstate-renderer assumes all config-false vals are in DB (no special opstate callbacks needed)\n\n    ";len_prefix_running=RestconfServer.len_prefix_running;len_prefix_operational=RestconfServer.len_prefix_operational;len_prefix_operations=RestconfServer.len_prefix_operations;supported_media_types=_c,
	def __init__(A,_dal,_mode,_loop):
		S=':tenants/tenant/truststore/certificate-bags/certificate-bag/certificate/cert-data';R=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/certificates/certificate/cert-data';Q=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/cleartext-private-key';P=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/public-key';O=':truststore/certificate-bags/certificate-bag/certificate/cert-data';N=':keystore/asymmetric-keys/asymmetric-key/certificates/certificate/cert-data';M=':keystore/asymmetric-keys/asymmetric-key/cleartext-private-key';L=':keystore/asymmetric-keys/asymmetric-key/public-key';K=':preferences/system/plugins/plugin/functions/function';J=':preferences/system/plugins/plugin';I=':tenants/tenant/admin-accounts/admin-account/password';H='multi-tenant';G=':admin-accounts/admin-account/password';F=':plugins';A.dal=_dal;A.mode=_mode;A.loop=_loop;A.fifolock=FifoLock();A.create_callbacks={};A.change_callbacks={};A.delete_callbacks={};A.subtree_change_callbacks={};A.somehow_change_callbacks={};A.leafref_callbacks={};A.periodic_callbacks={};A.onetime_callbacks={};A.plugins={};B=A.dal.handle_get_opstate_request('/ietf-yang-library:yang-library');T=A.loop.run_until_complete(B);U=re.sub(_d,'',__name__);V=pkg_resources.resource_filename(U,'yang/');A.dm=yangson.DataModel(json.dumps(T),[V]);A.val=ValidationLayer(A.dm,A.dal);B=A.dal.handle_get_opstate_request(_A+A.dal.app_ns+':preferences/system/plugins')
		try:D=A.loop.run_until_complete(B)
		except dal.NodeNotFound:pass
		else:
			if _U in D[A.dal.app_ns+F]:
				for C in D[A.dal.app_ns+F][_U]:
					W=C[_Q];B=_handle_plugin_created('',{_U:C},'',A);A.loop.run_until_complete(B)
					if _R in C:
						for E in C[_R][_e]:Z=E[_Q];X='FOO/plugins/plugin='+W+'/BAR';B=_handle_function_created('',{_e:E},X,A);A.loop.run_until_complete(B)
		A.register_create_callback(_A+A.dal.app_ns+G,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+G,_handle_admin_passwd_changed)
		if A.mode==H:A.register_create_callback(_A+A.dal.app_ns+I,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+I,_handle_admin_passwd_changed)
		A.register_create_callback(_A+A.dal.app_ns+':tenants/tenant',_handle_tenant_created);A.register_create_callback(_A+A.dal.app_ns+J,_handle_plugin_created);A.register_delete_callback(_A+A.dal.app_ns+J,_handle_plugin_deleted);A.register_create_callback(_A+A.dal.app_ns+K,_handle_function_created);A.register_delete_callback(_A+A.dal.app_ns+K,_handle_function_deleted);A.register_create_callback(_A+A.dal.app_ns+L,_handle_asymmetric_public_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+L,_handle_asymmetric_public_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+M,_handle_asymmetric_private_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+M,_handle_asymmetric_private_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+N,_handle_asymmetric_key_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+N,_handle_asymmetric_key_cert_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+O,_handle_trust_anchor_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+O,_handle_trust_anchor_cert_created_or_changed)
		if A.mode==H:A.register_create_callback(_A+A.dal.app_ns+P,_handle_asymmetric_public_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+P,_handle_asymmetric_public_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+Q,_handle_asymmetric_private_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+Q,_handle_asymmetric_private_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+R,_handle_asymmetric_key_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+R,_handle_asymmetric_key_cert_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+S,_handle_trust_anchor_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+S,_handle_trust_anchor_cert_created_or_changed)
		A.register_change_callback(_A+A.dal.app_ns+':transport/listen',_handle_transport_changed);A.register_delete_callback(_A+A.dal.app_ns+':transport',_handle_transport_delete);A.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations)
		for Y in A.dal.ref_stat_collectors:A.register_create_callback(Y.replace('/reference-statistics',''),_handle_ref_stat_parent_created)
	def register_create_callback(A,schema_path,callback):
		"\n        Executes when the specified node is created.\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback to execute when match (see below)\n\n        The 'callback' function must have the following signature:\n\n            async def func_name(watched_node_path: str, jsob: dict, jsob_data_path: str, obj: object) -> None:\n               '''\n               Parameters:\n                 watched_node_path : the data_path to the specific changed object having the schema_path\n                 jsob              : the python object that is about to be written to the database\n                 jsob_data_path    : the data_path of the above jsob object\n                 opaque            : the opaque object passed into the DAL's 'handle' routine\n\n               Note that the purpose of the `jsob` and `jsob_data_path` parameters is to enable the\n               callback to, potentially, update the incoming object before it is persisted, thereby\n               avoiding the need to perform additional database queries.  If a query or change is\n               needed beyond this, then the code must use DAL (via 'obj') to acheive its goal.\n               '''\n        ";C=callback;B=schema_path
		if B not in A.create_callbacks:A.create_callbacks[B]=[C]
		else:A.create_callbacks[B].append(C)
	def register_change_callback(A,schema_path,callback):
		"\n        Executes only when the specific node changed.  For terminal nodes, this is when the\n        node's value changes.  For non-terminal nodes, this is when a descendent is added\n        or removed.\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback to execute when match (see below)\n\n        The 'callback' function must have the following signature:\n\n            async def func_name(watched_node_path: str, jsob: dict, jsob_data_path: str, obj: object) -> None:\n               '''\n               Parameters:\n                 watched_node_path : the data_path to the specific changed object having the schema_path\n                 jsob              : the python object that is about to be written to the database\n                 jsob_data_path    : the data_path of the above jsob object\n                 obj               : the opaque object passed into the DAL's 'handle' routine\n\n               Note that the purpose of the `jsob` and `jsob_data_path` parameters is to enable the\n               callback to, potentially, update the incoming object before it is persisted, thereby\n               avoiding the need to perform additional database queries.  If a query or change is\n               needed beyond this, then the code must use DAL (via 'obj') to acheive its goal.\n               '''\n        ";C=callback;B=schema_path
		if B not in A.change_callbacks:A.change_callbacks[B]=[C]
		else:A.change_callbacks[B].append(C)
	def register_subtree_change_callback(A,schema_path,callback):
		"\n        Builds on top of the 'change' callback to notify whenever any part of an object's immediate\n        subtree is change.  This routine is itself built on top of by the 'implicit' change callback\n        handler.\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback to execute when match (see below)\n\n        The `callback` function must have the following signature:\n\n            #FIXME: this is right only if inline-func does the work.  if it instead sets a flag\n            #       for a post-sweep routine, it wouldn't have the jsob or jsob_data_path...\n            async def func_name(watched_node_path: str, jsob: dict, jsob_data_path: str, obj: object) -> None:\n               '''\n               Parameters:\n                 watched_node_path : the data_path to the object changed having the specified schema_path\n                 nvh               : this NativeViewHandler object\n               '''\n        ";C=callback;B=schema_path
		if B not in A.subtree_change_callbacks:A.subtree_change_callbacks[B]=[C]
		else:A.subtree_change_callbacks[B].append(C)
	def register_somehow_change_callback(A,schema_path,callback):
		"\n        Builds on top of the 'explicit' change callback to notify whenever any part of an object changes,\n        including any aspect of any recursively leafref-ed object changes.\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback to execute when match (see below)\n\n        The `callback` function must have the following signature:\n\n            #FIXME: this is right only if inline-func does the work.  if it instead sets a flag\n            #       for a post-sweep routine, it wouldn't have the jsob or jsob_data_path...\n            async def func_name(watched_node_path: str, jsob: dict, jsob_data_path: str, obj: object) -> None:\n               '''\n               Parameters:\n                 watched_node_path : the data_path to the object changed having the specified schema_path\n                 nvh               : this NativeViewHandler object\n               '''\n        ";C=callback;B=schema_path
		if B not in A.somehow_change_callbacks:A.somehow_change_callbacks[B]=[C]
		else:A.somehow_change_callbacks[B].append(C)
	def register_delete_callback(A,schema_path,callback):
		"\n        Executes when the specified node is deleted.\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback to execute when match (see below)\n\n        The 'callback' function must have the following signature:\n\n            async def func_name(watched_node_path: str, obj: object) -> None:\n               '''\n               Parameters:\n                 watched_node_path : the data_path to the deleted object having the schema_path\n                 obj               : the opaque object passed into the DAL's 'handle' routine\n               '''\n        ";C=callback;B=schema_path
		if B not in A.delete_callbacks:A.delete_callbacks[B]=[C]
		else:A.delete_callbacks[B].append(C)
	def register_onetime_callback(A,timestamp,callback,opaque):
		"\n        Parameters:\n          self        : this NativeViewHandler object\n          datatime    : the timestamp for when to call this callback\n          callback    : the callback to execute when match (see below)\n          opaque      : an arbitrary object that will be passed into the callback function\n\n        The `callback` function must have the following signature:\n\n            # FIXME: async def no longer needed?\n            def func_name(self: NativeViewHandler, opaque: object) -> None\n               '''\n               Parameters:\n                 self        : this NativeViewHandler object, even if/when registered by an external class!!!\n                 opaque      : the `opaque` parameter that was passed in the registration call\n\n               Note that the purpose of the `opaque` parameter is enable one-time callback to have\n               an idea as to why it is being called (e.g., the data_path to a specific object).\n\n               Exceptions: None\n               '''\n\n        Exceptions: None\n        ";B=callback
		if schema_path not in A.onetime_callbacks:A.onetime_callbacks[schema_path]=[B]
		else:A.onetime_callbacks[schema_path].append(B)
	def register_periodic_callback(A,period,anchor,callback):"\n        Parameters:\n          self        : this NativeViewHandler object\n          period      : the frequency expressed as a 2-tuple (amount, units)\n          anchor      : an anchor point that defines an offset/shift for the period\n          callback    : the callback to execute when match (see below)\n\n        The `callback` function must have the following signature:\n\n            # FIXME: async def no longer needed?\n            async def func_name(self: NativeViewHandler) -> None\n               '''\n               Parameters:\n                 self        : this NativeViewHandler object, even if/when registered by an external class!!!\n\n               Exceptions: None\n               '''\n\n        Exceptions: None\n        "
	def register_leafref_callback(A,schema_path,callback):
		"\n        NOTES:\n          - This routine supports reference statistics tracking.\n          - It does not support sub-object change detection\n\n        Parameters:\n          self        : this NativeViewHandler object\n          schema_path : the schema_path to monitor\n          callback    : the callback (see below) to execute when objects having the\n                        schema_path are referenced or unreferenced.\n\n        The `callback` function must have the following signature:\n\n            # FIXME: async def no longer needed?\n            async def func_name(self: NativeViewHandler, data_path: str, ref_action: RefAction, referrer_dpath: str) -> None\n               '''\n               Parameters:\n                 self           : this NativeViewHandler object, even if/when registered by an external class!!!\n                 data_path      : the data_path to the object that refed/unrefed\n                 ref_action     : indicates if a reference was added or removed.\n                 referrer_dpath : the data_path of the referrer\n\n               The code must use `self.dal` to persist any `reference-statistics` updates.\n\n               Exceptions: None\n               '''\n\n        Exceptions: None\n        ";C=callback;B=schema_path
		if B not in A.leafref_callbacks:A.leafref_callbacks[B]=[C]
		else:A.leafref_callbacks[B].append(C)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		C=audit_log_entry;B=tenant_name
		if C[_k]in{'GET','HEAD'}:return
		if B==_B:D=_A+A.dal.app_ns+':audit-log'
		else:D=_A+A.dal.app_ns+':tenants/tenant='+B+'/audit-log'
		E={};E[A.dal.app_ns+':log-entry']=C;await A.dal.handle_post_opstate_request(D,E)
	async def _check_auth(B,request,data_path):
		'\n          returns:\n             on error: web.Response(401)\n             success: web.Response(200)\n        ';P='No authorization required for fresh installs.';O=':admin-accounts/admin-account';L='access-denied';K='failure';J='success';G='comment';E='outcome';D=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=D.remote;A['source-proxies']=list(D.forwarded);A['host']=D.host;A[_k]=D.method;A['path']=D.path;M=D.headers.get('AUTHORIZATION')
		if M is _B:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+O)
			if H==0:A[E]=J;A[G]=P;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[E]=K;A[G]='No authorization specified in the HTTP header.';await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);F=utils.gen_rc_errors(_D,L);C.text=json.dumps(F,indent=2);return C
		I,Q=basicauth.decode(M);R=_A+B.dal.app_ns+':admin-accounts/admin-account='+I+'/password'
		try:S=await B.dal.handle_get_config_request(R)
		except dal.NodeNotFound as T:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+O)
			if H==0:A[E]=J;A[G]=P;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[E]=K;A[G]='Unknown admin: '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);F=utils.gen_rc_errors(_D,L);C.text=json.dumps(F,indent=2);return C
		N=S[B.dal.app_ns+':password'];assert N.startswith('$5$')
		if not sha256_crypt.verify(Q,N):A[E]=K;A[G]='Password mismatch for admin '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);F=utils.gen_rc_errors(_D,L);C.text=json.dumps(F,indent=2);return C
		A[E]=J;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
	async def handle_get_restconf_root(D,request):
		E=request;G=_A;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;C=B;assert C!=_K;F=utils.Encoding[C.rsplit(_L,1)[1]]
		A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert F==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		return A
	async def handle_get_yang_library_version(D,request):
		E=request;G=_A;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_M)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;C=B;assert C!=_K;F=utils.Encoding[C.rsplit(_L,1)[1]]
		A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert F==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		return A
	async def handle_get_opstate_request(C,request):
		'\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n        ';D=request;E,H=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_operational:]);A=await C._check_auth(D,E)
		if A.status==401:return A
		B,J=utils.check_http_headers(D,C.supported_media_types,accept_required=_M)
		if type(B)is web.Response:I=B;return I
		else:assert type(B)==str;F=B;assert F!=_K;K=utils.Encoding[F.rsplit(_L,1)[1]]
		A,G=await C.handle_get_opstate_request_lower_half(E,H)
		if G!=_B:A.text=json.dumps(G,indent=2)
		return A
	async def handle_get_opstate_request_lower_half(D,data_path,query_dict):
		'\n        Lower-half used by both the native and tenant view handlers.\n        Fetch and return from DB database.\n        Return object so tenant view can hack it.\n        ';B=query_dict
		async with D.fifolock(Read):
			if os.environ.get(_V)and _H in B:await asyncio.sleep(int(B[_H]))
			try:F=await D.dal.handle_get_opstate_request(data_path,B)
			except dal.NodeNotFound as C:A=web.Response(status=404);E=utils.gen_rc_errors(_D,_I,error_message=str(C));A.text=json.dumps(E,indent=2);return A,_B
			except NotImplementedError as C:A=web.Response(status=501);E=utils.gen_rc_errors(_E,_S,error_message=str(C));A.text=json.dumps(resp_text_ob,indent=2j);return A,_B
			A=web.Response(status=200);A.content_type=_c;return A,F
	async def handle_get_config_request(C,request):
		'\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n        ';D=request;E,H=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_running:]);A=await C._check_auth(D,E)
		if A.status==401:return A
		B,J=utils.check_http_headers(D,C.supported_media_types,accept_required=_M)
		if type(B)is web.Response:I=B;return I
		else:assert type(B)==str;F=B;assert F!=_K;K=utils.Encoding[F.rsplit(_L,1)[1]]
		A,G=await C.handle_get_config_request_lower_half(E,H)
		if G!=_B:A.text=json.dumps(G,indent=2)
		return A
	async def handle_get_config_request_lower_half(E,data_path,query_dict):
		'\n        Lower-half used by both the native and tenant view handlers.\n\n        Validate input.\n        Fetch and return from DB database.\n        Returns a Python object so the tenant view can hack it.\n        ';F=data_path;D=query_dict
		async with E.fifolock(Read):
			try:await E.val.handle_get_config_request(F,D)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			except val.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			if os.environ.get(_V)and _H in D:await asyncio.sleep(int(D[_H]))
			try:G=await E.dal.handle_get_config_request(F,D)
			except dal.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			A=web.Response(status=200);A.content_type=_c;return A,G
	async def handle_post_config_request(A,request):
		'\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n        ';B=request;E,H=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);F=await A._check_auth(B,E)
		if F.status==401:return F
		C,L=utils.check_http_headers(B,A.supported_media_types,accept_required=_T)
		if type(C)is web.Response:D=C;return D
		else:assert type(C)==str;G=C;assert G!=_K;M=utils.Encoding[G.rsplit(_L,1)[1]]
		try:I=await B.json()
		except json.decoder.JSONDecodeError as J:D=web.Response(status=400);K=utils.gen_rc_errors(_D,_l,error_message=_m+str(J));D.text=json.dumps(K,indent=2);return D
		return await A.handle_post_config_request_lower_half(E,H,I)
	async def handle_post_config_request_lower_half(D,data_path,query_dict,request_body):
		'\n        Lower-half used by both the native and tenant view handlers.\n\n        Validate input.\n        Commit to database (w/ inline create/change callbacks).\n        Execute post-commit logic: ref-stats, explicit_change, callbacks (separate transaction okay?).\n        ';G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write),BinaryTypePatcher():
			try:await D.val.handle_post_config_request(F,E,G)
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter,val.InvalidQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_n,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ValidationFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_S,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_E,_o,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_V)and _H in E:await asyncio.sleep(int(E[_H]))
			try:await D.dal.handle_post_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D)
			except (dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_p,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_S,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise Exception(_q+B.__class__.__name__+',  '+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic();return web.Response(status=201)
	async def handle_put_config_request(A,request):
		'\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n        ';B=request;E,H=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);F=await A._check_auth(B,E)
		if F.status==401:return F
		C,L=utils.check_http_headers(B,A.supported_media_types,accept_required=_T)
		if type(C)is web.Response:D=C;return D
		else:assert type(C)==str;G=C;assert G!=_K;M=utils.Encoding[G.rsplit(_L,1)[1]]
		try:I=await B.json()
		except json.decoder.JSONDecodeError as J:D=web.Response(status=400);K=utils.gen_rc_errors(_D,_l,error_message=_m+str(J));D.text=json.dumps(K,indent=2);return D
		return await A.handle_put_config_request_lower_half(E,H,I)
	async def handle_put_config_request_lower_half(D,data_path,query_dict,request_body):
		'\n        Lower-half used by both the native and tenant view handlers.\n\n        Validate input.\n        Commit to database (w/ inline create/change callbacks).\n        Execute post-commit logic: ref-stats, explicit_change, callbacks (separate transaction okay?).\n        ';G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write),BinaryTypePatcher():
			try:await D.val.handle_put_config_request(F,E,G)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_I,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (val.NonexistentSchemaNode,val.ValidationFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_n,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_E,_o,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_S,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_V)and _H in E:await asyncio.sleep(int(E[_H]))
			try:H=await D.dal.handle_put_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D.delete_callbacks,D)
			except (dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_p,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_S,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise Exception("why wasn't this assertion caught by val? (assuming it's a YANG validation thing)"+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic()
			if H==_M:return web.Response(status=201)
			else:return web.Response(status=204)
	async def handle_delete_config_request(A,request):
		'\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n        ';C=request;D,G=utils.parse_raw_path(C._message.path[A.len_prefix_running:]);assert G=={};E=await A._check_auth(C,D)
		if E.status==401:return E
		B,J=utils.check_http_headers(C,A.supported_media_types,accept_required=_T)
		if type(B)is web.Response:H=B;return H
		else:
			assert type(B)==str;F=B
			if F==_K:I=_B
			else:I=utils.Encoding[F.rsplit(_L,1)[1]]
		return await A.handle_delete_config_request_lower_half(D)
	async def handle_delete_config_request_lower_half(A,data_path):
		'\n        Lower-half used by both the native and tenant view handlers.\n\n        Validate input.\n        Commit to database (w/ inline create/change callbacks).\n        Execute post-commit logic: ref-stats, explicit_change, callbacks (separate transaction okay?).\n        ';E=data_path
		async with A.fifolock(Write),BinaryTypePatcher():
			try:await A.val.handle_delete_config_request(E)
			except val.NonexistentSchemaNode as C:B=web.Response(status=400);D=utils.gen_rc_errors(_E,_F,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.NodeNotFound as C:B=web.Response(status=404);D=utils.gen_rc_errors(_D,_I,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.ValidationFailed as C:B=web.Response(status=400);D=utils.gen_rc_errors(_E,_F,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			try:await A.dal.handle_delete_config_request(E,A.delete_callbacks,A.change_callbacks,A)
			except Exception as C:raise Exception(_q+str(C))
			A.val.inst=A.val.inst2;A.val.inst2=_B;await A.shared_post_commit_logic();return web.Response(status=204)
	async def shared_post_commit_logic(A):'\n          1) call subtree_change and somehow_change callbacks\n          2) update reference statistics\n        '
	async def handle_action_request(A,request):"\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n\n        No callbacks, as actions don't affect the configuration.\n        "
	async def handle_rpc_request(A,request):"\n        Following the pattern used by all the route handlers, this logic is split\n        so that the lower-half routine may be used by the tenant facade as well.\n\n        No callbacks, as rpcs don't affect the configuration.\n        ";raise NotImplementedError('Native needs an RPC handler?  - client accessible!')
	def _handle_generate_symmetric_key_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_generate_asymmetric_key_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_resend_activation_email_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_generate_certificate_signing_request_action(A,data_path,action_input):raise NotImplementedError(_W)
async def _handle_tenant_created(watched_node_path,jsob,jsob_data_path,obj):'\n    Inline edit jsob.\n\n    Tasks:\n      1. create the top-level "audit-log" opstate container\n\n    Parameters:\n      watched_node_path: the data_path for the node the callback triggered on\n      jsob:              the jsob that is about to be persisted to the database.\n                            - provided to negate the need for a DAL interaction in many cases\n                            - be careful! - this is post-VAL, so any mistakes won\'t be caught...\n      jsob_data_path:    the data_path of the node for the jsob\n      obj:               the opaque value passed into the call (nvh)\n    ';jsob['tenant']['audit-log']={'log-entry':[]}
async def _handle_transport_changed(watched_node_path,jsob,jsob_data_path,obj):'\n     send a SIGHUP signal to this process\n    ';os.kill(os.getpid(),signal.SIGHUP)
async def _handle_transport_delete(watched_node_path,opaque):"\n     The YANGSON permits this(?) - don't allow it to ever happen!\n\n     Parameters:\n        watched_node_path : the data_path to the deleted object having the schema_path\n        opaque            : the opaque object passed into the DAL's 'handle' routine (e.g., nvh)\n    ";raise NotImplementedError('Deleting the /transport node itself cannot be constrained by YANG.')
async def _handle_plugin_created(watched_node_path,jsob,jsob_data_path,opaque):
	"\n    Tasks: load module into memory\n\n    Parameters:\n      watched_node_path : the data_path for the node the callback triggered on\n      jsob              : the python object that is about to be written to the database\n      jsob_data_path    : the data_path of the above jsob object\n      opaque            : the opaque object passed into the DAL's 'handle' routine (e.g., nvh)\n    ";B=opaque;A=jsob[_U][_Q];E=re.sub(_d,'',__name__);C=E+_r+A
	if A in B.plugins:F=sys.modules[C];del sys.modules[C];del F;del B.plugins[A]
	try:G=importlib.import_module(C)
	except ModuleNotFoundError as D:raise PluginNotFound(str(D))
	except SyntaxError as D:raise PluginSyntaxError('SyntaxError: '+str(D))
	B.plugins[A]={_s:G,_R:{}}
async def _handle_plugin_deleted(watched_node_path,opaque):"\n     Parameters:\n        watched_node_path : the data_path to the deleted object having the schema_path\n        opaque            : the opaque object passed into the DAL's 'handle' routine (e.g., nvh)\n    ";C=opaque;A=re.sub(_f,_g,watched_node_path);D=re.sub(_d,'',__name__);B=D+_r+A;E=sys.modules[B];del sys.modules[B];del E;del C.plugins[A]
async def _handle_function_created(watched_node_path,jsob,jsob_data_path,opaque):
	"\n    Tasks: validate the function exists inside the module\n\n    Parameters:\n      watched_node_path : the data_path for the node the callback triggered on\n      jsob              : the python object that is about to be written to the database\n      jsob_data_path    : the data_path of the above jsob object\n      opaque            : the opaque object passed into the DAL's 'handle' routine (e.g., nvh)\n    ";B=opaque;C=re.sub(_f,_g,jsob_data_path);A=jsob[_e][_Q]
	try:D=getattr(B.plugins[C][_s],A)
	except AttributeError as E:raise FunctionNotFound(str(E))
	if not callable(D):raise FunctionNotCallable("The plugin function name '"+A+"' is not callable.")
	B.plugins[C][_R][A]=D
async def _handle_function_deleted(watched_node_path,opaque):"\n     Parameters:\n        watched_node_path : the data_path to the deleted object having the schema_path\n        opaque            : the opaque object passed into the DAL's 'handle' routine (e.g., nvh)\n    ";A=watched_node_path;B=opaque;C=re.sub(_f,_g,A);D=A.rsplit('=',1)[1];del B.plugins[C][_R][D]
async def _handle_admin_passwd_created(watched_node_path,jsob,jsob_data_path,obj):
	"\n    Inline edit jsob.\n\n    Tasks:\n      1. create the password-last-modified field\n      2. hash the password\n\n    Parameters:\n      watched_node_path: the data_path for the node the callback triggered on\n      jsob:              the jsob that is about to be persisted to the database.\n                            - provided to negate the need for a DAL interaction in many cases\n                            - be careful! - this is post-VAL, so any mistakes won't be caught...\n      jsob_data_path:    the data_path of the node for the jsob\n      obj:               the opaque value passed into the call (nvh)\n    ";A=jsob
	def B(item):
		A=item;A[_t]=datetime.datetime.utcnow().strftime(_u)
		if _J in A and A[_J].startswith('$0$'):A[_J]=sha256_crypt.using(rounds=1000).hash(A[_J][3:])
	if type(A)==dict:B(A[_v])
	else:
		assert _T;assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
async def _handle_admin_passwd_changed(watched_node_path,json,jsob_data_path,obj):
	"\n    Tasks:\n      1. update password-last-modified field (tries to use request body, otherwise (if self) uses dal.handle_put_opstate_request)\n      2. hash the password (requires access to request body)\n      3. clear any password-aging alarms for this admin-account (does NOT require access to json)\n\n    Parameters:\n      watched_node_path:    the data_path for the node the callback triggered on\n      json:         the json that is about to be persisted to the database.\n                              - provided to negate the need for a DAL interaction in many cases\n                              - be careful! - this is post-VAL, so any mistakes won't be caught...\n      jsob_data_path:    the data_path of the node for the json\n      obj:                  the opaque object passed into the DAL call\n\n    "
	def A(item):
		A=item;A[_t]=datetime.datetime.utcnow().strftime(_u)
		if _J in A and A[_J].startswith('$0$'):A[_J]=sha256_crypt.using(rounds=1000).hash(A[_J][3:])
		else:0
	assert json!=_B;assert jsob_data_path!=_B;A(json[_v])
async def _handle_ref_stat_parent_created(watched_node_path,jsob,jsob_data_path,obj):
	"\n    Tasks:\n      1. inline create the reference-statistic container (requires access to the jsob)\n\n    Parameters:\n      watched_node_path:    the data_path for the node the callback triggered on\n      jsob:                 the jsob that is about to be persisted to the database.\n                              - provided to negate the need for a DAL interaction in many cases\n                              - be careful! - this is post-VAL, so any mistakes won't be caught...\n      jsob_data_path:       the data_path of the node for the jsob\n      obj:                  the opaque object passed into the DAL call\n    ";A=jsob;assert watched_node_path==jsob_data_path
	def B(item):item['reference-statistics']={'reference-count':0,'last-referenced':'never'}
	if type(A)==dict:D=next(iter(A));B(A[D])
	else:
		raise NotImplementedError('dead code?');assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
def _handle_ref_stats_changed(leafrefed_node_data_path,obj):'\n    This code is easy, just increment/decrement the counters...\n\n    But writing the code to call this routine will be very hard!\n\n\n      obj:                  the opaque object passed into the DAL call\n    ';raise NotImplementedError('_handle_ref_stats_changed tested?')
def _handle_lingering_unreferenced_node_change(watched_node_path,obj):raise NotImplementedError(_w)
def _handle_expiring_certificate_change(watched_node_path,obj):raise NotImplementedError(_w)
async def _handle_asymmetric_public_key_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	N='Parsing private key structure failed for ';B=watched_node_path;A=jsob;O=A[_C][_h];J=base64.b64decode(O)
	if A[_C][_X]!=_x:raise dal.CreateOrChangeCallbackFailed(_y+A[_C][_X]+_Y+B.rsplit(_A,1)[0])
	try:R,G=decode_der(J,asn1Spec=rfc5280.SubjectPublicKeyInfo())
	except PyAsn1Error as C:raise dal.CreateOrChangeCallbackFailed(_z+B.rsplit(_A,1)[0]+_N+str(C)+')')
	K=serialization.load_der_public_key(J);P=A[_C][_A0];H=base64.b64decode(P)
	if A[_C][_G]==_Z:
		try:Q,G=decode_der(H,asn1Spec=rfc5915.ECPrivateKey())
		except PyAsn1Error as C:raise dal.CreateOrChangeCallbackFailed(N+B.rsplit(_A,1)[0]+_N+str(C)+')')
	elif A[_C][_G]==_a:
		try:Q,G=decode_der(H,asn1Spec=rfc3447.RSAPrivateKey())
		except PyAsn1Error as C:raise dal.CreateOrChangeCallbackFailed(N+B.rsplit(_A,1)[0]+_N+str(C)+')')
	else:raise dal.CreateOrChangeCallbackFailed(_A1+A[_C][_G]+_Y+B.rsplit(_A,1)[0])
	assert G==b'';L=serialization.load_der_private_key(H,_B,_B);E=_A2
	if A[_C][_G]==_Z:
		I=L.sign(E,ec.ECDSA(hashes.SHA256()))
		try:K.verify(I,E,ec.ECDSA(hashes.SHA256()))
		except InvalidSignature as C:raise dal.CreateOrChangeCallbackFailed(_b+B.rsplit(_A,1)[0])
	elif A[_C][_G]==_a:
		F=hashes.SHA256();I=L.sign(E,padding.PSS(mgf=padding.MGF1(F),salt_length=padding.PSS.MAX_LENGTH),F)
		try:K.verify(I,E,padding.PSS(mgf=padding.MGF1(F),salt_length=padding.PSS.MAX_LENGTH),F)
		except InvalidSignature as C:raise dal.CreateOrChangeCallbackFailed(_b+B.rsplit(_A,1)[0])
	if _O in A[_C]:
		if _P in A[_C][_O]:
			D=obj
			if D.dal.post_dal_callbacks is _B:D.dal.post_dal_callbacks=[]
			M=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,1)[0],D
			if M not in D.dal.post_dal_callbacks:D.dal.post_dal_callbacks.append(M)
async def _handle_asymmetric_private_key_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;A=jsob;N=A[_C][_A0];G=base64.b64decode(N)
	if A[_C][_G]==_Z:O,I=decode_der(G,asn1Spec=rfc5915.ECPrivateKey())
	elif A[_C][_G]==_a:O,I=decode_der(G,asn1Spec=rfc3447.RSAPrivateKey())
	else:raise dal.CreateOrChangeCallbackFailed(_A1+A[_C][_G]+_Y+B.rsplit(_A,1)[0]+_N+str(D)+')')
	J=serialization.load_der_private_key(G,_B,_B);P=A[_C][_h];K=base64.b64decode(P)
	if A[_C][_X]!=_x:raise dal.CreateOrChangeCallbackFailed(_y+A[_C][_X]+_Y+B.rsplit(_A,1)[0])
	try:Q,I=decode_der(K,asn1Spec=rfc5280.SubjectPublicKeyInfo())
	except PyAsn1Error as D:raise dal.CreateOrChangeCallbackFailed(_z+B.rsplit(_A,1)[0]+_N+str(D)+')')
	L=serialization.load_der_public_key(K);E=_A2
	if A[_C][_G]==_Z:
		H=J.sign(E,ec.ECDSA(hashes.SHA256()))
		try:L.verify(H,E,ec.ECDSA(hashes.SHA256()))
		except InvalidSignature as D:raise dal.CreateOrChangeCallbackFailed(_b+B.rsplit(_A,1)[0])
	elif A[_C][_G]==_a:
		F=hashes.SHA256();H=J.sign(E,padding.PSS(mgf=padding.MGF1(F),salt_length=padding.PSS.MAX_LENGTH),F)
		try:L.verify(H,E,padding.PSS(mgf=padding.MGF1(F),salt_length=padding.PSS.MAX_LENGTH),F)
		except InvalidSignature as D:raise dal.CreateOrChangeCallbackFailed(_b+B.rsplit(_A,1)[0])
	if _O in A[_C]:
		if _P in A[_C][_O]:
			C=obj
			if C.dal.post_dal_callbacks is _B:C.dal.post_dal_callbacks=[]
			M=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,1)[0],C
			if M not in C.dal.post_dal_callbacks:C.dal.post_dal_callbacks.append(M)
async def _handle_asymmetric_key_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;I=jsob[_P][_i];J=base64.b64decode(I);K,O=decode_der(J,asn1Spec=rfc5652.ContentInfo());L=utils.degenerate_cms_obj_to_ders(K);A=[]
	for M in L:N=x509.load_der_x509_certificate(M);A.append(N)
	E=[B for B in A if B.extensions.get_extension_for_oid(ExtensionOID.BASIC_CONSTRAINTS).value.ca==_T]
	if len(E)==0:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a certificate having "basic" constraint "ca" with value "False": '+B.rsplit(_A,1)[0])
	if len(E)>1:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode no more than one certificate having "basic" constraint "ca" with value "False" ('+str(len(E))+_A3+B.rsplit(_A,1)[0])
	G=E[0];A.remove(G);C=G
	while len(A):
		F=[B for B in A if B.subject==C.issuer]
		if len(F)==0:raise dal.CreateOrChangeCallbackFailed('End entity certificates must not encode superfluous certificates.  Found certificates unconnected to chain from the "leaf" certificate while looking for "'+str(C.subject)+_j+B.rsplit(_A,1)[0])
		if len(F)>1:raise dal.CreateOrChangeCallbackFailed('End entity certificates must not encode superfluous certificates.  CMS encodes multiple certificates having the same "subject" value ('+str(C.issuer)+'): '+B.rsplit(_A,1)[0])
		C=F[0];A.remove(C)
	D=obj
	if D.dal.post_dal_callbacks is _B:D.dal.post_dal_callbacks=[]
	H=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,3)[0],D
	if H not in D.dal.post_dal_callbacks:D.dal.post_dal_callbacks.append(H)
async def _handle_verify_asymmetric_key_and_certs_post_sweep(watched_node_path,conn,opaque):
	'\n    This routine tests the asymmetric key and any associted certs for correctness.\n    ';I='row_id';B=conn;A=watched_node_path;C=opaque;E=C.dal._get_row_data_for_list_path(A,B);F=re.sub('=[^/]*','',A);D=C.dal._get_jsob_for_row_id_in_table(F,E[I],B);J=D[_C][_h];K=base64.b64decode(J);L=serialization.load_der_public_key(K)
	if _O in D[_C]:
		if _P in D[_C][_O]:
			M=F+'/certificates/certificate';N=C.dal._find_rows_in_table_having_pid(M,E[I],{},B);G=N.fetchall();assert len(G)!=0
			for H in G:
				O=H['jsob'][_P][_i];P=base64.b64decode(O);Q,V=decode_der(P,asn1Spec=rfc5652.ContentInfo());R=utils.degenerate_cms_obj_to_ders(Q)
				for S in R:
					T=x509.load_der_x509_certificate(S);U=L.public_numbers()
					if T.public_key().public_numbers()==U:break
				else:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a "leaf" certificate having a public key matching the asymmetric key\'s public key: '+A+'/certificates/certificate='+H[_Q])
async def _handle_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;G=jsob[_P][_i];H=base64.b64decode(G)
	try:I,N=decode_der(H,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as J:raise dal.CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B.rsplit(_A,1)[0]+_N+str(J)+')')
	K=utils.degenerate_cms_obj_to_ders(I);A=[]
	for L in K:M=x509.load_der_x509_certificate(L);A.append(M)
	D=[B for B in A if B.subject==B.issuer]
	if len(D)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) certificate: '+B.rsplit(_A,1)[0])
	if len(D)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root (self-signed) certificate ('+str(len(D))+_A3+B.rsplit(_A,1)[0])
	F=D[0];A.remove(F);C=F
	while len(A):
		E=[B for B in A if B.issuer==C.subject]
		if len(E)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.  Discovered additional certificates while looking for the issuer of "'+str(C.subject)+_j+B.rsplit(_A,1)[0])
		if len(E)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+_j+B.rsplit(_A,1)[0])
		C=E[0];A.remove(C)
async def _check_expirations(nvh):0