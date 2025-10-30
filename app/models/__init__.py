"""Models module initialization"""

# Import basic types
from .basic_types import (
    DomainName as DomainName,
    SingleIpv6Addr as SingleIpv6Addr,
    EdgeCloudZoneStatus as EdgeCloudZoneStatus,
    EdgeCloudZoneId as EdgeCloudZoneId,
    EdgeCloudRegion as EdgeCloudRegion,
    EdgeCloudProvider as EdgeCloudProvider,
    EdgeCloudZoneName as EdgeCloudZoneName,
    ApplicationEndpointListId as ApplicationEndpointListId,
    ApplicationProfileId as ApplicationProfileId,
    EdgeCloudZone as EdgeCloudZone,
)


# Import application models
from .application_endpoint import (
    ApplicationEndpoint as ApplicationEndpoint,
    ApplicationEndpointsInfo as ApplicationEndpointsInfo,
)

# Import types from CamaraCommon for convenience
from CamaraCommon.Network import Port as Port, SingleIpv4Addr as SingleIpv4Addr
from CamaraCommon.Basic import XCorrelator as XCorrelator
from CamaraCommon.Error import ErrorInfo as ErrorInfo
