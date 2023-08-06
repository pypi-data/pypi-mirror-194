_A='DELETE'
import logging,os.path,threading,time
from typing import Dict
from localstack.aws.api import RequestContext
from localstack.services.plugins import ServiceManager
from localstack.state import StateVisitor
from localstack.state.snapshot import SnapshotPersistencePlugin
from localstack.utils.functions import call_safe
from localstack.utils.json import FileMappedDocument
from localstack.utils.scheduler import Scheduler
from localstack.utils.sync import SynchronizedDefaultDict
from plugin import PluginManager
from ..  import constants
from .load import LoadSnapshotVisitor
from .save import SaveSnapshotVisitor
LOG=logging.getLogger(__name__)
class SnapshotManager:
	'\n    This implements the glue for making the simple disk-based persistence strategy work. It instantiates the correct\n    visitors, uses a ``ServiceManager`` to locate service plugins, and makes sure ``StateLifecycleHook``s are invoked\n    appropriately.\n    ';service_manager:0;data_dir:0;persistence_plugin_manager:0
	def __init__(A,service_manager,data_dir):B=data_dir;A.data_dir=B;A.service_manager=service_manager;A.tracker=FileMappedDocument(os.path.join(B,constants.API_STATES_JSON));A.persistence_plugin_manager=PluginManager(SnapshotPersistencePlugin.namespace)
	def load(C,service_name):
		A=service_name;D=C._create_load_state_visitor(A)
		if(B:=C.service_manager.get_service(A)):
			call_safe(B.lifecycle_hook.on_before_state_load);LOG.debug('Loading state of service %s',A)
			try:B.accept_state_visitor(D)
			except Exception:LOG.exception('Error while loading state of service %s',A);return
			call_safe(B.lifecycle_hook.on_after_state_load)
	def save(B,service_name):
		A=service_name;D=B._create_save_state_visitor(A);B.tracker[A]=time.time();B.tracker.save()
		if(C:=B.service_manager.get_service(A)):
			call_safe(C.lifecycle_hook.on_before_state_save);LOG.debug('Serializing state of service %s',A)
			try:C.accept_state_visitor(D)
			except Exception:LOG.exception('Error while serializing state of service %s',A);return
			call_safe(C.lifecycle_hook.on_after_state_save)
	def save_all(A):
		'\n        Saves the state of all loaded services.\n        '
		for B in A.service_manager.values():A.save(B.name())
	def load_all(A):
		'\n        Loads the state of all services that are found in the tracker file.\n        '
		for (B,C) in A.tracker.items():A.load(B)
	def _create_load_state_visitor(A,service_name):
		B=service_name
		if A.persistence_plugin_manager.exists(B):
			D=A.persistence_plugin_manager.load(B);C=D.create_load_snapshot_visitor(B,A.data_dir)
			if C:return C
		return LoadSnapshotVisitor(B,data_dir=A.data_dir)
	def _create_save_state_visitor(A,service_name):
		B=service_name
		if A.persistence_plugin_manager.exists(B):
			D=A.persistence_plugin_manager.load(B);C=D.create_save_snapshot_visitor(B,A.data_dir)
			if C:return C
		return SaveSnapshotVisitor(B,A.data_dir)
class SaveOnRequestHandler:
	'\n    Facilitates the "ON_REQUEST" save strategy.\n    ';state_manager:0
	def __init__(A,state_manager):A.state_manager=state_manager;A._locks=SynchronizedDefaultDict(threading.RLock)
	def on_request(B,_chain,context,_response):
		A=context
		if not A.service:return
		if A.request.method not in['POST','PUT','PATCH',_A]:return
		C=A.service.service_name;B._locks[C].acquire()
	def on_response(B,_chain,context,_response):
		A=context
		if not A.service:return
		if A.request.method not in['POST','PUT','PATCH',_A]:return
		C=A.service.service_name
		with B._locks[C]:B.state_manager.save(C)
class SaveStateScheduler:
	'\n    Saves the state on a regular basis, and facilitates the "SCHEDULED" save strategy (a compromise between ON_REQUEST\n    and ON_SHUTDOWN).\n\n    It also exposes a Handler that should be added to the handler chain, which schedules services similar to the\n    SaveOnRequestHandler.\n    ';state_manager:0;period:0
	def __init__(A,state_manager,period=30):A.state_manager=state_manager;A.scheduler=Scheduler();A.period=period;A._dirty_markers=set();A._marker_lock=threading.Lock()
	def start(A):threading.Thread(target=A.scheduler.run,daemon=True).start();A.scheduler.schedule(A._do_save,period=A.period)
	def schedule_for_save(A,service):
		'\n        Schedule the given service into the next save cycle. Call this when you think the state of a service may have\n        changed and should be flushed to disk.\n\n        :param service: the service to be stored\n        '
		with A._marker_lock:A._dirty_markers.add(service)
	def _do_save(A):
		'\n        Internal routine to perform save calls through the StateManager.\n        ';C=time.perf_counter()
		with A._marker_lock:B=list(A._dirty_markers);A._dirty_markers.clear()
		for D in B:A.state_manager.save(D)
		if B:LOG.info('Service state saved to disk in %.2f seconds',time.perf_counter()-C)
	def close(A):A.scheduler.close();A._do_save()
	def on_request_mark_service(B,_chain,context,_response):
		A=context
		if A.service is None:return
		B.schedule_for_save(A.service.service_name)