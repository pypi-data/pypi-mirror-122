import distro

# These imports have to be first to respect TA_ env vars in hypertrace agent
from hypertrace import env_var_settings
env_var_settings.ENV_VAR_PREFIXES.append('TA')

from hypertrace import agent  # pylint:disable=C0413
from hypertrace.agent.filter.registry import Registry # pylint:disable=C0413
from hypertrace.agent.custom_logger import get_custom_logger # pylint:disable=C0413
from hypertrace.agent import constants # pylint:disable=C0413

from traceableai.filter.traceable import Traceable, _BLOCKING_AVAILABLE  # pylint:disable=C0413
from traceableai.version import __version__ # pylint:disable=C0413

logger = get_custom_logger(__name__)



# We need to override the version that is reported to the platform from hypertrace
constants.TELEMETRY_SDK_VERSION = __version__

class Agent(agent.Agent):
    def __init__(self):
        super().__init__()
        logger.debug("Platform: %s", distro.id())
        logger.debug("Platform version: %s", distro.version())
        logger.debug('TraceableAI Agent version: %s', __version__)
        logger.debug("successfully initialized traceableai agent")


    def add_traceable_filter(self):  #pylint:disable=R0201
        logger.debug("in add_traceable_filter")
        if distro.id() == 'alpine':
            logger.info('blocking unavailable on alpine linux, skipping filter registration')
            return
        if not _BLOCKING_AVAILABLE:
            logger.info("blocking unavailable, skipping filter registration")
            return
        try:
            Registry().register(Traceable)
            logger.debug("successfully initialized traceable filter")
        except: # pylint:disable=W0702
            logger.info("failed to register traceable blocking filter")
