
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_B='/ds/ietf-datastores:operational'
_A='/ds/ietf-datastores:running'
import os,ssl,json,base64,pyasn1,yangson,datetime,tempfile,basicauth
from .  import utils
from aiohttp import web
from .handler import RouteHandler
from pyasn1.type import univ
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
'\n   DESIGN\n\n   for read-only config/opstate requests:\n     - first check if user is allowed to read the node\n     - get RW-lock(READ)\n     - get operational.RW-lock(WRITE)\n     - insert a record into audit log\n     - release operational.RW-lock(WRITE)\n     - fetch node from DAL\n     - release RW-lock(READ)\n     - prune sub-nodes from result as needed\n     - return result\n\n   for read-write config requests:\n     - first check if user is allowed to write the node\n     - get running.RW-lock(WRITE)\n     - get operational.RW-lock(WRITE)\n     - insert a record into audit log\n     - release operational.RW-lock(WRITE)\n     - validate the request via VAL\n     - execute pre-persist callbacks (e.g., crypt-hash)\n     - persist the request via DAL (into <running>)\n     - spawn sub-task (see below) - should block on trying to acquire read lock\n     - release running.RW-lock(WRITE)\n     - return\n     - as a spawned subtask\n       - get running.RW-lock(READ)  // warning, there\'s a lock-gap here!\n       - execute post-persist callbacks (e.g., HUP)\n           - NOTE: "HUP" callback SHOULD be built-in!\n           - FIXME: traverse leafrefs to notify all stakeholders\n                    (e.g., addr-book obj has cascading impact)\n       - FUTURE\n          - get running.RW-lock(READ)\n          - get intended.RW-lock(WRITE)\n          - perform impact-analysis (i.e., traverse leafrefs)\n             - do minimal <running> --> <intended> transformations.\n          - persist <intended>\n          - release intended.RW-lock(WRITE)\n          - release running.RW-lock(READ)\n       - release running.RW-lock(READ)\n\n    for rpcs/actions:\n     - first check if user is allowed to write the node\n     - get RW-lock(READ)\n     - get operational.RW-lock(WRITE)\n     - insert a record into audit log\n     - release operational.RW-lock(WRITE)\n     - validate the request via VAL\n     - execute registed rpc/action callback\n        - FIXME: how can they affect <operational> !!!\n     - release RW-lock(READ)\n     - return result\n\n\n\n   FIXME: <OPERATIONAL>\n\n     - how will <operational> ever be implemented?\n     - ignore for now (just return <running>)\n\n\n\n   FIXME: OPTIMIZED SUB-TENANT ACCESS\n\n     The default RESTCONF server instance represents native yang-library (e.g., 1 vs x)\n  \n     When running multi-tenant, the default would be for sub-tenants to have to access via\n     the "/tenants/tenant[name=\'\']/..." hierarchy.  This might be okay for some, and perhaps\n     necessary for "admins" that have access to more than one sub-tenant (but are not host-\n     system admins), but a more PROFESSIONAL scenario would be to have a PROXY RC server\n     running on another PORT that presents the "single-tenant" view (inc. yang-library)\n     while actually transparently switching to the corrent sub-tenant hierarchy based on\n     which tenant the admin account is mapped to.\n  \n     This is preferable because 1) it leaks less information to sub-tenants (they don\'t\n     know that they\'re sub-tenants) and 2) the admin port can configured to only be\n     accessible from the inside network (security).\n  \n     For now, just the plain-access is being implemented, but the proxy-access should\n     be implemented later!\n\n\n'
async def set_server_header(request,response):response.headers['Server']='<redacted>'
class RestconfServer:
	root='/restconf';prefix_running=root+_A;prefix_operational=root+_B;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler):
		x='client-certs';w='local-truststore-reference';v='ca-certs';u='client-authentication';t='\n-----END CERTIFICATE-----\n';s='-----BEGIN CERTIFICATE-----\n';r='cert-data';q='private-key-format';p=':keystore/asymmetric-keys/asymmetric-key=';o='reference';n='server-identity';m='local-port';l='http';W='ASCII';V=':asymmetric-key';U=None;T='tcp-server-parameters';M='certificate';L='tls-server-parameters';K='/ds/ietf-datastores:running{tail:.*}';J='/';G=dal;D='https';C=endpoint_config;B=view_handler;A.len_prefix_running=len(A.root+_A);A.len_prefix_operational=len(A.root+_B);A.loop=loop;A.dal=G;A.name=C['name'];A.view_handler=B;A.app=web.Application(client_max_size=1024*1024*32);A.app.on_response_prepare.append(set_server_header);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,B.handle_get_restconf_root);A.app.router.add_get(A.root+J,B.handle_get_restconf_root);A.app.router.add_get(A.root+'/yang-library-version',B.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',B.handle_get_opstate_request);A.app.router.add_get(A.root+K,B.handle_get_config_request);A.app.router.add_put(A.root+K,B.handle_put_config_request);A.app.router.add_post(A.root+K,B.handle_post_config_request);A.app.router.add_delete(A.root+K,B.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',B.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',B.handle_rpc_request)
		if l in C:F=l
		else:assert D in C;F=D
		A.local_address=C[F][T]['local-address'];A.local_port=os.environ.get('SZTPD_INIT_PORT',8080)
		if m in C[F][T]:A.local_port=C[F][T][m]
		E=U
		if F==D:
			X=C[D][L][n][M][o]['asymmetric-key'];N=A.dal.handle_get_config_request(J+A.dal.app_ns+p+X);O=A.loop.run_until_complete(N);P=O[A.dal.app_ns+V][0]['cleartext-private-key'];Y=base64.b64decode(P)
			if O[A.dal.app_ns+V][0][q]=='ietf-crypto-types:ec-private-key-format':Q,y=der_decoder(Y,asn1Spec=rfc5915.ECPrivateKey());z=der_encoder(Q);Z=base64.b64encode(z).decode(W);assert P==Z;a='-----BEGIN EC PRIVATE KEY-----\n'+Z+'\n-----END EC PRIVATE KEY-----\n'
			elif O[A.dal.app_ns+V][0][q]=='ietf-crypto-types:rsa-private-key-format':Q,y=der_decoder(Y,asn1Spec=rfc3447.RSAPrivateKey());A0=der_encoder(Q);b=base64.b64encode(A0).decode(W);assert P==b;a='-----BEGIN RSA PRIVATE KEY-----\n'+b+'\n-----END RSA PRIVATE KEY-----\n'
			else:raise NotImplementedError('this line can never be reached')
			A1=C[D][L][n][M][o][M];N=A.dal.handle_get_config_request(J+A.dal.app_ns+p+X+'/certificates/certificate='+A1);A2=A.loop.run_until_complete(N);A3=A2[A.dal.app_ns+':certificate'][0][r];A4=base64.b64decode(A3);A5,c=der_decoder(A4,asn1Spec=rfc5652.ContentInfo());A6=A5.getComponentByName('content');A7,c=der_decoder(A6,asn1Spec=rfc5652.SignedData());d=A7.getComponentByName('certificates');H=''
			for A8 in range(len(d)):
				e=d[A8][0]
				for f in e['tbsCertificate']['extensions']:
					if f['extnID']==rfc5280.id_ce_basicConstraints:A9,c=der_decoder(f['extnValue'],asn1Spec=rfc5280.BasicConstraints())
				AA=der_encoder(e);g=base64.b64encode(AA).decode(W)
				if A9['cA']==False:H=s+g+t+H
				else:H+=s+g+t
			E=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);E.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as h:
				i=h+'key.pem';j=h+'certs.pem'
				with open(i,'w')as AB:AB.write(a)
				with open(j,'w')as AC:AC.write(H)
				E.load_cert_chain(j,i)
			if u in C[D][L]:
				I=C[D][L][u]
				def k(truststore_ref):
					C=G.handle_get_config_request(J+G.app_ns+':truststore/certificate-bags/certificate-bag='+truststore_ref);D=A.loop.run_until_complete(C);B=[]
					for E in D[G.app_ns+':certificate-bag'][0][M]:F=base64.b64decode(E[r]);H,I=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not I;B+=utils.degenerate_cms_obj_to_ders(H)
					return B
				R=[]
				if v in I:S=I[v][w];R+=k(S)
				if x in I:S=I[x][w];R+=k(S)
				AD=utils.der_dict_to_multipart_pem({'CERTIFICATE':R});E.load_verify_locations(cadata=AD)
		if F==D:assert not E is U
		else:assert E is U
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=E,reuse_port=True);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):'\n          no auth check, since outside restconf server.\n          no audit log entry, since outside restconf server.\n        ';A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A