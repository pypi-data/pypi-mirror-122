from .clearscreen import *
from .pressanykey import *
from .standtextout import *
from .multiprint import *
from .sanitiseinput import *

import warnings
warnings.warn("Importing turbofunc by itself is deprecated and not recommended. It will be removed in turbofunc 2.0. Run help(turbofunc) to see the possible imports.", DeprecationWarning, stacklevel=2) #https://stackoverflow.com/a/30093619/9654083
