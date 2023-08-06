import logging
from localstack import config
from localstack.runtime import hooks,shutdown
from localstack.utils.objects import singleton_factory
from .api import SaveStrategy
LOG=logging.getLogger(__name__)
@singleton_factory
def get_save_strategy():
	from .config import SAVE_STRATEGY as A
	try:
		if A:return SaveStrategy(A)
	except ValueError as B:LOG.warning('Invalid save strategy, falling back to on_shutdown: %s',B)
	return SaveStrategy.ON_SHUTDOWN
@singleton_factory
def get_service_state_manager():from localstack import config as A;from localstack.services.plugins import SERVICE_PLUGINS as B;from .manager import SnapshotManager as C;return C(B,A.dirs.data)
@hooks.on_infra_start(should_load=config.PERSISTENCE)
def register_state_resource():from localstack.services.internal import get_internal_apis as A;from .endpoints import StateResource as B;C=B(get_service_state_manager());A().add(C)
@hooks.on_infra_start(should_load=config.PERSISTENCE)
def do_restore_snapshot():get_service_state_manager().load_all()
@hooks.on_infra_start(should_load=config.PERSISTENCE)
def register_state_save_strategy():
	from localstack.aws.handlers import run_custom_response_handlers as G,serve_custom_service_request_handlers as C;from .api import SaveStrategy as A;from .manager import SaveOnRequestHandler as H,SaveStateScheduler as I;D=get_save_strategy();E=get_service_state_manager()
	match D:
		case A.ON_SHUTDOWN:LOG.info('registering ON_SHUTDOWN persistence strategy');shutdown.SHUTDOWN_HANDLERS.register(E.save_all)
		case A.ON_REQUEST:LOG.info('registering ON_REQUEST persistence strategy');F=H(get_service_state_manager());C.append(F.on_request);G.append(F.on_response)
		case A.SCHEDULED:LOG.info('registering SCHEDULED persistence strategy');B=I(E,period=15);shutdown.SHUTDOWN_HANDLERS.register(B.close);C.append(B.on_request_mark_service);B.start()
		case _:LOG.warning('Unknown save strategy %s',D)