from jetpack.redis import redis

__version__ = "0.5.1-dev20211010"

from jetpack._job.interface import job
from jetpack._remote.interface import remote
from jetpack.cli import handle as init
