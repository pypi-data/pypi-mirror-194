import logging,zipfile
from localstack.services.plugins import ServiceManager
from localstack.utils.functions import call_safe
from .load import CloudPodArchive,InjectPodVisitor
from .save import CreatePodVisitor
LOG=logging.getLogger(__name__)
class PodStateManager:
	service_manager:0
	def __init__(A,service_manager):A.service_manager=service_manager
	def extract_into(B,pod_archive,service_names=None):
		'\n        Extracts the state of the currently running localstack instance and writes it into the given cloudpod.\n        :param pod_archive: the cloudpod archive to write to\n        ';C=service_names;D=CreatePodVisitor(pod_archive);E=B.service_manager.values()if not C else[B.service_manager.get_service(A)for A in C]
		for A in E:
			call_safe(A.lifecycle_hook.on_before_state_save);LOG.debug('Saving state of service %s into pod',A.name())
			try:A.accept_state_visitor(D)
			except Exception:LOG.exception('Error while saving state of service %s into pod',A.name());return
			call_safe(A.lifecycle_hook.on_after_state_save)
	def inject(D,pod_archive):
		'\n        Injects the given cloudpod into the currently running LocalStack instance.\n\n        :param pod_archive: the cloudpod archive to read from\n        ';C=pod_archive;E=CloudPodArchive(C);F=InjectPodVisitor(C)
		for A in E.services:
			if(B:=D.service_manager.get_service(A)):
				call_safe(B.lifecycle_hook.on_before_state_load);LOG.debug('Injecting state of service %s from pod',A)
				try:B.accept_state_visitor(F)
				except Exception:LOG.exception('Error while injecting state of service %s from pod',A);return
				call_safe(B.lifecycle_hook.on_after_state_load)