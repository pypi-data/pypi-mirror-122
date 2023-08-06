# Allow use of TA_ env vars instead of HT_
from hypertrace import env_var_settings

from traceableai.agent import Agent

env_var_settings.ENV_VAR_PREFIXES.append('TA')

# This will initialize the hypertrace instrumentation
a = Agent()
import hypertrace.agent.autoinstrumentation.sitecustomize # pylint:disable=C0413,W0611,C0411


from traceableai.config.config import Config  # pylint:disable=C0413,C0412

from hypertrace.agent.custom_logger import get_custom_logger  # pylint:disable=C0413,C0412,C0411

config = Config()
logger = get_custom_logger(__name__)
if config.config.blocking_config.enabled.value is True:
    a.add_traceable_filter()
else:
    logger.info("Not adding traceableai blocking module")
