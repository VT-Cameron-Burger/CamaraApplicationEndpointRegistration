"""Models module initialization"""

# Import basic types
from CamaraCommon.Basic import XCorrelator as XCorrelator
from CamaraCommon.Error import ErrorInfo as ErrorInfo

# Import types from CamaraCommon for convenience
from CamaraCommon.Network import Port as Port
from CamaraCommon.Network import SingleIpv4Addr as SingleIpv4Addr

# Import application models
from .application_endpoint import ApplicationEndpoint as ApplicationEndpoint
from .application_endpoint import ApplicationEndpointsInfo as ApplicationEndpointsInfo
from .basic_types import ApplicationEndpointListId as ApplicationEndpointListId
from .basic_types import ApplicationProfileId as ApplicationProfileId
from .basic_types import DomainName as DomainName
from .basic_types import EdgeCloudProvider as EdgeCloudProvider
from .basic_types import EdgeCloudRegion as EdgeCloudRegion
from .basic_types import EdgeCloudZone as EdgeCloudZone
from .basic_types import EdgeCloudZoneId as EdgeCloudZoneId
from .basic_types import EdgeCloudZoneName as EdgeCloudZoneName
from .basic_types import EdgeCloudZoneStatus as EdgeCloudZoneStatus
from .basic_types import SingleIpv6Addr as SingleIpv6Addr
