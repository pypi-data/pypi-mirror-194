
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_Ab='Returning an RPC-error provided by callback (NOTE: RPC-error != exception, hence a normal exit).'
_Aa='Unrecognized error-tag: '
_AZ='partial-operation'
_AY='operation-failed'
_AX='rollback-failed'
_AW='data-exists'
_AV='resource-denied'
_AU='lock-denied'
_AT='unknown-namespace'
_AS='bad-element'
_AR='unknown-attribute'
_AQ='bad-attribute'
_AP='missing-attribute'
_AO='exception-thrown'
_AN='functions'
_AM='callback-details'
_AL='from-device'
_AK='identity-certificate'
_AJ='source-ip-address'
_AI='serial-number'
_AH='"ietf-sztp-bootstrap-server:input" is missing.'
_AG='/ietf-sztp-bootstrap-server:report-progress'
_AF='Resource does not exist.'
_AE='Requested resource does not exist.'
_AD=':log-entry'
_AC='/devices/device='
_AB=':devices/device='
_AA='2019-04-30'
_A9='urn:ietf:params:xml:ns:yang:ietf-yang-types'
_A8='ietf-yang-types'
_A7='module-set-id'
_A6='ietf-yang-library:modules-state'
_A5='application/yang-data+xml'
_A4='webhooks'
_A3='callout-type'
_A2='passed-input'
_A1='ssl_object'
_A0='access-denied'
_z='/ietf-sztp-bootstrap-server:get-bootstrapping-data'
_y='Parent node does not exist.'
_x='Resource can not be modified.'
_w='multi-tenant'
_v='2022-05-26'
_u='2013-07-15'
_t='webhook'
_s='exited-normally'
_r='opaque'
_q='function'
_p='plugin'
_o='rpc-supported'
_n='data-missing'
_m='Unable to parse "input" document: '
_l=':device'
_k='import'
_j='application/yang-data+json'
_i='operation-not-supported'
_h='Content-Type'
_g='malformed-message'
_f=False
_e=':tenants/tenant='
_d='single-tenant'
_c='implement'
_b='callback-results'
_a='callback'
_Z='invalid-value'
_Y='unknown-element'
_X=True
_W='application'
_V='path'
_U='method'
_T='source-ip'
_S='timestamp'
_R='ietf-sztp-bootstrap-server:input'
_Q='conformance-type'
_P='namespace'
_O='revision'
_N='error-tag'
_M='error'
_L='protocol'
_K='text/plain'
_J='ietf-restconf:errors'
_I=':dynamic-callout'
_H='+'
_G='name'
_F='return-code'
_E='dynamic-callout'
_D='error-returned'
_C=None
_B='event-details'
_A='/'
import os,json,base64,pprint,asyncio,aiohttp,yangson,datetime,basicauth,urllib.parse,pkg_resources
from aiohttp import web
from pyasn1.type import univ
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from .yangcore import dal
from .yangcore import utils
from .yangcore.native import Read
from .yangcore.dal import DataAccessLayer
from .yangcore.rcsvr import RestconfServer
from .yangcore.handler import RouteHandler
from .  import yl
class RFC8572ViewHandler(RouteHandler):
	'\n      Implements route handler for the SZTPD RFC 8572 facade/view.\n    ';len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43);supported_media_types=_j,_A5;yl4errors={_A6:{_A7:'TBD','module':[{_G:_A8,_O:_u,_P:_A9,_Q:_k},{_G:'ietf-restconf',_O:'2017-01-26',_P:'urn:ietf:params:xml:ns:yang:ietf-restconf',_Q:_c},{_G:'ietf-netconf-acm',_O:'2018-02-14',_P:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_Q:_k},{_G:'ietf-sztp-bootstrap-server',_O:_AA,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_Q:_c},{_G:'ietf-yang-structure-ext',_O:'2020-06-22',_P:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_Q:_c},{_G:'ietf-ztp-types',_O:_v,_P:'urn:ietf:params:xml:ns:yang:ietf-ztp-types',_Q:_c},{_G:'ietf-sztp-csr',_O:_v,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_Q:_c},{_G:'ietf-crypto-types',_O:_v,_P:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_Q:_c}]}};yl4conveyedinfo={_A6:{_A7:'TBD','module':[{_G:_A8,_O:_u,_P:_A9,_Q:_k},{_G:'ietf-inet-types',_O:_u,_P:'urn:ietf:params:xml:ns:yang:ietf-inet-types',_Q:_k},{_G:'ietf-sztp-conveyed-info',_O:_AA,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-conveyed-info',_Q:_c}]}}
	def __init__(A,dal,mode,yl,nvh):C='sztpd';A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename(C,'yang');A.dm=yangson.DataModel(yl,[B]);A.dm4conveyedinfo=yangson.DataModel(json.dumps(A.yl4conveyedinfo),[B]);D=pkg_resources.resource_filename(C,'yang4errors');A.dm4errors=yangson.DataModel(json.dumps(A.yl4errors),[D,B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_d:C=_A+A.dal.app_ns+_AB+B[0]+E
		elif A.mode==_w:C=_A+A.dal.app_ns+_e+B[1]+_AC+B[0]+E
		else:raise Exception('logic should never reach this branch')
		D={};D[A.dal.app_ns+_AD]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_d or B==_C:C=_A+A.dal.app_ns+':audit-log'
		elif A.mode==_w:C=_A+A.dal.app_ns+_e+B+'/audit-log'
		D={};D[A.dal.app_ns+_AD]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_restconf_root(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=C.remote;B[_U]=C.method;B[_V]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_H,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert I==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_yang_library_version(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=C.remote;B[_U]=C.method;B[_V]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;L=K;B[_F]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_K;I=utils.Encoding[G.rsplit(_H,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert I==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		B[_F]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_opstate_request(C,request):
		D=request;E=D.path[C.len_prefix_operational:];E=_A;G=await C._check_auth(D,E)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;F,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_X)
		if type(F)is web.Response:A=F;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(F)==str;H=F;assert H!=_K;J=utils.Encoding[H.rsplit(_H,1)[1]]
		if E=='/ietf-yang-library:yang-library'or E==_A or E=='':A=web.Response(status=200);A.content_type=_j;A.text=getattr(yl,'sbi_rfc8572')()
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_H,1)[1]];K=utils.gen_rc_errors(_L,_Y,error_message=_AE);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_get_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;J=utils.Encoding[H.rsplit(_H,1)[1]]
		if F==_A or F=='':A=web.Response(status=204)
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_H,1)[1]];K=utils.gen_rc_errors(_L,_Y,error_message=_AE);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_F]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_post_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_H,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_W,_Z,error_message=_x)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Y,error_message=_y)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_H,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_put_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_H,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_W,_Z,error_message=_x)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Y,error_message=_y)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_H,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_delete_config_request(C,request):
		D=request;G=D.path[C.len_prefix_running:];H=await C._check_auth(D,G)
		if type(H)is web.Response:A=H;return A
		else:L=H
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;E,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;N=M;B[_F]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(L,B);return A
		else:
			assert type(E)==str;I=E
			if I==_K:J=_C
			else:J=utils.Encoding[I.rsplit(_H,1)[1]]
		if G==_A or G=='':A=web.Response(status=400);F=_x;K=utils.gen_rc_errors(_W,_Z,error_message=F)
		else:A=web.Response(status=404);F=_y;K=utils.gen_rc_errors(_L,_Y,error_message=F)
		A.content_type=I
		if J is _C:A.text=F
		else:O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,O)
		B[_F]=A.status;B[_D]=K;await C._insert_bootstrapping_log_entry(L,B);return A
	async def handle_action_request(C,request):
		D=request;F=D.path[C.len_prefix_operational:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(E)is web.Response:A=E;M=L;B[_F]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_K;K=utils.Encoding[H.rsplit(_H,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_W,_Z,error_message='Resource does not support action.')
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_L,_Y,error_message=_AF)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_H,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_rpc_request(C,request):
		M='sleep';D=request;F=D.path[C.len_prefix_operations:];J=await C._check_auth(D,F)
		if type(J)is web.Response:A=J;return A
		else:E=J
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=D.remote;B[_U]=D.method;B[_V]=D.path;H,N=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if type(H)is web.Response:A=H;O=N;B[_F]=A.status;B[_D]=O;await C._insert_bootstrapping_log_entry(E,B);return A
		else:
			assert type(H)==str;K=H
			if K==_K:L=_C
			else:L=utils.Encoding[K.rsplit(_H,1)[1]]
		if F==_z:
			async with C.nvh.fifolock(Read):
				if os.environ.get('SZTPD_INIT_MODE')and M in D.query:await asyncio.sleep(int(D.query[M]))
				A=await C._handle_get_bootstrapping_data_rpc(E,D,B);B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_AG:
			try:A=await C._handle_report_progress_rpc(E,D,B)
			except NotImplementedError as Q:raise NotImplementedError('is this ever called?')
			B[_F]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_A or F=='':A=web.Response(status=400);G=_AF;I=utils.gen_rc_errors(_W,_Z,error_message=G)
		else:A=web.Response(status=404);G='Unrecognized RPC.';I=utils.gen_rc_errors(_L,_Y,error_message=G)
		A.content_type=K
		if A.content_type==_K:A.text=G
		else:I=utils.gen_rc_errors(_L,_Z,error_message=G);P=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,L,C.dm4errors,P)
		B[_F]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(E,B);return A
	async def _check_auth(A,request,data_path):
		'\n          creates/inserts audit-log entry!\n\n          returns:\n            on error: web.Response\n            success:  tuple (serial_number, tenant_name)\n        ';m='num-times-accessed';l='local-truststore-reference';k=':device-type';j='identity-certificates';i='activation-code';h='" not found for any tenant.';g='Device "';f='X-Client-Cert';V='verification';U='device-type';Q='sbi-access-stats';L='lifecycle-statistics';J='comment';I='failure';F='outcome';C=request
		def G(request,supported_media_types):
			'\n              inline func def\n            ';E=supported_media_types;D='Accept';C=request;B=web.Response(status=401)
			if D in C.headers and any((C.headers[D]==A for A in E)):B.content_type=C.headers[D]
			elif _h in C.headers and any((C.headers[_h]==A for A in E)):B.content_type=C.headers[_h]
			else:B.content_type=_K
			if B.content_type!=_K:F=utils.Encoding[B.content_type.rsplit(_H,1)[1]];G=utils.gen_rc_errors(_L,_A0);H=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(G,F,A.dm4errors,H)
			return B
		B={};B[_S]=datetime.datetime.utcnow();B[_T]=C.remote;B['source-proxies']=list(C.forwarded);B['host']=C.host;B[_U]=C.method;B[_V]=C.path;K=set();M=_C;N=C.transport.get_extra_info('peercert')
		if N is not _C:O=N['subject'][-1][0][1];K.add(O)
		elif C.headers.get(f)!=_C:n=C.headers.get(f);W=bytes(urllib.parse.unquote(n),'utf-8');M=x509.load_pem_x509_certificate(W,default_backend());o=M.subject;O=o.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;K.add(O)
		R=_C;X=_C;S=C.headers.get('AUTHORIZATION')
		if S!=_C:R,X=basicauth.decode(S);K.add(R)
		if len(K)==0:B[F]=I;B[J]='Device provided no identification credentials.';await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
		if len(K)!=1:B[F]=I;B[J]='Device provided mismatched authentication credentials ('+O+' != '+R+').';await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
		E=K.pop();D=_C
		if A.mode==_d:
			P=_A+A.dal.app_ns+_AB+E
			try:D=await A.dal.handle_get_opstate_request(P)
			except dal.NodeNotFound as Y:B[F]=I;B[J]=g+E+h;await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
			H=_C
		elif A.mode==_w:
			try:H=await A.dal.get_tenant_name_for_global_key(_A+A.dal.app_ns+':tenants/tenant/devices/device',E)
			except dal.NodeNotFound as Y:B[F]=I;B[J]=g+E+h;await A._insert_audit_log_entry(_C,B);return G(C,A.supported_media_types)
			P=_A+A.dal.app_ns+_e+H+_AC+E;D=await A.dal.handle_get_opstate_request(P)
		assert D!=_C;assert A.dal.app_ns+_l in D;D=D[A.dal.app_ns+_l][0]
		if i in D:
			if S==_C:B[F]=I;B[J]='Activation code required but none passed for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
			Z=D[i];assert Z.startswith('$5$')
			if not sha256_crypt.verify(X,Z):B[F]=I;B[J]='Activation code mismatch for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
		else:0
		assert U in D;p=_A+A.dal.app_ns+':device-types/device-type='+D[U];a=await A.dal.handle_get_opstate_request(p)
		if j in a[A.dal.app_ns+k][0]:
			if N is _C and M is _C:B[F]=I;B[J]='Client cert required but none passed for serial number '+E;await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
			if N:b=C.transport.get_extra_info(_A1);assert b is not _C;c=b.getpeercert(_X)
			else:assert M is not _C;c=W
			T=a[A.dal.app_ns+k][0][j];assert V in T;assert l in T[V];d=T[V][l];q=_A+A.dal.app_ns+':truststore/certificate-bags/certificate-bag='+d['certificate-bag']+'/certificate='+d['certificate'];r=await A.dal.handle_get_config_request(q);s=r[A.dal.app_ns+':certificate'][0]['cert-data'];t=base64.b64decode(s);u,v=der_decoder(t,asn1Spec=rfc5652.ContentInfo());assert not v;w=utils.degenerate_cms_obj_to_ders(u);x=ValidationContext(trust_roots=w);y=CertificateValidator(c,validation_context=x)
			try:y._validate_path()
			except PathBuildingError as Y:B[F]=I;B[J]="Client cert for serial number '"+E+"' does not validate using trust anchors specified by device-type '"+D[U]+"'";await A._insert_audit_log_entry(H,B);return G(C,A.supported_media_types)
		B[F]='success';await A._insert_audit_log_entry(H,B);z=P+'/lifecycle-statistics';e=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if D[L][Q][m]==0:D[L][Q]['first-accessed']=e
		D[L][Q]['last-accessed']=e;D[L][Q][m]+=1;await A.dal.handle_put_opstate_request(z,D[L]);return E,H
	async def _handle_get_bootstrapping_data_rpc(A,device_id,request,bootstrapping_log_entry):
		AP='ietf-sztp-bootstrap-server:output';AO='content';AN='contentType';AM=':configuration';AL='configuration-handling';AK='script';AJ='hash-value';AI='hash-algorithm';AH='address';AG='referenced-definition';AF='match-criteria';AE='matched-response';A6='post-configuration-script';A5='configuration';A4='pre-configuration-script';A3='os-version';A2='os-name';A1='trust-anchor';A0='port';z='bootstrap-server';y='ietf-sztp-conveyed-info:redirect-information';x='value';w='response-manager';p=device_id;o='image-verification';n='download-uri';m='boot-image';l='selected-response';h='onboarding-information';g='key';c='reference';Z=request;Y='ietf-sztp-conveyed-info:onboarding-information';X='redirect-information';L='response';J='managed-response';I='response-details';E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_entry;i,AQ=utils.check_http_headers(Z,A.supported_media_types,accept_required=_X)
		if type(i)is web.Response:B=i;AR=AQ;C[_F]=B.status;C[_D]=AR;return B
		else:assert type(i)==str;O=i;assert O!=_K;S=utils.Encoding[O.rsplit(_H,1)[1]]
		M=_C
		if Z.body_exists:
			AS=await Z.text();AT=utils.Encoding[Z.headers[_h].rsplit(_H,1)[1]]
			try:G=A.dm.get_schema_node(_z);M=utils.encoded_str_to_obj(AS,AT,A.dm,G)
			except Exception as a:B=web.Response(status=400);q=_m+str(a);B.content_type=O;H=utils.gen_rc_errors(_L,_g,error_message=q);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
			if not _R in M:
				B=web.Response(status=400)
				if not _R in M:q=_m+_AH
				B.content_type=O;H=utils.gen_rc_errors(_L,_g,error_message=q);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
		C[_B]={};C[_B][E]={}
		if M is _C:C[_B][E][_A2]={'no-input-passed':[_C]}
		else:C[_B][E][_A2]=M[_R]
		if A.mode==_d:Q=_A+A.dal.app_ns+':'
		else:Q=_A+A.dal.app_ns+_e+p[1]+_A
		AU=Q+'devices/device='+p[0]
		try:V=await A.dal.handle_get_config_request(AU)
		except Exception as a:B=web.Response(status=501);B.content_type=_j;H=utils.gen_rc_errors(_W,_i,error_message='Unhandled exception: '+str(a));B.text=utils.enc_rc_errors('json',H);return B
		assert V!=_C;assert A.dal.app_ns+_l in V;V=V[A.dal.app_ns+_l][0]
		if w not in V or AE not in V[w]:B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_W,_n,error_message='No responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;C[_B][E][l]='no-responses-configured';return B
		F=_C
		for j in V[w][AE]:
			if not AF in j:F=j;break
			if M is _C:continue
			for P in j[AF]['match']:
				if P[g]not in M[_R]:break
				if'present'in P:
					if'not'in P:
						if P[g]in M[_R]:break
					elif P[g]not in M[_R]:break
				elif x in P:
					if'not'in P:
						if P[x]==M[_R][P[g]]:break
					elif P[x]!=M[_R][P[g]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:F=j;break
		if F is _C or'none'in F[L]:
			if F is _C:C[_B][E][l]='no-match-found'
			else:C[_B][E][l]=F[_G]+" (explicit 'none')"
			B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_W,_n,error_message='No matching responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
		C[_B][E][l]=F[_G];C[_B][E][I]={J:{}}
		if D in F[L]:
			C[_B][E][I][J]={D:{}};N={}
			if _E in F[L][D]:
				C[_B][E][I][J][D]={_E:{}};assert c in F[L][D][_E];r=F[L][D][_E][c];C[_B][E][I][J][D][_E][_G]=r;R=await A.dal.handle_get_config_request(Q+'dynamic-callouts/dynamic-callout='+r);assert r==R[A.dal.app_ns+_I][0][_G];C[_B][E][I][J][D][_E][_o]=R[A.dal.app_ns+_I][0][_o];d={};d[_AI]=p[0];d[_AJ]=Z.remote;A7=Z.transport.get_extra_info(_A1)
				if A7:
					A8=A7.getpeercert(_X)
					if A8:d[_AK]=A8
				if M:d[_AL]=M
				if _a in R[A.dal.app_ns+_I][0]:
					C[_B][E][I][J][D][_E][_A3]=_a;A9=R[A.dal.app_ns+_I][0][_a][_p];AA=R[A.dal.app_ns+_I][0][_a][_q];C[_B][E][I][J][D][_E][_AM]={_p:A9,_q:AA};C[_B][E][I][J][D][_E][_b]={}
					if _r in R[A.dal.app_ns+_I][0]:AB=R[A.dal.app_ns+_I][0][_r]
					else:AB=_C
					K=_C
					try:K=A.nvh.plugins[A9][_AN][AA](d,AB)
					except Exception as a:C[_B][E][I][J][D][_E][_b][_AO]=str(a);B=web.Response(status=500);B.content_type=O;H=utils.gen_rc_errors(_W,_i,error_message='Server encountered an error while trying to generate a response: '+str(a));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
					assert K and type(K)==dict
					if _J in K:
						assert len(K[_J][_M])==1
						if any((A==K[_J][_M][0][_N]for A in(_Z,'too-big',_AP,_AQ,_AR,_AS,_Y,_AT,_g))):B=web.Response(status=400)
						elif any((A==K[_J][_M][0][_N]for A in _A0)):B=web.Response(status=403)
						elif any((A==K[_J][_M][0][_N]for A in('in-use',_AU,_AV,_AW,_n))):B=web.Response(status=409)
						elif any((A==K[_J][_M][0][_N]for A in(_AX,_AY,_AZ))):B=web.Response(status=500)
						elif any((A==K[_J][_M][0][_N]for A in _i)):B=web.Response(status=501)
						else:raise NotImplementedError(_Aa+K[_J][_M][0][_N])
						B.content_type=O;H=K;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=K;C[_B][E][I][J][D][_E][_b][_s]=_Ab;return B
					else:C[_B][E][I][J][D][_E][_b][_s]='Returning conveyed information provided by callback.'
				elif _A4 in R[A.dal.app_ns+_I][0]:C[_B][E][I][J][D][_E][_A3]=_t;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(R[A.dal.app_ns+_I][0]))
				N=K
			elif X in F[L][D]:
				C[_B][E][I][J][D]={X:{}};N[y]={};N[y][z]=[]
				if c in F[L][D][X]:
					e=F[L][D][X][c];C[_B][E][I][J][D][X]={AG:e};s=await A.dal.handle_get_config_request(Q+'conveyed-information-responses/redirect-information-response='+e)
					for AV in s[A.dal.app_ns+':redirect-information-response'][0][X][z]:
						W=await A.dal.handle_get_config_request(Q+'bootstrap-servers/bootstrap-server='+AV);W=W[A.dal.app_ns+':bootstrap-server'][0];k={};k[AH]=W[AH]
						if A0 in W:k[A0]=W[A0]
						if A1 in W:k[A1]=W[A1]
						N[y][z].append(k)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(F[L][D][X]))
			elif h in F[L][D]:
				C[_B][E][I][J][D]={};N[Y]={}
				if c in F[L][D][h]:
					e=F[L][D][h][c];C[_B][E][I][J][D][h]={AG:e};s=await A.dal.handle_get_config_request(Q+'conveyed-information-responses/onboarding-information-response='+e);T=s[A.dal.app_ns+':onboarding-information-response'][0][h]
					if m in T:
						AW=T[m];AX=await A.dal.handle_get_config_request(Q+'boot-images/boot-image='+AW);U=AX[A.dal.app_ns+':boot-image'][0];N[Y][m]={};b=N[Y][m]
						if A2 in U:b[A2]=U[A2]
						if A3 in U:b[A3]=U[A3]
						if n in U:
							b[n]=list()
							for AY in U[n]:b[n].append(AY)
						if o in U:
							b[o]=list()
							for AC in U[o]:t={};t[AI]=AC[AI];t[AJ]=AC[AJ];b[o].append(t)
					if A4 in T:AZ=T[A4];Aa=await A.dal.handle_get_config_request(Q+'scripts/pre-configuration-script='+AZ);N[Y][A4]=Aa[A.dal.app_ns+':pre-configuration-script'][0][AK]
					if A5 in T:Ab=T[A5];AD=await A.dal.handle_get_config_request(Q+'configurations/configuration='+Ab);N[Y][AL]=AD[A.dal.app_ns+AM][0][AL];N[Y][A5]=AD[A.dal.app_ns+AM][0]['config']
					if A6 in T:Ac=T[A6];Ad=await A.dal.handle_get_config_request(Q+'scripts/post-configuration-script='+Ac);N[Y][A6]=Ad[A.dal.app_ns+':post-configuration-script'][0][AK]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(F[L][D]))
		else:raise NotImplementedError('unhandled response type: '+str(F[L]))
		f=rfc5652.ContentInfo()
		if O==_j:f[AN]=A.id_ct_sztpConveyedInfoJSON;f[AO]=encode_der(json.dumps(N,indent=2),asn1Spec=univ.OctetString())
		else:assert O==_A5;f[AN]=A.id_ct_sztpConveyedInfoXML;G=A.dm4conveyedinfo.get_schema_node(_A);assert G;Ae=utils.obj_to_encoded_str(N,S,A.dm4conveyedinfo,G,strip_wrapper=_X);f[AO]=encode_der(Ae,asn1Spec=univ.OctetString())
		Af=encode_der(f,rfc5652.ContentInfo());u=base64.b64encode(Af).decode('ASCII');Ag=base64.b64decode(u);Ah=base64.b64encode(Ag).decode('ASCII');assert u==Ah;v={};v[AP]={};v[AP][D]=u;B=web.Response(status=200);B.content_type=O;G=A.dm.get_schema_node(_z);B.text=utils.obj_to_encoded_str(v,S,A.dm,G);return B
	async def _handle_report_progress_rpc(B,device_id,request,bootstrapping_log_entry):
		g='remote-port';f='webhook-results';Y='tcp-client-parameters';X='encoding';W=device_id;V='http';L=request;E='report-progress-event';C=bootstrapping_log_entry;S,h=utils.check_http_headers(L,B.supported_media_types,accept_required=_f)
		if type(S)is web.Response:A=S;i=h;C[_F]=A.status;C[_D]=i;return A
		else:assert type(S)==str;J=S
		if J!=_K:N=utils.Encoding[J.rsplit(_H,1)[1]]
		if not L.body_exists:
			M='RPC "input" node missing (required for "report-progress").';A=web.Response(status=400);A.content_type=J
			if A.content_type==_K:A.text=M
			else:F=utils.gen_rc_errors(_L,_Z,error_message=M);G=B.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(F,N,B.dm4errors,G)
			C[_D]=A.text;return A
		j=utils.Encoding[L.headers[_h].rsplit(_H,1)[1]];k=await L.text()
		try:G=B.dm.get_schema_node(_AG);O=utils.encoded_str_to_obj(k,j,B.dm,G)
		except Exception as K:A=web.Response(status=400);M=_m+str(K);A.content_type=J;F=utils.gen_rc_errors(_L,_g,error_message=M);G=B.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(F,N,B.dm4errors,G);C[_D]=F;return A
		if not _R in O:
			A=web.Response(status=400)
			if not _R in O:M=_m+_AH
			A.content_type=J;F=utils.gen_rc_errors(_L,_g,error_message=M);G=B.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(F,N,B.dm4errors,G);C[_D]=F;return A
		C[_B]={};C[_B][E]={};C[_B][E][_A2]=O[_R];C[_B][E][_E]={}
		if B.mode==_d:P=_A+B.dal.app_ns+':preferences/outbound-interactions/relay-progress-report-callout'
		else:P=_A+B.dal.app_ns+_e+W[1]+'/preferences/outbound-interactions/relay-progress-report-callout'
		try:l=await B.dal.handle_get_config_request(P)
		except Exception as K:C[_B][E][_E]['no-callout-configured']=[_C]
		else:
			T=l[B.dal.app_ns+':relay-progress-report-callout'];C[_B][E][_E][_G]=T
			if B.mode==_d:P=_A+B.dal.app_ns+':dynamic-callouts/dynamic-callout='+T
			else:P=_A+B.dal.app_ns+_e+W[1]+'/dynamic-callouts/dynamic-callout='+T
			H=await B.dal.handle_get_config_request(P);assert T==H[B.dal.app_ns+_I][0][_G];C[_B][E][_E][_o]=H[B.dal.app_ns+_I][0][_o];Q={};Q[_AI]=W[0];Q[_AJ]=L.remote;Z=L.transport.get_extra_info(_A1)
			if Z:
				a=Z.getpeercert(_X)
				if a:Q[_AK]=a
			if O:Q[_AL]=O
			if _a in H[B.dal.app_ns+_I][0]:
				C[_B][E][_E][_A3]=_a;b=H[B.dal.app_ns+_I][0][_a][_p];c=H[B.dal.app_ns+_I][0][_a][_q];C[_B][E][_E][_AM]={_p:b,_q:c};C[_B][E][_E][_b]={}
				if _r in H[B.dal.app_ns+_I][0]:d=H[B.dal.app_ns+_I][0][_r]
				else:d=_C
				D=_C
				try:D=B.nvh.plugins[b][_AN][c](Q,d)
				except Exception as K:C[_B][E][_E][_b][_AO]=str(K);A=web.Response(status=500);A.content_type=J;F=utils.gen_rc_errors(_W,_i,error_message='Server encountered an error while trying to process the progress report: '+str(K));G=B.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(F,N,B.dm4errors,G);C[_D]=F;return A
				if D:
					assert type(D)==dict;assert len(D)==1;assert _J in D;assert len(D[_J][_M])==1
					if any((A==D[_J][_M][0][_N]for A in(_Z,'too-big',_AP,_AQ,_AR,_AS,_Y,_AT,_g))):A=web.Response(status=400)
					elif any((A==D[_J][_M][0][_N]for A in _A0)):A=web.Response(status=403)
					elif any((A==D[_J][_M][0][_N]for A in('in-use',_AU,_AV,_AW,_n))):A=web.Response(status=409)
					elif any((A==D[_J][_M][0][_N]for A in(_AX,_AY,_AZ))):A=web.Response(status=500)
					elif any((A==D[_J][_M][0][_N]for A in _i)):A=web.Response(status=501)
					else:raise NotImplementedError(_Aa+D[_J][_M][0][_N])
					A.content_type=J;F=D;G=B.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(F,N,B.dm4errors,G);C[_D]=D;C[_B][E][_E][_b][_s]=_Ab;return A
				else:C[_B][E][_E][_b][_s]='Callback returned no output (normal)'
			elif _A4 in H[B.dal.app_ns+_I][0]:
				C[_B][E][_E][f]={_t:[]}
				for I in H[B.dal.app_ns+_I][0][_A4][_t]:
					R={};R[_G]=I[_G]
					if X not in I or I[X]=='json':e=rpc_input_json
					elif I[X]=='xml':e=rpc_input_xml
					if V in I:
						U='http://'+I[V][Y]['remote-address']
						if g in I[V][Y]:U+=':'+str(I[V][Y][g])
						U+='/relay-notification';R['uri']=U
						try:
							async with aiohttp.ClientSession()as m:A=await m.post(U,data=e)
						except aiohttp.client_exceptions.ClientConnectorError as K:R['connection-error']=str(K)
						else:
							R['http-status-code']=A.status
							if A.status==200:break
					else:assert'https'in I;raise NotImplementedError('https-based webhook is not supported yet.')
					C[_B][E][_E][f][_t].append(R)
			else:raise NotImplementedError('unrecognized callout type '+str(H[B.dal.app_ns+_I][0]))
		A=web.Response(status=204);return A