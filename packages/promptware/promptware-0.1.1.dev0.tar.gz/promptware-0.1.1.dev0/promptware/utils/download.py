import enum

from promptware.utils.logging import get_logger

logger = get_logger(__name__)


class DownloadMode(enum.Enum):
    """`Enum` for how to treat pre-existing downloads and data.
    The default mode is `REUSE_DATASET_IF_EXISTS`, which will reuse both
    raw downloads and the prepared dataset if they exist.
    The generations modes:
    |                                     | Downloads | Dataset |
    |-------------------------------------|-----------|---------|
    | `REUSE_DATASET_IF_EXISTS` (default) | Reuse     | Reuse   |
    | `REUSE_CACHE_IF_EXISTS`             | Reuse     | Fresh   |
    | `FORCE_REDOWNLOAD`                  | Fresh     | Fresh   |
    """

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    REUSE_CACHE_IF_EXISTS = "reuse_cache_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"
