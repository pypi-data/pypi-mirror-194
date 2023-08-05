
# Copyright (c) 2023 Watsen Networks.  All Rights Reserved.

_A=None
import os,json,signal,asyncio,functools
from .dal import DataAccessLayer,AuthenticationFailed
from .rcsvr import RestconfServer
from .tenant import TenantViewHandler
from .native import NativeViewHandler
class ContractNotAccepted(Exception):0
class UnrecognizedAcceptValue(Exception):0
class UnrecognizedModeValue(Exception):0
loop=_A
sig=_A
nvh=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def init(firsttime_cb_func,db_url,cacert_param=_A,cert_param=_A,key_param=_A):
	'\n    Entry point.  Isolated from command-line arg parsing logic primarily for pytests.\n\n    Args:\n      db_url:        database location specifier\n      cacert_param:  path to PEM file containing a list of X.509 certificate\n      cert_param:    path to PEM file containing the client certificate (FIXME: must be a single cert, MySQL-only?)\n      key_param:     path to PEM file containing a key for the client certificate\n\n    Returns:\n      dal:  DataAccessLayer\n      mode: "single-tenant" or "multi-tenant"\n    ';F=db_url;D=key_param;C=cert_param;B=cacert_param
	if B is not _A and F.startswith('sqlite:'):raise Exception('The "sqlite" dialect does not support the "cacert" parameter.')
	if(C or D)and not B:raise Exception('The "cacert" parameter must be specified whenever the "key" and "cert" parameters are specified.')
	if(C is _A)!=(D is _A):raise Exception('The "key" and "cert" parameters must be specified together.')
	H=False
	try:G=DataAccessLayer(F,B,C,D)
	except (SyntaxError,AssertionError,AuthenticationFailed)as A:raise A
	except NotImplementedError as A:H=True
	if H==True:
		try:I,K,L=firsttime_cb_func()
		except Exception as A:raise A
		try:G=DataAccessLayer(F,B,C,D,json.loads(L()),K)
		except Exception as A:raise A
		E=os.environ.get('SZTPD_INIT_PORT')
		if E!=_A:
			try:J=int(E)
			except ValueError as A:raise ValueError('Invalid "SZTPD_INIT_PORT" value ('+E+').')
			if J<=0 or J>2**16-1:raise ValueError('The "SZTPD_INIT_PORT" value ('+E+') is out of range [1..65535].')
		assert G!=_A;assert I!=_A;return G,I
def run(dal,mode,endpoint_settings):
	'\n    Entry point for yangcore\'s "forever" loop.\n    ';e='yang-library-func';d='periodic_callback';c='somehow_change_callback';b='subtree_change_callback';a='change_callback';Z='delete_callback';Y='create_callback';X='wn-app:native-interface';W=':transport';V='SIGHUP';P='wn-app:tenant-interface';K='use-for';I='schema_path';G='callback_func';F=endpoint_settings;C=dal;global loop;global sig;global nvh;loop=asyncio.new_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=V));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		J=[];E=C.handle_get_config_request('/'+C.app_ns+W);L=loop.run_until_complete(E)
		for B in L[C.app_ns+W]['listen']['endpoint']:
			if B[K]==X:
				D=NativeViewHandler(C,mode,loop);nvh=D;A=F[X]
				if Y in A:
					for Q in A[Y]:D.register_create_callback(Q[I],Q[G])
				if Z in A:
					for R in A[Z]:D.register_delete_callback(R[I],R[G])
				if a in A:
					for S in A[a]:D.register_change_callback(S[I],S[G])
				if b in A:
					for T in A[b]:D.register_subtree_change_callback(T[I],T[G])
				if c in A:
					for U in A[c]:D.register_somehow_change_callback(U[I],U[G])
				if d in A:
					for M in A[d]:D.register_periodic_callback(M['period'],M['anchor'],M[G])
				N=RestconfServer(loop,C,B,D)
			elif B[K]==P:f=TenantViewHandler(nvh,F[P][e],F[P]['tenant-ns']);N=RestconfServer(loop,C,B,f)
			else:
				O=B[K]
				if O not in F:raise KeyError('Error: support for the configured endpoint "use-for" interface "'+O+'" was not supplied in the "endpoint_settings" parameter in the yangcore.run() method.')
				g=F[O]['view-handler'];h=g(C,mode,F[B[K]][e](),nvh);N=RestconfServer(loop,C,B,h)
			J.append(N);del B;B=_A
		del L;L=_A;loop.run_forever()
		for H in J:E=H.app.shutdown();loop.run_until_complete(E);E=H.runner.cleanup();loop.run_until_complete(E);E=H.app.cleanup();loop.run_until_complete(E);del H;H=_A
		del J;J=_A
		if sig==V:sig=_A
	loop.close()