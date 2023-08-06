import logging,os.path,zipfile
from collections import defaultdict
from functools import cached_property,singledispatchmethod
from typing import Any,List,Tuple
from localstack import config
from localstack.services.stores import AccountRegionBundle
from localstack.state import AssetDirectory,Decoder,StateVisitor,pickle
from moto.core import BackendDict
from localstack_persistence import constants
LOG=logging.getLogger(__name__)
class InjectPodVisitor(StateVisitor):
	zip:0
	def __init__(A,zip_file,decoder=None):A.zip=zip_file;A.pod=CloudPodArchive(A.zip);A.decoder=decoder or pickle.PickleDecoder()
	@singledispatchmethod
	def visit(self,state_container):LOG.warning('cannot save state container of type %s',type(state_container))
	@visit.register(AccountRegionBundle)
	def _(self,state_container):
		B=state_container;A=self;C=B.service_name
		if C not in A.pod.stores_index:return
		for (D,E,F) in A.pod.stores_index[C]:
			with A.zip.open(F)as G:H=A.decoder.decode(G);B[D][E].__dict__.update(H.__dict__)
	@visit.register(BackendDict)
	def _(self,state_container):
		B=state_container;A=self;C=B.service_name
		if C not in A.pod.stores_index:return
		for (D,E,F) in A.pod.moto_backend_index[C]:
			with A.zip.open(F)as G:H=A.decoder.decode(G);B[D][E].__dict__.update(H.__dict__)
	@visit.register(AssetDirectory)
	def _(self,state_container):
		A=state_container
		if not A.path.startswith(config.dirs.data):return
		C=os.path.relpath(A.path,config.dirs.data)+'/';B=[A for A in self.zip.namelist()if A.startswith(C)]
		if B:self.zip.extractall(config.dirs.data,B)
class CloudPodArchive:
	zip:0
	def __init__(A,zip_file):A.zip=zip_file
	@cached_property
	def services(self):'\n        Returns the list of services that have state in this cloud pod.\n        ';A=set();A.update(self.stores_index.keys());A.update(self.moto_backend_index.keys());return A
	@cached_property
	def stores_index(self):
		'\n        Creates from the list of zip items an index that makes it easy to look up all account-region-store triples for a\n        given service.\n        ';D=self.zip.namelist();B=defaultdict(list)
		for C in D:
			A=C.lstrip('/')
			if not A.startswith(constants.API_STATES_DIRECTORY):continue
			if not A.endswith(constants.LOCALSTACK_STORE_STATE_FILE):continue
			E,F,G=A.split('/')[1:4];B[F].append((E,G,C))
		return B
	@cached_property
	def moto_backend_index(self):
		D=self.zip.namelist();B=defaultdict(list)
		for C in D:
			A=C.lstrip('/')
			if not A.startswith(constants.API_STATES_DIRECTORY):continue
			if not A.endswith(constants.MOTO_BACKEND_STATE_FILE):continue
			E,F,G=A.split('/')[1:4];B[F].append((E,G,C))
		return B