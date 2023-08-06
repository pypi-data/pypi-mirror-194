from ._version import get_versions

from .oauth import OAuth
from .oauth_manager import OAuthManager
from .base_client import BaseClient
from .client import Client
from .utils import load_oauth_configuration, load_configuration, load_zoho_configuration, read_json_file, \
    demand_configuration

from .resources import *

from .aws import *

__version__ = get_versions()['version']
del get_versions
