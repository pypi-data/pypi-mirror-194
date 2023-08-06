_A='rds'
import os
from localstack import config
from localstack_ext.bootstrap.pods.server.plugins import StateLifecyclePlugin
RDS_DATA_ROOT=_A
class RDSPersistencePlugin(StateLifecyclePlugin):
	name=_A;service=_A
	def get_assets_location(A):return os.path.join(config.dirs.data,RDS_DATA_ROOT)
	def inject_assets(B,pod_asset_directory):from localstack_ext.services.rds.provider import restore_backend_state as A;super().inject_assets(pod_asset_directory);A()