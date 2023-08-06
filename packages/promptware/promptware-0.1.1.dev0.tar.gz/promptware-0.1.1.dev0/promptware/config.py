import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

os_api_key = os.getenv("OS_API_KEY")
eb_api_key = os.getenv("EB_API_KEY")
eb_username = os.getenv("EB_USERNAME")


# Version
SCRIPTS_VERSION = "main"
HUB_DEFAULT_VERSION = "main"

# Hub
EP_ENDPOINT = os.environ.get("EP_ENDPOINT", "http://expressai.co")
HUB_SOFTWARE_URL = (
    "https://raw.githubusercontent.com/expressai/data/{revision}"
    "/softwares/{path}/{name}"
)


# Cache location
DEFAULT_XDG_CACHE_HOME = "~/.cache"
XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)
# "~/.cache/expressai"
DEFAULT_EP_CACHE_HOME = os.path.join(XDG_CACHE_HOME, "expressai")
EP_CACHE_HOME = os.path.expanduser(os.getenv("EP_HOME", DEFAULT_EP_CACHE_HOME))


# "~/.cache/expressai/software"
DEFAULT_EP_SOFTWARE_CACHE = os.path.join(EP_CACHE_HOME, "software")
EP_SOFTWARE_CACHE = Path(os.getenv("EP_SOFTWARE_CACHE", DEFAULT_EP_SOFTWARE_CACHE))


# "~/.cache/expressai/modules"
DEFAULT_EP_MODULES_CACHE = os.path.join(EP_CACHE_HOME, "modules")
EP_MODULES_CACHE = Path(os.getenv("EP_MODULES_CACHE", DEFAULT_EP_MODULES_CACHE))

# "~/.cache/expressai/software/downloads"
DOWNLOADED_DATASETS_DIR = "downloads"
DEFAULT_DOWNLOADED_SOFTWARE_PATH = os.path.join(
    EP_SOFTWARE_CACHE, DOWNLOADED_DATASETS_DIR
)
DOWNLOADED_SOFTWARE_PATH = Path(
    os.getenv("EP_DATASETS_DOWNLOADED_SOFTWARE_PATH", DEFAULT_DOWNLOADED_SOFTWARE_PATH)
)


# "~/.cache/expressai/software/downloads/extracted"
EXTRACTED_SOFTWARE_DIR = "extracted"
DEFAULT_EXTRACTED_SOFTWARE_PATH = os.path.join(
    DEFAULT_DOWNLOADED_SOFTWARE_PATH, EXTRACTED_SOFTWARE_DIR
)
EXTRACTED_SOFTWARE_PATH = Path(
    os.getenv("EP_DATASETS_EXTRACTED_SOFTWARE_PATH", DEFAULT_EXTRACTED_SOFTWARE_PATH)
)


# File names
LICENSE_FILENAME = "LICENSE"
MODULE_NAME_FOR_DYNAMIC_MODULES = "software_modules"
SOFTWARE_INFO_FILENAME = "software_info.json"


# General environment variables accepted values for booleans
ENV_VARS_TRUE_VALUES = {"1", "ON", "YES", "TRUE"}
ENV_VARS_TRUE_AND_AUTO_VALUES = ENV_VARS_TRUE_VALUES.union({"AUTO"})

# Offline mode
EP_SOFTWARE_OFFLINE = (
    os.environ.get("EP_SOFTWARE_OFFLINE", "AUTO").upper() in ENV_VARS_TRUE_VALUES
)
