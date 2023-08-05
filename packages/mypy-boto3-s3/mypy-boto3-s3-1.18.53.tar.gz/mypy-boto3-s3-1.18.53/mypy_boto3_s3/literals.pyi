"""
Type annotations for s3 service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_s3/literals.html)

Usage::

    ```python
    from mypy_boto3_s3.literals import AnalyticsS3ExportFileFormatType

    data: AnalyticsS3ExportFileFormatType = "CSV"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AnalyticsS3ExportFileFormatType",
    "ArchiveStatusType",
    "BucketAccelerateStatusType",
    "BucketCannedACLType",
    "BucketExistsWaiterName",
    "BucketLocationConstraintType",
    "BucketLogsPermissionType",
    "BucketNotExistsWaiterName",
    "BucketVersioningStatusType",
    "CompressionTypeType",
    "DeleteMarkerReplicationStatusType",
    "EncodingTypeType",
    "EventType",
    "ExistingObjectReplicationStatusType",
    "ExpirationStatusType",
    "ExpressionTypeType",
    "FileHeaderInfoType",
    "FilterRuleNameType",
    "IntelligentTieringAccessTierType",
    "IntelligentTieringStatusType",
    "InventoryFormatType",
    "InventoryFrequencyType",
    "InventoryIncludedObjectVersionsType",
    "InventoryOptionalFieldType",
    "JSONTypeType",
    "ListMultipartUploadsPaginatorName",
    "ListObjectVersionsPaginatorName",
    "ListObjectsPaginatorName",
    "ListObjectsV2PaginatorName",
    "ListPartsPaginatorName",
    "MFADeleteStatusType",
    "MFADeleteType",
    "MetadataDirectiveType",
    "MetricsStatusType",
    "ObjectCannedACLType",
    "ObjectExistsWaiterName",
    "ObjectLockEnabledType",
    "ObjectLockLegalHoldStatusType",
    "ObjectLockModeType",
    "ObjectLockRetentionModeType",
    "ObjectNotExistsWaiterName",
    "ObjectOwnershipType",
    "ObjectStorageClassType",
    "ObjectVersionStorageClassType",
    "OwnerOverrideType",
    "PayerType",
    "PermissionType",
    "ProtocolType",
    "QuoteFieldsType",
    "ReplicaModificationsStatusType",
    "ReplicationRuleStatusType",
    "ReplicationStatusType",
    "ReplicationTimeStatusType",
    "RequestChargedType",
    "RequestPayerType",
    "RestoreRequestTypeType",
    "ServerSideEncryptionType",
    "SseKmsEncryptedObjectsStatusType",
    "StorageClassAnalysisSchemaVersionType",
    "StorageClassType",
    "TaggingDirectiveType",
    "TierType",
    "TransitionStorageClassType",
    "TypeType",
    "ServiceName",
    "PaginatorName",
    "WaiterName",
)

AnalyticsS3ExportFileFormatType = Literal["CSV"]
ArchiveStatusType = Literal["ARCHIVE_ACCESS", "DEEP_ARCHIVE_ACCESS"]
BucketAccelerateStatusType = Literal["Enabled", "Suspended"]
BucketCannedACLType = Literal["authenticated-read", "private", "public-read", "public-read-write"]
BucketExistsWaiterName = Literal["bucket_exists"]
BucketLocationConstraintType = Literal[
    "EU",
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "cn-north-1",
    "cn-northwest-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
    "us-east-2",
    "us-gov-east-1",
    "us-gov-west-1",
    "us-west-1",
    "us-west-2",
]
BucketLogsPermissionType = Literal["FULL_CONTROL", "READ", "WRITE"]
BucketNotExistsWaiterName = Literal["bucket_not_exists"]
BucketVersioningStatusType = Literal["Enabled", "Suspended"]
CompressionTypeType = Literal["BZIP2", "GZIP", "NONE"]
DeleteMarkerReplicationStatusType = Literal["Disabled", "Enabled"]
EncodingTypeType = Literal["url"]
EventType = Literal[
    "s3:ObjectCreated:*",
    "s3:ObjectCreated:CompleteMultipartUpload",
    "s3:ObjectCreated:Copy",
    "s3:ObjectCreated:Post",
    "s3:ObjectCreated:Put",
    "s3:ObjectRemoved:*",
    "s3:ObjectRemoved:Delete",
    "s3:ObjectRemoved:DeleteMarkerCreated",
    "s3:ObjectRestore:*",
    "s3:ObjectRestore:Completed",
    "s3:ObjectRestore:Post",
    "s3:ReducedRedundancyLostObject",
    "s3:Replication:*",
    "s3:Replication:OperationFailedReplication",
    "s3:Replication:OperationMissedThreshold",
    "s3:Replication:OperationNotTracked",
    "s3:Replication:OperationReplicatedAfterThreshold",
]
ExistingObjectReplicationStatusType = Literal["Disabled", "Enabled"]
ExpirationStatusType = Literal["Disabled", "Enabled"]
ExpressionTypeType = Literal["SQL"]
FileHeaderInfoType = Literal["IGNORE", "NONE", "USE"]
FilterRuleNameType = Literal["prefix", "suffix"]
IntelligentTieringAccessTierType = Literal["ARCHIVE_ACCESS", "DEEP_ARCHIVE_ACCESS"]
IntelligentTieringStatusType = Literal["Disabled", "Enabled"]
InventoryFormatType = Literal["CSV", "ORC", "Parquet"]
InventoryFrequencyType = Literal["Daily", "Weekly"]
InventoryIncludedObjectVersionsType = Literal["All", "Current"]
InventoryOptionalFieldType = Literal[
    "BucketKeyStatus",
    "ETag",
    "EncryptionStatus",
    "IntelligentTieringAccessTier",
    "IsMultipartUploaded",
    "LastModifiedDate",
    "ObjectLockLegalHoldStatus",
    "ObjectLockMode",
    "ObjectLockRetainUntilDate",
    "ReplicationStatus",
    "Size",
    "StorageClass",
]
JSONTypeType = Literal["DOCUMENT", "LINES"]
ListMultipartUploadsPaginatorName = Literal["list_multipart_uploads"]
ListObjectVersionsPaginatorName = Literal["list_object_versions"]
ListObjectsPaginatorName = Literal["list_objects"]
ListObjectsV2PaginatorName = Literal["list_objects_v2"]
ListPartsPaginatorName = Literal["list_parts"]
MFADeleteStatusType = Literal["Disabled", "Enabled"]
MFADeleteType = Literal["Disabled", "Enabled"]
MetadataDirectiveType = Literal["COPY", "REPLACE"]
MetricsStatusType = Literal["Disabled", "Enabled"]
ObjectCannedACLType = Literal[
    "authenticated-read",
    "aws-exec-read",
    "bucket-owner-full-control",
    "bucket-owner-read",
    "private",
    "public-read",
    "public-read-write",
]
ObjectExistsWaiterName = Literal["object_exists"]
ObjectLockEnabledType = Literal["Enabled"]
ObjectLockLegalHoldStatusType = Literal["OFF", "ON"]
ObjectLockModeType = Literal["COMPLIANCE", "GOVERNANCE"]
ObjectLockRetentionModeType = Literal["COMPLIANCE", "GOVERNANCE"]
ObjectNotExistsWaiterName = Literal["object_not_exists"]
ObjectOwnershipType = Literal["BucketOwnerPreferred", "ObjectWriter"]
ObjectStorageClassType = Literal[
    "DEEP_ARCHIVE",
    "GLACIER",
    "INTELLIGENT_TIERING",
    "ONEZONE_IA",
    "OUTPOSTS",
    "REDUCED_REDUNDANCY",
    "STANDARD",
    "STANDARD_IA",
]
ObjectVersionStorageClassType = Literal["STANDARD"]
OwnerOverrideType = Literal["Destination"]
PayerType = Literal["BucketOwner", "Requester"]
PermissionType = Literal["FULL_CONTROL", "READ", "READ_ACP", "WRITE", "WRITE_ACP"]
ProtocolType = Literal["http", "https"]
QuoteFieldsType = Literal["ALWAYS", "ASNEEDED"]
ReplicaModificationsStatusType = Literal["Disabled", "Enabled"]
ReplicationRuleStatusType = Literal["Disabled", "Enabled"]
ReplicationStatusType = Literal["COMPLETE", "FAILED", "PENDING", "REPLICA"]
ReplicationTimeStatusType = Literal["Disabled", "Enabled"]
RequestChargedType = Literal["requester"]
RequestPayerType = Literal["requester"]
RestoreRequestTypeType = Literal["SELECT"]
ServerSideEncryptionType = Literal["AES256", "aws:kms"]
SseKmsEncryptedObjectsStatusType = Literal["Disabled", "Enabled"]
StorageClassAnalysisSchemaVersionType = Literal["V_1"]
StorageClassType = Literal[
    "DEEP_ARCHIVE",
    "GLACIER",
    "INTELLIGENT_TIERING",
    "ONEZONE_IA",
    "OUTPOSTS",
    "REDUCED_REDUNDANCY",
    "STANDARD",
    "STANDARD_IA",
]
TaggingDirectiveType = Literal["COPY", "REPLACE"]
TierType = Literal["Bulk", "Expedited", "Standard"]
TransitionStorageClassType = Literal[
    "DEEP_ARCHIVE", "GLACIER", "INTELLIGENT_TIERING", "ONEZONE_IA", "STANDARD_IA"
]
TypeType = Literal["AmazonCustomerByEmail", "CanonicalUser", "Group"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "batch",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-messaging",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iotwireless",
    "ivs",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migrationhub-config",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "voice-id",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "xray",
]
PaginatorName = Literal[
    "list_multipart_uploads",
    "list_object_versions",
    "list_objects",
    "list_objects_v2",
    "list_parts",
]
WaiterName = Literal["bucket_exists", "bucket_not_exists", "object_exists", "object_not_exists"]
