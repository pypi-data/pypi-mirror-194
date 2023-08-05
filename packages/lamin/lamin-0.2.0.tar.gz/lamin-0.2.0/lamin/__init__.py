__version__ = "0.2.0"  # denote a pre-release for 0.1.0 with 0.1rc1
import lndb as _lndb
from lndb import *

from . import dev

__doc__ = _lndb.__doc__.replace("lndb", "lamin")
