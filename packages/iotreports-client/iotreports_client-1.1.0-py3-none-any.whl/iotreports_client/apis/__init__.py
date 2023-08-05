
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.category_api import CategoryApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from iotreports_client.api.category_api import CategoryApi
from iotreports_client.api.organization_api import OrganizationApi
from iotreports_client.api.permissions_api import PermissionsApi
from iotreports_client.api.report_api import ReportApi
from iotreports_client.api.report_type_api import ReportTypeApi
from iotreports_client.api.user_api import UserApi
