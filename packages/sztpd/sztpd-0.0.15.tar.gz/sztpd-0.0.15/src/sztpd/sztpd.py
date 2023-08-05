
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

_I='tested?'
_H='wn-sztpd-1'
_G='multi-tenant'
_F='wn-sztpd-0:device'
_E='device'
_D='single-tenant'
_C=None
_B='/'
_A='activation-code'
import gc,tracemalloc,os,re,json,base64,datetime,pkg_resources
from passlib.hash import sha256_crypt
from .yangcore import utils
from .yangcore import yangcore
from .yangcore.native import NativeViewHandler,Period,TimeUnit
from .yangcore.dal import CreateCallbackFailed,CreateOrChangeCallbackFailed
from .rfc8572 import RFC8572ViewHandler
from .  import yl
from pyasn1.codec.der.decoder import decode as decode_der
from pyasn1.error import PyAsn1Error
from pyasn1_modules import rfc5652
from cryptography import x509
from cryptography.hazmat.primitives import serialization
def sztpd_firsttime_callback():
	'\n    Prompts end-user to accept a license and prompts user to select mode,\n    since SZTPD can be run either way.\n\n    Return parameterss (per Yangcore API)\n      mode:       "single-tenant" or "multi-tenent"\n      app_ns:     the namespace for root nodes (wn-sztpd-1 or wn-sztpd-x)\n      yl_cb_func: a callback that produces the yang-library as JSON\n    ';F='Yes';B='1';C=os.environ.get('SZTPD_ACCEPT_CONTRACT')
	if C==_C:
		print('');G=pkg_resources.resource_filename('sztpd','LICENSE.txt');E=open(G,'r');print(E.read());E.close();print('First time initialization.  Please accept the license terms.');print('');print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print('');H=input('Please enter "Yes" or "No": ')
		if H!=F:print('');print('Thank you for your consideration.');print('');raise yangcore.ContractNotAccepted()
	elif C!=F:print('');print('The "SZTPD_ACCEPT_CONTRACT" environment variable is set to a value other than "Yes".  Please correct the value and try again.');print('');raise yangcore.UnrecognizedAcceptValue()
	C=os.environ.get('SZTPD_INIT_MODE')
	if C==_C:
		print('');print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print('');A=input('Please select mode: ')
		if A not in[B,'x']:print('Unknown mode selection.  Please try again.');raise yangcore.UnrecognizedModeValue()
		print('');D=_D if A==B else _G;print('Running SZTPD in "'+D+'" mode. (No more output expected)');print('')
	else:
		A=C
		if A not in[B,'x']:print('The "SZTPD_INIT_MODE" environment variable is set to an unknown value.  Must be \'1\' or \'x\'.');raise yangcore.UnrecognizedModeValue()
		D=_D if A==B else _G
	I=_H if A==B else'wn-sztpd-x';J=getattr(yl,'nbi_1'if A==B else'nbi_x');return D,I,J
def run(db_url,cacert_param=_C,cert_param=_C,key_param=_C):
	'\n    Entry point.  Isolated from command-line arg parsing logic primarily for pytests.\n\n    Args:\n      db_url:        database location specifier\n      cacert_param:  path to PEM file containing a list of X.509 certificate\n      cert_param:    path to PEM file containing the client certificate (FIXME: must be a single cert, MySQL-only?)\n      key_param:     path to PEM file containing a key for the client certificate\n\n    Returns:\n      0 on success, 1 on error\n    ';I='yang-library-func';H='/wn-sztpd-x:tenants/tenant/bootstrap-servers/bootstrap-server/trust-anchor';G='/wn-sztpd-1:bootstrap-servers/bootstrap-server/trust-anchor';B='schema_path';A='callback_func'
	try:E,C=yangcore.init(sztpd_firsttime_callback,db_url,cacert_param,cert_param,key_param)
	except Exception as F:print('yangcore.init() threw exception: '+F.__class__.__name__);print(str(F));raise F;return 1
	if C==_D:D=_B+E.app_ns+':devices/device'
	elif C==_G:D=_B+E.app_ns+':tenants/tenant/devices/device'
	else:print('Unknown mode value: "'+C+'"');return 1
	J={'wn-app:native-interface':{'create_callback':[{B:D,A:_handle_device_created},{B:G if C==_D else H,A:_handle_bss_trust_anchor_cert_created_or_changed}],'delete_callback':[{B:D,A:_handle_device_deleted}],'change_callback':[{B:D+'/activation-code',A:_handle_device_act_code_changed},{B:G if C==_D else H,A:_handle_bss_trust_anchor_cert_created_or_changed}],'subtree_change_callback':[{B:D,A:_handle_device_subtree_changed}],'somehow_change_callback':[{B:D,A:_handle_device_somehow_changed}],'periodic_callback':[{'period':Period(24,TimeUnit.Hours),'anchor':datetime.datetime(2000,1,1,0),A:_check_expirations}]},'wn-app:tenant-interface':{I:getattr(yl,'nbi_x_tenant'),'tenant-ns':_H},'wn-sztpd-0:rfc8572-interface':{'view-handler':RFC8572ViewHandler,I:getattr(yl,'sbi_rfc8572')}};yangcore.run(E,C,J);del E;return 0
async def _handle_device_created_post_sweep(watched_node_path,conn,opaque):
	"\n    This routine enables the ownership-authorization test to occur outside of the\n    DAL routine that created the device object, and possibly a device-types object,\n    which causes a lookup-miss (never understood exactly why, possibly a SQLAlchemy\n    driver thing)...\n \n    The idea now to:\n      1) the handle_device_create callback registers this callback\n      2) native's post/put/delete handling logic executes and clears callbacks *before* committing VAL (i.e., inst = inst2)\n \n    Parameters:\n      - watch_data_node: the data_path to the device that got created\n    ";g=':dynamic-callout';f='webhooks';e='verification-result';d='failure';c='tenant';b='function';a='functions';Z='plugin';Y='callback';X='ownership-authorization';O='verification-results';N='dynamic-callout';M='device-type';L='row_id';K='=[^/]*';I=watched_node_path;H='wn-sztpd-rpcs:output';B=conn;A=opaque;C=A.dal._get_row_data_for_list_path(I,B);D=re.sub(K,'',I);h=A.dal._get_jsob_for_row_id_in_table(D,C[L],B);P=_B+A.dal.app_ns+':device-types/device-type='+h[_E][M];C=A.dal._get_row_data_for_list_path(P,B);D=re.sub(K,'',P);Q=A.dal._get_jsob_for_row_id_in_table(D,C[L],B)
	if X in Q[M]:
		R=_B+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+Q[M][X][N]['reference'];C=A.dal._get_row_data_for_list_path(R,B);D=re.sub(K,'',R);E=A.dal._get_jsob_for_row_id_in_table(D,C[L],B)
		if Y in E[N]:
			F=E[N][Y];assert F[Z]in A.plugins;S=A.plugins[F[Z]];assert a in S;T=S[a];assert F[b]in T;i=T[F[b]];J=I.split(_B)
			if J[2]==c:U=J[1].split('=')[1]
			else:U='not-applicable'
			V=J[-1].split('=')[1];j={'wn-sztpd-rpcs:input':{c:U,'serial-number':[V]}};G=i(j);W=d
			if H in G:
				if O in G[H]:
					if e in G[H][O]:W=G[H][O][e][0]['result']
			if W==d:raise CreateCallbackFailed('Unable to verify ownership for device: '+V)
		else:assert f in E[A.dal.app_ns+g][0];k=E[A.dal.app_ns+g][0][f];raise NotImplementedError('webhooks for ownership verification not implemented yet')
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh):
	'\n    Notes:\n      FIXME: Code below has assertion statements that might tigger in production environments\n\n    Tasks:\n      0: call the "verify-device-ownership" callout\n      1. create the lifecycle-statistics node\n      2. create the bootstrapping-log node\n      3. hash password, if passed and not hashed already\n\n    Parameters:\n      watched_node_path:    the data_path for the node the callback triggered on\n      jsob:                 the jsob that is about to be persisted to the database.\n                              - provided to negate the need for a DAL interaction in many cases\n                              - be careful! - this is post-VAL, so any mistakes won\'t be caught...\n      jsob_data_path:       the (quasi)data_path of the node for the jsob\n      nvh:                  the *native* view handler\n\n    ';C=nvh;B=jsob;assert type(B)==dict
	if jsob_data_path==_B:assert _F in B;A=B[_F]
	else:assert _E in B;A=B[_E]
	if C.dal.post_dal_callbacks is _C:C.dal.post_dal_callbacks=[]
	C.dal.post_dal_callbacks.append((_handle_device_created_post_sweep,watched_node_path,C));A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={'log-entry':[]}
	if _A in A and A[_A].startswith('$0$'):A[_A]=sha256_crypt.using(rounds=1000).hash(A[_A][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_B:assert _F in A;B=A[_F]
	else:assert _E in A;B=A[_E]
	if _A in B and B[_A].startswith('$0$'):B[_A]=sha256_crypt.using(rounds=1000).hash(B[_A][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_I)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_I)
async def _handle_device_deleted(data_path,nvh):0
async def _handle_bss_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	G='": ';B=watched_node_path;H=jsob['bootstrap-server']['trust-anchor'];I=base64.b64decode(H)
	try:J,O=decode_der(I,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as K:raise CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B+' ('+str(K)+')')
	L=utils.degenerate_cms_obj_to_ders(J);A=[]
	for M in L:N=x509.load_der_x509_certificate(M);A.append(N)
	D=[B for B in A if B.subject==B.issuer]
	if len(D)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) certificate: '+B)
	if len(D)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root (self-signed) certificate ('+str(len(D))+' found): '+B)
	F=D[0];A.remove(F);C=F
	while len(A):
		E=[B for B in A if B.issuer==C.subject]
		if len(E)==0:raise CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.  CMS encodes additional certs not issued by the certificate "'+str(C.subject)+G+B)
		if len(E)>1:raise CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+G+B)
		C=E[0];A.remove(C)
def _check_expirations(nvh):0