"""
Type annotations for rds service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_rds import RDSClient

    client: RDSClient = boto3.client("rds")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ActivityStreamModeType,
    DBProxyEndpointTargetRoleType,
    EngineFamilyType,
    ReplicaModeType,
    SourceTypeType,
)
from .paginator import (
    DescribeCertificatesPaginator,
    DescribeCustomAvailabilityZonesPaginator,
    DescribeDBClusterBacktracksPaginator,
    DescribeDBClusterEndpointsPaginator,
    DescribeDBClusterParameterGroupsPaginator,
    DescribeDBClusterParametersPaginator,
    DescribeDBClusterSnapshotsPaginator,
    DescribeDBClustersPaginator,
    DescribeDBEngineVersionsPaginator,
    DescribeDBInstanceAutomatedBackupsPaginator,
    DescribeDBInstancesPaginator,
    DescribeDBLogFilesPaginator,
    DescribeDBParameterGroupsPaginator,
    DescribeDBParametersPaginator,
    DescribeDBProxiesPaginator,
    DescribeDBProxyEndpointsPaginator,
    DescribeDBProxyTargetGroupsPaginator,
    DescribeDBProxyTargetsPaginator,
    DescribeDBSecurityGroupsPaginator,
    DescribeDBSnapshotsPaginator,
    DescribeDBSubnetGroupsPaginator,
    DescribeEngineDefaultClusterParametersPaginator,
    DescribeEngineDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeExportTasksPaginator,
    DescribeGlobalClustersPaginator,
    DescribeInstallationMediaPaginator,
    DescribeOptionGroupOptionsPaginator,
    DescribeOptionGroupsPaginator,
    DescribeOrderableDBInstanceOptionsPaginator,
    DescribePendingMaintenanceActionsPaginator,
    DescribeReservedDBInstancesOfferingsPaginator,
    DescribeReservedDBInstancesPaginator,
    DescribeSourceRegionsPaginator,
    DownloadDBLogFilePortionPaginator,
)
from .type_defs import (
    AccountAttributesMessageTypeDef,
    AddSourceIdentifierToSubscriptionResultTypeDef,
    ApplyPendingMaintenanceActionResultTypeDef,
    AuthorizeDBSecurityGroupIngressResultTypeDef,
    CertificateMessageTypeDef,
    CloudwatchLogsExportConfigurationTypeDef,
    ConnectionPoolConfigurationTypeDef,
    CopyDBClusterParameterGroupResultTypeDef,
    CopyDBClusterSnapshotResultTypeDef,
    CopyDBParameterGroupResultTypeDef,
    CopyDBSnapshotResultTypeDef,
    CopyOptionGroupResultTypeDef,
    CreateCustomAvailabilityZoneResultTypeDef,
    CreateDBClusterParameterGroupResultTypeDef,
    CreateDBClusterResultTypeDef,
    CreateDBClusterSnapshotResultTypeDef,
    CreateDBInstanceReadReplicaResultTypeDef,
    CreateDBInstanceResultTypeDef,
    CreateDBParameterGroupResultTypeDef,
    CreateDBProxyEndpointResponseTypeDef,
    CreateDBProxyResponseTypeDef,
    CreateDBSecurityGroupResultTypeDef,
    CreateDBSnapshotResultTypeDef,
    CreateDBSubnetGroupResultTypeDef,
    CreateEventSubscriptionResultTypeDef,
    CreateGlobalClusterResultTypeDef,
    CreateOptionGroupResultTypeDef,
    CustomAvailabilityZoneMessageTypeDef,
    DBClusterBacktrackMessageTypeDef,
    DBClusterBacktrackResponseMetadataTypeDef,
    DBClusterCapacityInfoTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterEndpointResponseMetadataTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupNameMessageTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceAutomatedBackupMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupNameMessageTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSecurityGroupMessageTypeDef,
    DBSnapshotMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DeleteCustomAvailabilityZoneResultTypeDef,
    DeleteDBClusterResultTypeDef,
    DeleteDBClusterSnapshotResultTypeDef,
    DeleteDBInstanceAutomatedBackupResultTypeDef,
    DeleteDBInstanceResultTypeDef,
    DeleteDBProxyEndpointResponseTypeDef,
    DeleteDBProxyResponseTypeDef,
    DeleteDBSnapshotResultTypeDef,
    DeleteEventSubscriptionResultTypeDef,
    DeleteGlobalClusterResultTypeDef,
    DescribeDBClusterSnapshotAttributesResultTypeDef,
    DescribeDBLogFilesResponseTypeDef,
    DescribeDBProxiesResponseTypeDef,
    DescribeDBProxyEndpointsResponseTypeDef,
    DescribeDBProxyTargetGroupsResponseTypeDef,
    DescribeDBProxyTargetsResponseTypeDef,
    DescribeDBSnapshotAttributesResultTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeValidDBInstanceModificationsResultTypeDef,
    DownloadDBLogFilePortionDetailsTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    ExportTaskResponseMetadataTypeDef,
    ExportTasksMessageTypeDef,
    FailoverDBClusterResultTypeDef,
    FailoverGlobalClusterResultTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    InstallationMediaMessageTypeDef,
    InstallationMediaResponseMetadataTypeDef,
    ModifyCertificatesResultTypeDef,
    ModifyDBClusterResultTypeDef,
    ModifyDBClusterSnapshotAttributeResultTypeDef,
    ModifyDBInstanceResultTypeDef,
    ModifyDBProxyEndpointResponseTypeDef,
    ModifyDBProxyResponseTypeDef,
    ModifyDBProxyTargetGroupResponseTypeDef,
    ModifyDBSnapshotAttributeResultTypeDef,
    ModifyDBSnapshotResultTypeDef,
    ModifyDBSubnetGroupResultTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    ModifyGlobalClusterResultTypeDef,
    ModifyOptionGroupResultTypeDef,
    OptionConfigurationTypeDef,
    OptionGroupOptionsMessageTypeDef,
    OptionGroupsTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    ParameterTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    ProcessorFeatureTypeDef,
    PromoteReadReplicaDBClusterResultTypeDef,
    PromoteReadReplicaResultTypeDef,
    PurchaseReservedDBInstancesOfferingResultTypeDef,
    RebootDBInstanceResultTypeDef,
    RegisterDBProxyTargetsResponseTypeDef,
    RemoveFromGlobalClusterResultTypeDef,
    RemoveSourceIdentifierFromSubscriptionResultTypeDef,
    ReservedDBInstanceMessageTypeDef,
    ReservedDBInstancesOfferingMessageTypeDef,
    RestoreDBClusterFromS3ResultTypeDef,
    RestoreDBClusterFromSnapshotResultTypeDef,
    RestoreDBClusterToPointInTimeResultTypeDef,
    RestoreDBInstanceFromDBSnapshotResultTypeDef,
    RestoreDBInstanceFromS3ResultTypeDef,
    RestoreDBInstanceToPointInTimeResultTypeDef,
    RevokeDBSecurityGroupIngressResultTypeDef,
    ScalingConfigurationTypeDef,
    SourceRegionMessageTypeDef,
    StartActivityStreamResponseTypeDef,
    StartDBClusterResultTypeDef,
    StartDBInstanceAutomatedBackupsReplicationResultTypeDef,
    StartDBInstanceResultTypeDef,
    StopActivityStreamResponseTypeDef,
    StopDBClusterResultTypeDef,
    StopDBInstanceAutomatedBackupsReplicationResultTypeDef,
    StopDBInstanceResultTypeDef,
    TagListMessageTypeDef,
    TagTypeDef,
    UserAuthConfigTypeDef,
)
from .waiter import (
    DBClusterSnapshotAvailableWaiter,
    DBClusterSnapshotDeletedWaiter,
    DBInstanceAvailableWaiter,
    DBInstanceDeletedWaiter,
    DBSnapshotAvailableWaiter,
    DBSnapshotCompletedWaiter,
    DBSnapshotDeletedWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("RDSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    AuthorizationQuotaExceededFault: Type[BotocoreClientError]
    BackupPolicyNotFoundFault: Type[BotocoreClientError]
    CertificateNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CustomAvailabilityZoneAlreadyExistsFault: Type[BotocoreClientError]
    CustomAvailabilityZoneNotFoundFault: Type[BotocoreClientError]
    CustomAvailabilityZoneQuotaExceededFault: Type[BotocoreClientError]
    DBClusterAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterBacktrackNotFoundFault: Type[BotocoreClientError]
    DBClusterEndpointAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterEndpointNotFoundFault: Type[BotocoreClientError]
    DBClusterEndpointQuotaExceededFault: Type[BotocoreClientError]
    DBClusterNotFoundFault: Type[BotocoreClientError]
    DBClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBClusterQuotaExceededFault: Type[BotocoreClientError]
    DBClusterRoleAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterRoleNotFoundFault: Type[BotocoreClientError]
    DBClusterRoleQuotaExceededFault: Type[BotocoreClientError]
    DBClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    DBInstanceAlreadyExistsFault: Type[BotocoreClientError]
    DBInstanceAutomatedBackupNotFoundFault: Type[BotocoreClientError]
    DBInstanceAutomatedBackupQuotaExceededFault: Type[BotocoreClientError]
    DBInstanceNotFoundFault: Type[BotocoreClientError]
    DBInstanceRoleAlreadyExistsFault: Type[BotocoreClientError]
    DBInstanceRoleNotFoundFault: Type[BotocoreClientError]
    DBInstanceRoleQuotaExceededFault: Type[BotocoreClientError]
    DBLogFileNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    DBProxyAlreadyExistsFault: Type[BotocoreClientError]
    DBProxyEndpointAlreadyExistsFault: Type[BotocoreClientError]
    DBProxyEndpointNotFoundFault: Type[BotocoreClientError]
    DBProxyEndpointQuotaExceededFault: Type[BotocoreClientError]
    DBProxyNotFoundFault: Type[BotocoreClientError]
    DBProxyQuotaExceededFault: Type[BotocoreClientError]
    DBProxyTargetAlreadyRegisteredFault: Type[BotocoreClientError]
    DBProxyTargetGroupNotFoundFault: Type[BotocoreClientError]
    DBProxyTargetNotFoundFault: Type[BotocoreClientError]
    DBSecurityGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBSecurityGroupNotFoundFault: Type[BotocoreClientError]
    DBSecurityGroupNotSupportedFault: Type[BotocoreClientError]
    DBSecurityGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBSnapshotNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    DBSubnetGroupNotAllowedFault: Type[BotocoreClientError]
    DBSubnetGroupNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSubnetQuotaExceededFault: Type[BotocoreClientError]
    DBUpgradeDependencyFailureFault: Type[BotocoreClientError]
    DomainNotFoundFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    ExportTaskAlreadyExistsFault: Type[BotocoreClientError]
    ExportTaskNotFoundFault: Type[BotocoreClientError]
    GlobalClusterAlreadyExistsFault: Type[BotocoreClientError]
    GlobalClusterNotFoundFault: Type[BotocoreClientError]
    GlobalClusterQuotaExceededFault: Type[BotocoreClientError]
    IamRoleMissingPermissionsFault: Type[BotocoreClientError]
    IamRoleNotFoundFault: Type[BotocoreClientError]
    InstallationMediaAlreadyExistsFault: Type[BotocoreClientError]
    InstallationMediaNotFoundFault: Type[BotocoreClientError]
    InstanceQuotaExceededFault: Type[BotocoreClientError]
    InsufficientAvailableIPsInSubnetFault: Type[BotocoreClientError]
    InsufficientDBClusterCapacityFault: Type[BotocoreClientError]
    InsufficientDBInstanceCapacityFault: Type[BotocoreClientError]
    InsufficientStorageClusterCapacityFault: Type[BotocoreClientError]
    InvalidDBClusterCapacityFault: Type[BotocoreClientError]
    InvalidDBClusterEndpointStateFault: Type[BotocoreClientError]
    InvalidDBClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBClusterStateFault: Type[BotocoreClientError]
    InvalidDBInstanceAutomatedBackupStateFault: Type[BotocoreClientError]
    InvalidDBInstanceStateFault: Type[BotocoreClientError]
    InvalidDBParameterGroupStateFault: Type[BotocoreClientError]
    InvalidDBProxyEndpointStateFault: Type[BotocoreClientError]
    InvalidDBProxyStateFault: Type[BotocoreClientError]
    InvalidDBSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidDBSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBSubnetGroupFault: Type[BotocoreClientError]
    InvalidDBSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidDBSubnetStateFault: Type[BotocoreClientError]
    InvalidEventSubscriptionStateFault: Type[BotocoreClientError]
    InvalidExportOnlyFault: Type[BotocoreClientError]
    InvalidExportSourceStateFault: Type[BotocoreClientError]
    InvalidExportTaskStateFault: Type[BotocoreClientError]
    InvalidGlobalClusterStateFault: Type[BotocoreClientError]
    InvalidOptionGroupStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidS3BucketFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    OptionGroupAlreadyExistsFault: Type[BotocoreClientError]
    OptionGroupNotFoundFault: Type[BotocoreClientError]
    OptionGroupQuotaExceededFault: Type[BotocoreClientError]
    PointInTimeRestoreNotEnabledFault: Type[BotocoreClientError]
    ProvisionedIopsNotAvailableInAZFault: Type[BotocoreClientError]
    ReservedDBInstanceAlreadyExistsFault: Type[BotocoreClientError]
    ReservedDBInstanceNotFoundFault: Type[BotocoreClientError]
    ReservedDBInstanceQuotaExceededFault: Type[BotocoreClientError]
    ReservedDBInstancesOfferingNotFoundFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    SharedSnapshotQuotaExceededFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    StorageTypeNotSupportedFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]


class RDSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RDSClient exceptions.
        """

    def add_role_to_db_cluster(
        self, *, DBClusterIdentifier: str, RoleArn: str, FeatureName: str = ...
    ) -> None:
        """
        Associates an Identity and Access Management (IAM) role from an Amazon Aurora DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.add_role_to_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#add_role_to_db_cluster)
        """

    def add_role_to_db_instance(
        self, *, DBInstanceIdentifier: str, RoleArn: str, FeatureName: str
    ) -> None:
        """
        Associates an Amazon Web Services Identity and Access Management (IAM) role with
        a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.add_role_to_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#add_role_to_db_instance)
        """

    def add_source_identifier_to_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> AddSourceIdentifierToSubscriptionResultTypeDef:
        """
        Adds a source identifier to an existing RDS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.add_source_identifier_to_subscription)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#add_source_identifier_to_subscription)
        """

    def add_tags_to_resource(self, *, ResourceName: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds metadata tags to an Amazon RDS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.add_tags_to_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#add_tags_to_resource)
        """

    def apply_pending_maintenance_action(
        self, *, ResourceIdentifier: str, ApplyAction: str, OptInType: str
    ) -> ApplyPendingMaintenanceActionResultTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to a DB
        instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.apply_pending_maintenance_action)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#apply_pending_maintenance_action)
        """

    def authorize_db_security_group_ingress(
        self,
        *,
        DBSecurityGroupName: str,
        CIDRIP: str = ...,
        EC2SecurityGroupName: str = ...,
        EC2SecurityGroupId: str = ...,
        EC2SecurityGroupOwnerId: str = ...
    ) -> AuthorizeDBSecurityGroupIngressResultTypeDef:
        """
        Enables ingress to a DBSecurityGroup using one of two forms of authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.authorize_db_security_group_ingress)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#authorize_db_security_group_ingress)
        """

    def backtrack_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        BacktrackTo: Union[datetime, str],
        Force: bool = ...,
        UseEarliestTimeOnPointInTimeUnavailable: bool = ...
    ) -> DBClusterBacktrackResponseMetadataTypeDef:
        """
        Backtracks a DB cluster to a specific time, without creating a new DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.backtrack_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#backtrack_db_cluster)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#can_paginate)
        """

    def cancel_export_task(self, *, ExportTaskIdentifier: str) -> ExportTaskResponseMetadataTypeDef:
        """
        Cancels an export task in progress that is exporting a snapshot to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.cancel_export_task)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#cancel_export_task)
        """

    def copy_db_cluster_parameter_group(
        self,
        *,
        SourceDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyDBClusterParameterGroupResultTypeDef:
        """
        Copies the specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.copy_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#copy_db_cluster_parameter_group)
        """

    def copy_db_cluster_snapshot(
        self,
        *,
        SourceDBClusterSnapshotIdentifier: str,
        TargetDBClusterSnapshotIdentifier: str,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        CopyTags: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        SourceRegion: str = ...
    ) -> CopyDBClusterSnapshotResultTypeDef:
        """
        Copies a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.copy_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#copy_db_cluster_snapshot)
        """

    def copy_db_parameter_group(
        self,
        *,
        SourceDBParameterGroupIdentifier: str,
        TargetDBParameterGroupIdentifier: str,
        TargetDBParameterGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyDBParameterGroupResultTypeDef:
        """
        Copies the specified DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.copy_db_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#copy_db_parameter_group)
        """

    def copy_db_snapshot(
        self,
        *,
        SourceDBSnapshotIdentifier: str,
        TargetDBSnapshotIdentifier: str,
        KmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        CopyTags: bool = ...,
        PreSignedUrl: str = ...,
        OptionGroupName: str = ...,
        TargetCustomAvailabilityZone: str = ...,
        SourceRegion: str = ...
    ) -> CopyDBSnapshotResultTypeDef:
        """
        Copies the specified DB snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.copy_db_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#copy_db_snapshot)
        """

    def copy_option_group(
        self,
        *,
        SourceOptionGroupIdentifier: str,
        TargetOptionGroupIdentifier: str,
        TargetOptionGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyOptionGroupResultTypeDef:
        """
        Copies the specified option group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.copy_option_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#copy_option_group)
        """

    def create_custom_availability_zone(
        self,
        *,
        CustomAvailabilityZoneName: str,
        ExistingVpnId: str = ...,
        NewVpnTunnelName: str = ...,
        VpnTunnelOriginatorIP: str = ...
    ) -> CreateCustomAvailabilityZoneResultTypeDef:
        """
        Creates a custom Availability Zone (AZ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_custom_availability_zone)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_custom_availability_zone)
        """

    def create_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        BackupRetentionPeriod: int = ...,
        CharacterSetName: str = ...,
        DatabaseName: str = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        DBSubnetGroupName: str = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        OptionGroupName: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        ReplicationSourceIdentifier: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        BacktrackWindow: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        EngineMode: str = ...,
        ScalingConfiguration: "ScalingConfigurationTypeDef" = ...,
        DeletionProtection: bool = ...,
        GlobalClusterIdentifier: str = ...,
        EnableHttpEndpoint: bool = ...,
        CopyTagsToSnapshot: bool = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...,
        EnableGlobalWriteForwarding: bool = ...,
        SourceRegion: str = ...
    ) -> CreateDBClusterResultTypeDef:
        """
        Creates a new Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_cluster)
        """

    def create_db_cluster_endpoint(
        self,
        *,
        DBClusterIdentifier: str,
        DBClusterEndpointIdentifier: str,
        EndpointType: str,
        StaticMembers: Sequence[str] = ...,
        ExcludedMembers: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> DBClusterEndpointResponseMetadataTypeDef:
        """
        Creates a new custom endpoint and associates it with an Amazon Aurora DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_cluster_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_cluster_endpoint)
        """

    def create_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        DBParameterGroupFamily: str,
        Description: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBClusterParameterGroupResultTypeDef:
        """
        Creates a new DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_cluster_parameter_group)
        """

    def create_db_cluster_snapshot(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        DBClusterIdentifier: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBClusterSnapshotResultTypeDef:
        """
        Creates a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_cluster_snapshot)
        """

    def create_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        DBInstanceClass: str,
        Engine: str,
        DBName: str = ...,
        AllocatedStorage: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        DBSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        AvailabilityZone: str = ...,
        DBSubnetGroupName: str = ...,
        PreferredMaintenanceWindow: str = ...,
        DBParameterGroupName: str = ...,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...,
        Port: int = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        CharacterSetName: str = ...,
        NcharCharacterSetName: str = ...,
        PubliclyAccessible: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DBClusterIdentifier: str = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        Domain: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        MonitoringRoleArn: str = ...,
        DomainIAMRoleName: str = ...,
        PromotionTier: int = ...,
        Timezone: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        PerformanceInsightsRetentionPeriod: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        DeletionProtection: bool = ...,
        MaxAllocatedStorage: int = ...,
        EnableCustomerOwnedIp: bool = ...
    ) -> CreateDBInstanceResultTypeDef:
        """
        Creates a new DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_instance)
        """

    def create_db_instance_read_replica(
        self,
        *,
        DBInstanceIdentifier: str,
        SourceDBInstanceIdentifier: str,
        DBInstanceClass: str = ...,
        AvailabilityZone: str = ...,
        Port: int = ...,
        MultiAZ: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        DBParameterGroupName: str = ...,
        PubliclyAccessible: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DBSubnetGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        StorageType: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        MonitoringRoleArn: str = ...,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        PerformanceInsightsRetentionPeriod: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        UseDefaultProcessorFeatures: bool = ...,
        DeletionProtection: bool = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...,
        ReplicaMode: ReplicaModeType = ...,
        MaxAllocatedStorage: int = ...,
        SourceRegion: str = ...
    ) -> CreateDBInstanceReadReplicaResultTypeDef:
        """
        Creates a new DB instance that acts as a read replica for an existing source DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_instance_read_replica)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_instance_read_replica)
        """

    def create_db_parameter_group(
        self,
        *,
        DBParameterGroupName: str,
        DBParameterGroupFamily: str,
        Description: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBParameterGroupResultTypeDef:
        """
        Creates a new DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_parameter_group)
        """

    def create_db_proxy(
        self,
        *,
        DBProxyName: str,
        EngineFamily: EngineFamilyType,
        Auth: Sequence["UserAuthConfigTypeDef"],
        RoleArn: str,
        VpcSubnetIds: Sequence[str],
        VpcSecurityGroupIds: Sequence[str] = ...,
        RequireTLS: bool = ...,
        IdleClientTimeout: int = ...,
        DebugLogging: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBProxyResponseTypeDef:
        """
        Creates a new DB proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_proxy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_proxy)
        """

    def create_db_proxy_endpoint(
        self,
        *,
        DBProxyName: str,
        DBProxyEndpointName: str,
        VpcSubnetIds: Sequence[str],
        VpcSecurityGroupIds: Sequence[str] = ...,
        TargetRole: DBProxyEndpointTargetRoleType = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBProxyEndpointResponseTypeDef:
        """
        Creates a `DBProxyEndpoint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_proxy_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_proxy_endpoint)
        """

    def create_db_security_group(
        self,
        *,
        DBSecurityGroupName: str,
        DBSecurityGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBSecurityGroupResultTypeDef:
        """
        Creates a new DB security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_security_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_security_group)
        """

    def create_db_snapshot(
        self,
        *,
        DBSnapshotIdentifier: str,
        DBInstanceIdentifier: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBSnapshotResultTypeDef:
        """
        Creates a snapshot of a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_snapshot)
        """

    def create_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        DBSubnetGroupDescription: str,
        SubnetIds: Sequence[str],
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBSubnetGroupResultTypeDef:
        """
        Creates a new DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_db_subnet_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_db_subnet_group)
        """

    def create_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        SourceIds: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an RDS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_event_subscription)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_event_subscription)
        """

    def create_global_cluster(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        SourceDBClusterIdentifier: str = ...,
        Engine: str = ...,
        EngineVersion: str = ...,
        DeletionProtection: bool = ...,
        DatabaseName: str = ...,
        StorageEncrypted: bool = ...
    ) -> CreateGlobalClusterResultTypeDef:
        """
        Creates an Aurora global database spread across multiple Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_global_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_global_cluster)
        """

    def create_option_group(
        self,
        *,
        OptionGroupName: str,
        EngineName: str,
        MajorEngineVersion: str,
        OptionGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateOptionGroupResultTypeDef:
        """
        Creates a new option group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.create_option_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#create_option_group)
        """

    def delete_custom_availability_zone(
        self, *, CustomAvailabilityZoneId: str
    ) -> DeleteCustomAvailabilityZoneResultTypeDef:
        """
        Deletes a custom Availability Zone (AZ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_custom_availability_zone)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_custom_availability_zone)
        """

    def delete_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        SkipFinalSnapshot: bool = ...,
        FinalDBSnapshotIdentifier: str = ...
    ) -> DeleteDBClusterResultTypeDef:
        """
        The DeleteDBCluster action deletes a previously provisioned DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_cluster)
        """

    def delete_db_cluster_endpoint(
        self, *, DBClusterEndpointIdentifier: str
    ) -> DBClusterEndpointResponseMetadataTypeDef:
        """
        Deletes a custom endpoint and removes it from an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_cluster_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_cluster_endpoint)
        """

    def delete_db_cluster_parameter_group(self, *, DBClusterParameterGroupName: str) -> None:
        """
        Deletes a specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_cluster_parameter_group)
        """

    def delete_db_cluster_snapshot(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DeleteDBClusterSnapshotResultTypeDef:
        """
        Deletes a DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_cluster_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_cluster_snapshot)
        """

    def delete_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        SkipFinalSnapshot: bool = ...,
        FinalDBSnapshotIdentifier: str = ...,
        DeleteAutomatedBackups: bool = ...
    ) -> DeleteDBInstanceResultTypeDef:
        """
        The DeleteDBInstance action deletes a previously provisioned DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_instance)
        """

    def delete_db_instance_automated_backup(
        self, *, DbiResourceId: str = ..., DBInstanceAutomatedBackupsArn: str = ...
    ) -> DeleteDBInstanceAutomatedBackupResultTypeDef:
        """
        Deletes automated backups using the `DbiResourceId` value of the source DB
        instance or the Amazon Resource Name (ARN) of the automated backups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_instance_automated_backup)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_instance_automated_backup)
        """

    def delete_db_parameter_group(self, *, DBParameterGroupName: str) -> None:
        """
        Deletes a specified DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_parameter_group)
        """

    def delete_db_proxy(self, *, DBProxyName: str) -> DeleteDBProxyResponseTypeDef:
        """
        Deletes an existing DB proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_proxy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_proxy)
        """

    def delete_db_proxy_endpoint(
        self, *, DBProxyEndpointName: str
    ) -> DeleteDBProxyEndpointResponseTypeDef:
        """
        Deletes a `DBProxyEndpoint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_proxy_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_proxy_endpoint)
        """

    def delete_db_security_group(self, *, DBSecurityGroupName: str) -> None:
        """
        Deletes a DB security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_security_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_security_group)
        """

    def delete_db_snapshot(self, *, DBSnapshotIdentifier: str) -> DeleteDBSnapshotResultTypeDef:
        """
        Deletes a DB snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_snapshot)
        """

    def delete_db_subnet_group(self, *, DBSubnetGroupName: str) -> None:
        """
        Deletes a DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_db_subnet_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_db_subnet_group)
        """

    def delete_event_subscription(
        self, *, SubscriptionName: str
    ) -> DeleteEventSubscriptionResultTypeDef:
        """
        Deletes an RDS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_event_subscription)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_event_subscription)
        """

    def delete_global_cluster(
        self, *, GlobalClusterIdentifier: str
    ) -> DeleteGlobalClusterResultTypeDef:
        """
        Deletes a global database cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_global_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_global_cluster)
        """

    def delete_installation_media(
        self, *, InstallationMediaId: str
    ) -> InstallationMediaResponseMetadataTypeDef:
        """
        Deletes the installation medium for a DB engine that requires an on-premises
        customer provided license, such as Microsoft SQL Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_installation_media)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_installation_media)
        """

    def delete_option_group(self, *, OptionGroupName: str) -> None:
        """
        Deletes an existing option group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.delete_option_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#delete_option_group)
        """

    def deregister_db_proxy_targets(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        DBInstanceIdentifiers: Sequence[str] = ...,
        DBClusterIdentifiers: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Remove the association between one or more `DBProxyTarget` data structures and a
        `DBProxyTargetGroup` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.deregister_db_proxy_targets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#deregister_db_proxy_targets)
        """

    def describe_account_attributes(self) -> AccountAttributesMessageTypeDef:
        """
        Lists all of the attributes for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_account_attributes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_account_attributes)
        """

    def describe_certificates(
        self,
        *,
        CertificateIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> CertificateMessageTypeDef:
        """
        Lists the set of CA certificates provided by Amazon RDS for this Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_certificates)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_certificates)
        """

    def describe_custom_availability_zones(
        self,
        *,
        CustomAvailabilityZoneId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> CustomAvailabilityZoneMessageTypeDef:
        """
        Returns information about custom Availability Zones (AZs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_custom_availability_zones)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_custom_availability_zones)
        """

    def describe_db_cluster_backtracks(
        self,
        *,
        DBClusterIdentifier: str,
        BacktrackIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterBacktrackMessageTypeDef:
        """
        Returns information about backtracks for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_backtracks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_backtracks)
        """

    def describe_db_cluster_endpoints(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterEndpointIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterEndpointMessageTypeDef:
        """
        Returns information about endpoints for an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_endpoints)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_endpoints)
        """

    def describe_db_cluster_parameter_groups(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of `DBClusterParameterGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_parameter_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_parameter_groups)
        """

    def describe_db_cluster_parameters(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_parameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_parameters)
        """

    def describe_db_cluster_snapshot_attributes(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DescribeDBClusterSnapshotAttributesResultTypeDef:
        """
        Returns a list of DB cluster snapshot attribute names and values for a manual DB
        cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_snapshot_attributes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_snapshot_attributes)
        """

    def describe_db_cluster_snapshots(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...
    ) -> DBClusterSnapshotMessageTypeDef:
        """
        Returns information about DB cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_cluster_snapshots)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_cluster_snapshots)
        """

    def describe_db_clusters(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...
    ) -> DBClusterMessageTypeDef:
        """
        Returns information about provisioned Aurora DB clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_clusters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_clusters)
        """

    def describe_db_engine_versions(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...,
        IncludeAll: bool = ...
    ) -> DBEngineVersionMessageTypeDef:
        """
        Returns a list of the available DB engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_engine_versions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_engine_versions)
        """

    def describe_db_instance_automated_backups(
        self,
        *,
        DbiResourceId: str = ...,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        DBInstanceAutomatedBackupsArn: str = ...
    ) -> DBInstanceAutomatedBackupMessageTypeDef:
        """
        Displays backups for both current and deleted instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_instance_automated_backups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_instance_automated_backups)
        """

    def describe_db_instances(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBInstanceMessageTypeDef:
        """
        Returns information about provisioned RDS instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_instances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_instances)
        """

    def describe_db_log_files(
        self,
        *,
        DBInstanceIdentifier: str,
        FilenameContains: str = ...,
        FileLastWritten: int = ...,
        FileSize: int = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeDBLogFilesResponseTypeDef:
        """
        Returns a list of DB log files for the DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_log_files)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_log_files)
        """

    def describe_db_parameter_groups(
        self,
        *,
        DBParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBParameterGroupsMessageTypeDef:
        """
        Returns a list of `DBParameterGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_parameter_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_parameter_groups)
        """

    def describe_db_parameters(
        self,
        *,
        DBParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_parameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_parameters)
        """

    def describe_db_proxies(
        self,
        *,
        DBProxyName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> DescribeDBProxiesResponseTypeDef:
        """
        Returns information about DB proxies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_proxies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_proxies)
        """

    def describe_db_proxy_endpoints(
        self,
        *,
        DBProxyName: str = ...,
        DBProxyEndpointName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> DescribeDBProxyEndpointsResponseTypeDef:
        """
        Returns information about DB proxy endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_proxy_endpoints)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_proxy_endpoints)
        """

    def describe_db_proxy_target_groups(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> DescribeDBProxyTargetGroupsResponseTypeDef:
        """
        Returns information about DB proxy target groups, represented by
        `DBProxyTargetGroup` data structures.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_proxy_target_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_proxy_target_groups)
        """

    def describe_db_proxy_targets(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> DescribeDBProxyTargetsResponseTypeDef:
        """
        Returns information about `DBProxyTarget` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_proxy_targets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_proxy_targets)
        """

    def describe_db_security_groups(
        self,
        *,
        DBSecurityGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBSecurityGroupMessageTypeDef:
        """
        Returns a list of `DBSecurityGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_security_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_security_groups)
        """

    def describe_db_snapshot_attributes(
        self, *, DBSnapshotIdentifier: str
    ) -> DescribeDBSnapshotAttributesResultTypeDef:
        """
        Returns a list of DB snapshot attribute names and values for a manual DB
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_snapshot_attributes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_snapshot_attributes)
        """

    def describe_db_snapshots(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        DBSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        DbiResourceId: str = ...
    ) -> DBSnapshotMessageTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_snapshots)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_snapshots)
        """

    def describe_db_subnet_groups(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBSubnetGroupMessageTypeDef:
        """
        Returns a list of DBSubnetGroup descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_db_subnet_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_db_subnet_groups)
        """

    def describe_engine_default_cluster_parameters(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEngineDefaultClusterParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the cluster
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_engine_default_cluster_parameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_engine_default_cluster_parameters)
        """

    def describe_engine_default_parameters(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEngineDefaultParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the specified
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_engine_default_parameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_engine_default_parameters)
        """

    def describe_event_categories(
        self, *, SourceType: str = ..., Filters: Sequence["FilterTypeDef"] = ...
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of categories for all event source types, or, if specified, for
        a specified source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_event_categories)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_event_categories)
        """

    def describe_event_subscriptions(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists all the subscription descriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_event_subscriptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_event_subscriptions)
        """

    def describe_events(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventsMessageTypeDef:
        """
        Returns events related to DB instances, DB clusters, DB parameter groups, DB
        security groups, DB snapshots, and DB cluster snapshots for the past 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_events)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_events)
        """

    def describe_export_tasks(
        self,
        *,
        ExportTaskIdentifier: str = ...,
        SourceArn: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> ExportTasksMessageTypeDef:
        """
        Returns information about a snapshot export to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_export_tasks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_export_tasks)
        """

    def describe_global_clusters(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> GlobalClustersMessageTypeDef:
        """
        Returns information about Aurora global database clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_global_clusters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_global_clusters)
        """

    def describe_installation_media(
        self,
        *,
        InstallationMediaId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> InstallationMediaMessageTypeDef:
        """
        Describes the available installation media for a DB engine that requires an on-
        premises customer provided license, such as Microsoft SQL Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_installation_media)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_installation_media)
        """

    def describe_option_group_options(
        self,
        *,
        EngineName: str,
        MajorEngineVersion: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> OptionGroupOptionsMessageTypeDef:
        """
        Describes all available options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_option_group_options)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_option_group_options)
        """

    def describe_option_groups(
        self,
        *,
        OptionGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...,
        EngineName: str = ...,
        MajorEngineVersion: str = ...
    ) -> OptionGroupsTypeDef:
        """
        Describes the available option groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_option_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_option_groups)
        """

    def describe_orderable_db_instance_options(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        AvailabilityZoneGroup: str = ...,
        Vpc: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> OrderableDBInstanceOptionsMessageTypeDef:
        """
        Returns a list of orderable DB instance options for the specified engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_orderable_db_instance_options)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_orderable_db_instance_options)
        """

    def describe_pending_maintenance_actions(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> PendingMaintenanceActionsMessageTypeDef:
        """
        Returns a list of resources (for example, DB instances) that have at least one
        pending maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_pending_maintenance_actions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_pending_maintenance_actions)
        """

    def describe_reserved_db_instances(
        self,
        *,
        ReservedDBInstanceId: str = ...,
        ReservedDBInstancesOfferingId: str = ...,
        DBInstanceClass: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MultiAZ: bool = ...,
        LeaseId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> ReservedDBInstanceMessageTypeDef:
        """
        Returns information about reserved DB instances for this account, or about a
        specified reserved DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_reserved_db_instances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_reserved_db_instances)
        """

    def describe_reserved_db_instances_offerings(
        self,
        *,
        ReservedDBInstancesOfferingId: str = ...,
        DBInstanceClass: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MultiAZ: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> ReservedDBInstancesOfferingMessageTypeDef:
        """
        Lists available reserved DB instance offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_reserved_db_instances_offerings)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_reserved_db_instances_offerings)
        """

    def describe_source_regions(
        self,
        *,
        RegionName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> SourceRegionMessageTypeDef:
        """
        Returns a list of the source Amazon Web Services Regions where the current
        Amazon Web Services Region can create a read replica, copy a DB snapshot from,
        or replicate automated backups from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_source_regions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_source_regions)
        """

    def describe_valid_db_instance_modifications(
        self, *, DBInstanceIdentifier: str
    ) -> DescribeValidDBInstanceModificationsResultTypeDef:
        """
        You can call `DescribeValidDBInstanceModifications` to learn what modifications
        you can make to your DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.describe_valid_db_instance_modifications)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#describe_valid_db_instance_modifications)
        """

    def download_db_log_file_portion(
        self,
        *,
        DBInstanceIdentifier: str,
        LogFileName: str,
        Marker: str = ...,
        NumberOfLines: int = ...
    ) -> DownloadDBLogFilePortionDetailsTypeDef:
        """
        Downloads all or a portion of the specified log file, up to 1 MB in size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.download_db_log_file_portion)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#download_db_log_file_portion)
        """

    def failover_db_cluster(
        self, *, DBClusterIdentifier: str, TargetDBInstanceIdentifier: str = ...
    ) -> FailoverDBClusterResultTypeDef:
        """
        Forces a failover for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.failover_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#failover_db_cluster)
        """

    def failover_global_cluster(
        self, *, GlobalClusterIdentifier: str, TargetDbClusterIdentifier: str
    ) -> FailoverGlobalClusterResultTypeDef:
        """
        Initiates the failover process for an Aurora global database ( GlobalCluster ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.failover_global_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#failover_global_cluster)
        """

    def generate_db_auth_token(
        self, DBHostname: str, Port: int, DBUsername: str, Region: str = None
    ) -> str:
        """
        Generates an auth token used to connect to a db with IAM credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.generate_db_auth_token)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#generate_db_auth_token)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#generate_presigned_url)
        """

    def import_installation_media(
        self,
        *,
        CustomAvailabilityZoneId: str,
        Engine: str,
        EngineVersion: str,
        EngineInstallationMediaPath: str,
        OSInstallationMediaPath: str
    ) -> InstallationMediaResponseMetadataTypeDef:
        """
        Imports the installation media for a DB engine that requires an on-premises
        customer provided license, such as SQL Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.import_installation_media)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#import_installation_media)
        """

    def list_tags_for_resource(
        self, *, ResourceName: str, Filters: Sequence["FilterTypeDef"] = ...
    ) -> TagListMessageTypeDef:
        """
        Lists all tags on an Amazon RDS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#list_tags_for_resource)
        """

    def modify_certificates(
        self, *, CertificateIdentifier: str = ..., RemoveCustomerOverride: bool = ...
    ) -> ModifyCertificatesResultTypeDef:
        """
        Override the system-default Secure Sockets Layer/Transport Layer Security
        (SSL/TLS) certificate for Amazon RDS for new DB instances temporarily, or remove
        the override.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_certificates)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_certificates)
        """

    def modify_current_db_cluster_capacity(
        self,
        *,
        DBClusterIdentifier: str,
        Capacity: int = ...,
        SecondsBeforeTimeout: int = ...,
        TimeoutAction: str = ...
    ) -> DBClusterCapacityInfoTypeDef:
        """
        Set the capacity of an Aurora Serverless DB cluster to a specific value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_current_db_cluster_capacity)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_current_db_cluster_capacity)
        """

    def modify_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        NewDBClusterIdentifier: str = ...,
        ApplyImmediately: bool = ...,
        BackupRetentionPeriod: int = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Port: int = ...,
        MasterUserPassword: str = ...,
        OptionGroupName: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        BacktrackWindow: int = ...,
        CloudwatchLogsExportConfiguration: "CloudwatchLogsExportConfigurationTypeDef" = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...,
        DBInstanceParameterGroupName: str = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...,
        ScalingConfiguration: "ScalingConfigurationTypeDef" = ...,
        DeletionProtection: bool = ...,
        EnableHttpEndpoint: bool = ...,
        CopyTagsToSnapshot: bool = ...,
        EnableGlobalWriteForwarding: bool = ...
    ) -> ModifyDBClusterResultTypeDef:
        """
        Modify a setting for an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_cluster)
        """

    def modify_db_cluster_endpoint(
        self,
        *,
        DBClusterEndpointIdentifier: str,
        EndpointType: str = ...,
        StaticMembers: Sequence[str] = ...,
        ExcludedMembers: Sequence[str] = ...
    ) -> DBClusterEndpointResponseMetadataTypeDef:
        """
        Modifies the properties of an endpoint in an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_cluster_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_cluster_endpoint)
        """

    def modify_db_cluster_parameter_group(
        self, *, DBClusterParameterGroupName: str, Parameters: Sequence["ParameterTypeDef"]
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_cluster_parameter_group)
        """

    def modify_db_cluster_snapshot_attribute(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        AttributeName: str,
        ValuesToAdd: Sequence[str] = ...,
        ValuesToRemove: Sequence[str] = ...
    ) -> ModifyDBClusterSnapshotAttributeResultTypeDef:
        """
        Adds an attribute and values to, or removes an attribute and values from, a
        manual DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_cluster_snapshot_attribute)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_cluster_snapshot_attribute)
        """

    def modify_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        AllocatedStorage: int = ...,
        DBInstanceClass: str = ...,
        DBSubnetGroupName: str = ...,
        DBSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        ApplyImmediately: bool = ...,
        MasterUserPassword: str = ...,
        DBParameterGroupName: str = ...,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        NewDBInstanceIdentifier: str = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        CACertificateIdentifier: str = ...,
        Domain: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        DBPortNumber: int = ...,
        PubliclyAccessible: bool = ...,
        MonitoringRoleArn: str = ...,
        DomainIAMRoleName: str = ...,
        PromotionTier: int = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        PerformanceInsightsRetentionPeriod: int = ...,
        CloudwatchLogsExportConfiguration: "CloudwatchLogsExportConfigurationTypeDef" = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        UseDefaultProcessorFeatures: bool = ...,
        DeletionProtection: bool = ...,
        MaxAllocatedStorage: int = ...,
        CertificateRotationRestart: bool = ...,
        ReplicaMode: ReplicaModeType = ...,
        EnableCustomerOwnedIp: bool = ...,
        AwsBackupRecoveryPointArn: str = ...
    ) -> ModifyDBInstanceResultTypeDef:
        """
        Modifies settings for a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_instance)
        """

    def modify_db_parameter_group(
        self, *, DBParameterGroupName: str, Parameters: Sequence["ParameterTypeDef"]
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_parameter_group)
        """

    def modify_db_proxy(
        self,
        *,
        DBProxyName: str,
        NewDBProxyName: str = ...,
        Auth: Sequence["UserAuthConfigTypeDef"] = ...,
        RequireTLS: bool = ...,
        IdleClientTimeout: int = ...,
        DebugLogging: bool = ...,
        RoleArn: str = ...,
        SecurityGroups: Sequence[str] = ...
    ) -> ModifyDBProxyResponseTypeDef:
        """
        Changes the settings for an existing DB proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_proxy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_proxy)
        """

    def modify_db_proxy_endpoint(
        self,
        *,
        DBProxyEndpointName: str,
        NewDBProxyEndpointName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...
    ) -> ModifyDBProxyEndpointResponseTypeDef:
        """
        Changes the settings for an existing DB proxy endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_proxy_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_proxy_endpoint)
        """

    def modify_db_proxy_target_group(
        self,
        *,
        TargetGroupName: str,
        DBProxyName: str,
        ConnectionPoolConfig: "ConnectionPoolConfigurationTypeDef" = ...,
        NewName: str = ...
    ) -> ModifyDBProxyTargetGroupResponseTypeDef:
        """
        Modifies the properties of a `DBProxyTargetGroup` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_proxy_target_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_proxy_target_group)
        """

    def modify_db_snapshot(
        self, *, DBSnapshotIdentifier: str, EngineVersion: str = ..., OptionGroupName: str = ...
    ) -> ModifyDBSnapshotResultTypeDef:
        """
        Updates a manual DB snapshot with a new engine version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_snapshot)
        """

    def modify_db_snapshot_attribute(
        self,
        *,
        DBSnapshotIdentifier: str,
        AttributeName: str,
        ValuesToAdd: Sequence[str] = ...,
        ValuesToRemove: Sequence[str] = ...
    ) -> ModifyDBSnapshotAttributeResultTypeDef:
        """
        Adds an attribute and values to, or removes an attribute and values from, a
        manual DB snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_snapshot_attribute)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_snapshot_attribute)
        """

    def modify_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        SubnetIds: Sequence[str],
        DBSubnetGroupDescription: str = ...
    ) -> ModifyDBSubnetGroupResultTypeDef:
        """
        Modifies an existing DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_db_subnet_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_db_subnet_group)
        """

    def modify_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str = ...,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        Enabled: bool = ...
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing RDS event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_event_subscription)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_event_subscription)
        """

    def modify_global_cluster(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        NewGlobalClusterIdentifier: str = ...,
        DeletionProtection: bool = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...
    ) -> ModifyGlobalClusterResultTypeDef:
        """
        Modify a setting for an Amazon Aurora global cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_global_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_global_cluster)
        """

    def modify_option_group(
        self,
        *,
        OptionGroupName: str,
        OptionsToInclude: Sequence["OptionConfigurationTypeDef"] = ...,
        OptionsToRemove: Sequence[str] = ...,
        ApplyImmediately: bool = ...
    ) -> ModifyOptionGroupResultTypeDef:
        """
        Modifies an existing option group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.modify_option_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#modify_option_group)
        """

    def promote_read_replica(
        self,
        *,
        DBInstanceIdentifier: str,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...
    ) -> PromoteReadReplicaResultTypeDef:
        """
        Promotes a read replica DB instance to a standalone DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.promote_read_replica)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#promote_read_replica)
        """

    def promote_read_replica_db_cluster(
        self, *, DBClusterIdentifier: str
    ) -> PromoteReadReplicaDBClusterResultTypeDef:
        """
        Promotes a read replica DB cluster to a standalone DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.promote_read_replica_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#promote_read_replica_db_cluster)
        """

    def purchase_reserved_db_instances_offering(
        self,
        *,
        ReservedDBInstancesOfferingId: str,
        ReservedDBInstanceId: str = ...,
        DBInstanceCount: int = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> PurchaseReservedDBInstancesOfferingResultTypeDef:
        """
        Purchases a reserved DB instance offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.purchase_reserved_db_instances_offering)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#purchase_reserved_db_instances_offering)
        """

    def reboot_db_instance(
        self, *, DBInstanceIdentifier: str, ForceFailover: bool = ...
    ) -> RebootDBInstanceResultTypeDef:
        """
        You might need to reboot your DB instance, usually for maintenance reasons.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.reboot_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#reboot_db_instance)
        """

    def register_db_proxy_targets(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        DBInstanceIdentifiers: Sequence[str] = ...,
        DBClusterIdentifiers: Sequence[str] = ...
    ) -> RegisterDBProxyTargetsResponseTypeDef:
        """
        Associate one or more `DBProxyTarget` data structures with a
        `DBProxyTargetGroup` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.register_db_proxy_targets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#register_db_proxy_targets)
        """

    def remove_from_global_cluster(
        self, *, GlobalClusterIdentifier: str = ..., DbClusterIdentifier: str = ...
    ) -> RemoveFromGlobalClusterResultTypeDef:
        """
        Detaches an Aurora secondary cluster from an Aurora global database cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.remove_from_global_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#remove_from_global_cluster)
        """

    def remove_role_from_db_cluster(
        self, *, DBClusterIdentifier: str, RoleArn: str, FeatureName: str = ...
    ) -> None:
        """
        Disassociates an Amazon Web Services Identity and Access Management (IAM) role
        from an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.remove_role_from_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#remove_role_from_db_cluster)
        """

    def remove_role_from_db_instance(
        self, *, DBInstanceIdentifier: str, RoleArn: str, FeatureName: str
    ) -> None:
        """
        Disassociates an Amazon Web Services Identity and Access Management (IAM) role
        from a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.remove_role_from_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#remove_role_from_db_instance)
        """

    def remove_source_identifier_from_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> RemoveSourceIdentifierFromSubscriptionResultTypeDef:
        """
        Removes a source identifier from an existing RDS event notification
        subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.remove_source_identifier_from_subscription)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#remove_source_identifier_from_subscription)
        """

    def remove_tags_from_resource(self, *, ResourceName: str, TagKeys: Sequence[str]) -> None:
        """
        Removes metadata tags from an Amazon RDS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.remove_tags_from_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#remove_tags_from_resource)
        """

    def reset_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence["ParameterTypeDef"] = ...
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group to the default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.reset_db_cluster_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#reset_db_cluster_parameter_group)
        """

    def reset_db_parameter_group(
        self,
        *,
        DBParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence["ParameterTypeDef"] = ...
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group to the engine/system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.reset_db_parameter_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#reset_db_parameter_group)
        """

    def restore_db_cluster_from_s3(
        self,
        *,
        DBClusterIdentifier: str,
        Engine: str,
        MasterUsername: str,
        MasterUserPassword: str,
        SourceEngine: str,
        SourceEngineVersion: str,
        S3BucketName: str,
        S3IngestionRoleArn: str,
        AvailabilityZones: Sequence[str] = ...,
        BackupRetentionPeriod: int = ...,
        CharacterSetName: str = ...,
        DatabaseName: str = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        DBSubnetGroupName: str = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        OptionGroupName: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        S3Prefix: str = ...,
        BacktrackWindow: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...,
        CopyTagsToSnapshot: bool = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...
    ) -> RestoreDBClusterFromS3ResultTypeDef:
        """
        Creates an Amazon Aurora DB cluster from MySQL data stored in an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_cluster_from_s3)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_cluster_from_s3)
        """

    def restore_db_cluster_from_snapshot(
        self,
        *,
        DBClusterIdentifier: str,
        SnapshotIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        DatabaseName: str = ...,
        OptionGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        BacktrackWindow: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        EngineMode: str = ...,
        ScalingConfiguration: "ScalingConfigurationTypeDef" = ...,
        DBClusterParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        CopyTagsToSnapshot: bool = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...
    ) -> RestoreDBClusterFromSnapshotResultTypeDef:
        """
        Creates a new DB cluster from a DB snapshot or DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_cluster_from_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_cluster_from_snapshot)
        """

    def restore_db_cluster_to_point_in_time(
        self,
        *,
        DBClusterIdentifier: str,
        SourceDBClusterIdentifier: str,
        RestoreType: str = ...,
        RestoreToTime: Union[datetime, str] = ...,
        UseLatestRestorableTime: bool = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        OptionGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        BacktrackWindow: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DBClusterParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        CopyTagsToSnapshot: bool = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...,
        ScalingConfiguration: "ScalingConfigurationTypeDef" = ...,
        EngineMode: str = ...
    ) -> RestoreDBClusterToPointInTimeResultTypeDef:
        """
        Restores a DB cluster to an arbitrary point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_cluster_to_point_in_time)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_cluster_to_point_in_time)
        """

    def restore_db_instance_from_db_snapshot(
        self,
        *,
        DBInstanceIdentifier: str,
        DBSnapshotIdentifier: str,
        DBInstanceClass: str = ...,
        Port: int = ...,
        AvailabilityZone: str = ...,
        DBSubnetGroupName: str = ...,
        MultiAZ: bool = ...,
        PubliclyAccessible: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        DBName: str = ...,
        Engine: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Domain: str = ...,
        CopyTagsToSnapshot: bool = ...,
        DomainIAMRoleName: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        UseDefaultProcessorFeatures: bool = ...,
        DBParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        EnableCustomerOwnedIp: bool = ...
    ) -> RestoreDBInstanceFromDBSnapshotResultTypeDef:
        """
        Creates a new DB instance from a DB snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_instance_from_db_snapshot)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_instance_from_db_snapshot)
        """

    def restore_db_instance_from_s3(
        self,
        *,
        DBInstanceIdentifier: str,
        DBInstanceClass: str,
        Engine: str,
        SourceEngine: str,
        SourceEngineVersion: str,
        S3BucketName: str,
        S3IngestionRoleArn: str,
        DBName: str = ...,
        AllocatedStorage: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        DBSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        AvailabilityZone: str = ...,
        DBSubnetGroupName: str = ...,
        PreferredMaintenanceWindow: str = ...,
        DBParameterGroupName: str = ...,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...,
        Port: int = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        PubliclyAccessible: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageType: str = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        MonitoringRoleArn: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        S3Prefix: str = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        PerformanceInsightsRetentionPeriod: int = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        UseDefaultProcessorFeatures: bool = ...,
        DeletionProtection: bool = ...,
        MaxAllocatedStorage: int = ...
    ) -> RestoreDBInstanceFromS3ResultTypeDef:
        """
        Amazon Relational Database Service (Amazon RDS) supports importing MySQL
        databases by using backup files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_instance_from_s3)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_instance_from_s3)
        """

    def restore_db_instance_to_point_in_time(
        self,
        *,
        TargetDBInstanceIdentifier: str,
        SourceDBInstanceIdentifier: str = ...,
        RestoreTime: Union[datetime, str] = ...,
        UseLatestRestorableTime: bool = ...,
        DBInstanceClass: str = ...,
        Port: int = ...,
        AvailabilityZone: str = ...,
        DBSubnetGroupName: str = ...,
        MultiAZ: bool = ...,
        PubliclyAccessible: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        DBName: str = ...,
        Engine: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        CopyTagsToSnapshot: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Domain: str = ...,
        DomainIAMRoleName: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        ProcessorFeatures: Sequence["ProcessorFeatureTypeDef"] = ...,
        UseDefaultProcessorFeatures: bool = ...,
        DBParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        SourceDbiResourceId: str = ...,
        MaxAllocatedStorage: int = ...,
        SourceDBInstanceAutomatedBackupsArn: str = ...,
        EnableCustomerOwnedIp: bool = ...
    ) -> RestoreDBInstanceToPointInTimeResultTypeDef:
        """
        Restores a DB instance to an arbitrary point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.restore_db_instance_to_point_in_time)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#restore_db_instance_to_point_in_time)
        """

    def revoke_db_security_group_ingress(
        self,
        *,
        DBSecurityGroupName: str,
        CIDRIP: str = ...,
        EC2SecurityGroupName: str = ...,
        EC2SecurityGroupId: str = ...,
        EC2SecurityGroupOwnerId: str = ...
    ) -> RevokeDBSecurityGroupIngressResultTypeDef:
        """
        Revokes ingress from a DBSecurityGroup for previously authorized IP ranges or
        EC2 or VPC security groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.revoke_db_security_group_ingress)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#revoke_db_security_group_ingress)
        """

    def start_activity_stream(
        self,
        *,
        ResourceArn: str,
        Mode: ActivityStreamModeType,
        KmsKeyId: str,
        ApplyImmediately: bool = ...,
        EngineNativeAuditFieldsIncluded: bool = ...
    ) -> StartActivityStreamResponseTypeDef:
        """
        Starts a database activity stream to monitor activity on the database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.start_activity_stream)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#start_activity_stream)
        """

    def start_db_cluster(self, *, DBClusterIdentifier: str) -> StartDBClusterResultTypeDef:
        """
        Starts an Amazon Aurora DB cluster that was stopped using the Amazon Web
        Services console, the stop-db-cluster CLI command, or the StopDBCluster action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.start_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#start_db_cluster)
        """

    def start_db_instance(self, *, DBInstanceIdentifier: str) -> StartDBInstanceResultTypeDef:
        """
        Starts an Amazon RDS DB instance that was stopped using the Amazon Web Services
        console, the stop-db-instance CLI command, or the StopDBInstance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.start_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#start_db_instance)
        """

    def start_db_instance_automated_backups_replication(
        self,
        *,
        SourceDBInstanceArn: str,
        BackupRetentionPeriod: int = ...,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        SourceRegion: str = ...
    ) -> StartDBInstanceAutomatedBackupsReplicationResultTypeDef:
        """
        Enables replication of automated backups to a different Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.start_db_instance_automated_backups_replication)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#start_db_instance_automated_backups_replication)
        """

    def start_export_task(
        self,
        *,
        ExportTaskIdentifier: str,
        SourceArn: str,
        S3BucketName: str,
        IamRoleArn: str,
        KmsKeyId: str,
        S3Prefix: str = ...,
        ExportOnly: Sequence[str] = ...
    ) -> ExportTaskResponseMetadataTypeDef:
        """
        Starts an export of a snapshot to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.start_export_task)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#start_export_task)
        """

    def stop_activity_stream(
        self, *, ResourceArn: str, ApplyImmediately: bool = ...
    ) -> StopActivityStreamResponseTypeDef:
        """
        Stops a database activity stream that was started using the Amazon Web Services
        console, the `start-activity-stream` CLI command, or the `StartActivityStream`
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.stop_activity_stream)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#stop_activity_stream)
        """

    def stop_db_cluster(self, *, DBClusterIdentifier: str) -> StopDBClusterResultTypeDef:
        """
        Stops an Amazon Aurora DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.stop_db_cluster)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#stop_db_cluster)
        """

    def stop_db_instance(
        self, *, DBInstanceIdentifier: str, DBSnapshotIdentifier: str = ...
    ) -> StopDBInstanceResultTypeDef:
        """
        Stops an Amazon RDS DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.stop_db_instance)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#stop_db_instance)
        """

    def stop_db_instance_automated_backups_replication(
        self, *, SourceDBInstanceArn: str
    ) -> StopDBInstanceAutomatedBackupsReplicationResultTypeDef:
        """
        Stops automated backup replication for a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Client.stop_db_instance_automated_backups_replication)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/client.html#stop_db_instance_automated_backups_replication)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_certificates"]
    ) -> DescribeCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeCertificates)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecertificatespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_custom_availability_zones"]
    ) -> DescribeCustomAvailabilityZonesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeCustomAvailabilityZones)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describecustomavailabilityzonespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_backtracks"]
    ) -> DescribeDBClusterBacktracksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusterBacktracks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterbacktrackspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_endpoints"]
    ) -> DescribeDBClusterEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusterEndpoints)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterendpointspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameter_groups"]
    ) -> DescribeDBClusterParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameterGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparametergroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameters"]
    ) -> DescribeDBClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterparameterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_snapshots"]
    ) -> DescribeDBClusterSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusterSnapshots)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclustersnapshotspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_clusters"]
    ) -> DescribeDBClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBClusters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbclusterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_engine_versions"]
    ) -> DescribeDBEngineVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBEngineVersions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbengineversionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_instance_automated_backups"]
    ) -> DescribeDBInstanceAutomatedBackupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstanceautomatedbackupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_instances"]
    ) -> DescribeDBInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBInstances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbinstancespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_log_files"]
    ) -> DescribeDBLogFilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBLogFiles)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedblogfilespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameter_groups"]
    ) -> DescribeDBParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBParameterGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparametergroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameters"]
    ) -> DescribeDBParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBParameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbparameterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_proxies"]
    ) -> DescribeDBProxiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBProxies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxiespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_proxy_endpoints"]
    ) -> DescribeDBProxyEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBProxyEndpoints)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxyendpointspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_proxy_target_groups"]
    ) -> DescribeDBProxyTargetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargetGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetgroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_proxy_targets"]
    ) -> DescribeDBProxyTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbproxytargetspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_security_groups"]
    ) -> DescribeDBSecurityGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBSecurityGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsecuritygroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_snapshots"]
    ) -> DescribeDBSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBSnapshots)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsnapshotspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_subnet_groups"]
    ) -> DescribeDBSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeDBSubnetGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describedbsubnetgroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_cluster_parameters"]
    ) -> DescribeEngineDefaultClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultClusterParameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultclusterparameterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_parameters"]
    ) -> DescribeEngineDefaultParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultParameters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeenginedefaultparameterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeEventSubscriptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventsubscriptionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeEvents)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeeventspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_tasks"]
    ) -> DescribeExportTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeExportTasks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeexporttaskspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_clusters"]
    ) -> DescribeGlobalClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeGlobalClusters)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeglobalclusterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_installation_media"]
    ) -> DescribeInstallationMediaPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeInstallationMedia)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeinstallationmediapaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_option_group_options"]
    ) -> DescribeOptionGroupOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeOptionGroupOptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupoptionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_option_groups"]
    ) -> DescribeOptionGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeOptionGroups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeoptiongroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_db_instance_options"]
    ) -> DescribeOrderableDBInstanceOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeOrderableDBInstanceOptions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describeorderabledbinstanceoptionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_maintenance_actions"]
    ) -> DescribePendingMaintenanceActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribePendingMaintenanceActions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describependingmaintenanceactionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_db_instances"]
    ) -> DescribeReservedDBInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_db_instances_offerings"]
    ) -> DescribeReservedDBInstancesOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstancesOfferings)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describereserveddbinstancesofferingspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_source_regions"]
    ) -> DescribeSourceRegionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DescribeSourceRegions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#describesourceregionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["download_db_log_file_portion"]
    ) -> DownloadDBLogFilePortionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Paginator.DownloadDBLogFilePortion)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/paginators.html#downloaddblogfileportionpaginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_cluster_snapshot_available"]
    ) -> DBClusterSnapshotAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotAvailable)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbclustersnapshotavailablewaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_cluster_snapshot_deleted"]
    ) -> DBClusterSnapshotDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotDeleted)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbclustersnapshotdeletedwaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_instance_available"]
    ) -> DBInstanceAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBInstanceAvailable)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbinstanceavailablewaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["db_instance_deleted"]) -> DBInstanceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBInstanceDeleted)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbinstancedeletedwaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_snapshot_available"]
    ) -> DBSnapshotAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBSnapshotAvailable)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbsnapshotavailablewaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_snapshot_completed"]
    ) -> DBSnapshotCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBSnapshotCompleted)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbsnapshotcompletedwaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["db_snapshot_deleted"]) -> DBSnapshotDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/rds.html#RDS.Waiter.DBSnapshotDeleted)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_rds/waiters.html#dbsnapshotdeletedwaiter)
        """
