from decouple import config
from .base import *

if config('ENVIRONMENT') == "PRODUCTION":
    from .prod import *

elif config('ENVIRONMENT') == 'STAGING':
    from .staging import *

elif config('ENVIRONMENT') == 'GITHUB_WORKFLOW':
    from .test import *

else:
    from .dev import *