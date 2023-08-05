import os
import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

# Base path
DATABRICKS_RUNTIME_PATH = os.path.dirname(os.path.abspath(__file__))

# Runtime metadata
DATABRICKS_RUNTIME_METADATA_PATH = os.path.join(DATABRICKS_RUNTIME_PATH, "runtime-metadata.json")
with open(DATABRICKS_RUNTIME_METADATA_PATH, "r") as file:
    DATABRICKS_RUNTIME_METADATA = json.loads(file.read())

# Runtime version
DATABRICKS_RUNTIME_VERSION = DATABRICKS_RUNTIME_METADATA["current_build"]
DATABRICKS_RUNTIME_VERSION_METADATA = DATABRICKS_RUNTIME_METADATA["supported_runtimes"][DATABRICKS_RUNTIME_VERSION]

# End of support
DATABRIKCS_RUNTIME_EOS_WARNING = os.environ.get(
    "DATABRIKCS_RUNTIME_EOS_WARNING",
    default="true"
).lower().startswith("t")

DATABRIKCS_RUNTIME_EOS_STRING = DATABRICKS_RUNTIME_VERSION_METADATA["eos_date"]
DATABRIKCS_RUNTIME_EOS_TIMESTAMP = datetime.strptime(
    DATABRIKCS_RUNTIME_EOS_STRING,
    "%Y-%m-%d"
)


def supported_runtime() -> bool:
    return datetime.utcnow() < DATABRIKCS_RUNTIME_EOS_TIMESTAMP


if DATABRIKCS_RUNTIME_EOS_WARNING and not supported_runtime():
    logger.warning(
        "You are using an outdated databricks runtime (%s with eos: %s)",
        DATABRICKS_RUNTIME_VERSION,
        DATABRIKCS_RUNTIME_EOS_STRING
    )
