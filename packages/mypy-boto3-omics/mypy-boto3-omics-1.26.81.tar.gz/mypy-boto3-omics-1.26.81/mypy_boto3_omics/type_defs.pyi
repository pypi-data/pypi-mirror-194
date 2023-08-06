"""
Type annotations for omics service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_omics/type_defs/)

Usage::

    ```python
    from mypy_boto3_omics.type_defs import ActivateReadSetFilterTypeDef

    data: ActivateReadSetFilterTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AnnotationTypeType,
    FileTypeType,
    FormatToHeaderKeyType,
    JobStatusType,
    ReadSetActivationJobItemStatusType,
    ReadSetActivationJobStatusType,
    ReadSetExportJobItemStatusType,
    ReadSetExportJobStatusType,
    ReadSetFileType,
    ReadSetImportJobItemStatusType,
    ReadSetImportJobStatusType,
    ReadSetStatusType,
    ReferenceFileType,
    ReferenceImportJobItemStatusType,
    ReferenceImportJobStatusType,
    ReferenceStatusType,
    RunLogLevelType,
    RunStatusType,
    SchemaValueTypeType,
    StoreFormatType,
    StoreStatusType,
    TaskStatusType,
    WorkflowEngineType,
    WorkflowStatusType,
    WorkflowTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActivateReadSetFilterTypeDef",
    "ActivateReadSetJobItemTypeDef",
    "ActivateReadSetSourceItemTypeDef",
    "AnnotationImportItemDetailTypeDef",
    "AnnotationImportItemSourceTypeDef",
    "AnnotationImportJobItemTypeDef",
    "ReferenceItemTypeDef",
    "SseConfigTypeDef",
    "BatchDeleteReadSetRequestRequestTypeDef",
    "ReadSetBatchErrorTypeDef",
    "ResponseMetadataTypeDef",
    "CancelAnnotationImportRequestRequestTypeDef",
    "CancelRunRequestRequestTypeDef",
    "CancelVariantImportRequestRequestTypeDef",
    "CreateRunGroupRequestRequestTypeDef",
    "WorkflowParameterTypeDef",
    "DeleteAnnotationStoreRequestRequestTypeDef",
    "DeleteReferenceRequestRequestTypeDef",
    "DeleteReferenceStoreRequestRequestTypeDef",
    "DeleteRunGroupRequestRequestTypeDef",
    "DeleteRunRequestRequestTypeDef",
    "DeleteSequenceStoreRequestRequestTypeDef",
    "DeleteVariantStoreRequestRequestTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "ExportReadSetDetailTypeDef",
    "ExportReadSetFilterTypeDef",
    "ExportReadSetJobDetailTypeDef",
    "ExportReadSetTypeDef",
    "FileInformationTypeDef",
    "VcfOptionsTypeDef",
    "WaiterConfigTypeDef",
    "GetAnnotationImportRequestRequestTypeDef",
    "GetAnnotationStoreRequestRequestTypeDef",
    "GetReadSetActivationJobRequestRequestTypeDef",
    "GetReadSetExportJobRequestRequestTypeDef",
    "GetReadSetImportJobRequestRequestTypeDef",
    "GetReadSetMetadataRequestRequestTypeDef",
    "SequenceInformationTypeDef",
    "GetReadSetRequestRequestTypeDef",
    "GetReferenceImportJobRequestRequestTypeDef",
    "ImportReferenceSourceItemTypeDef",
    "GetReferenceMetadataRequestRequestTypeDef",
    "GetReferenceRequestRequestTypeDef",
    "GetReferenceStoreRequestRequestTypeDef",
    "GetRunGroupRequestRequestTypeDef",
    "GetRunRequestRequestTypeDef",
    "GetRunTaskRequestRequestTypeDef",
    "GetSequenceStoreRequestRequestTypeDef",
    "GetVariantImportRequestRequestTypeDef",
    "VariantImportItemDetailTypeDef",
    "GetVariantStoreRequestRequestTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "ImportReadSetFilterTypeDef",
    "ImportReadSetJobItemTypeDef",
    "SourceFilesTypeDef",
    "ImportReferenceFilterTypeDef",
    "ImportReferenceJobItemTypeDef",
    "ListAnnotationImportJobsFilterTypeDef",
    "PaginatorConfigTypeDef",
    "ListAnnotationStoresFilterTypeDef",
    "ReadSetFilterTypeDef",
    "ReferenceStoreFilterTypeDef",
    "ReferenceFilterTypeDef",
    "ReferenceListItemTypeDef",
    "ListRunGroupsRequestRequestTypeDef",
    "RunGroupListItemTypeDef",
    "ListRunTasksRequestRequestTypeDef",
    "TaskListItemTypeDef",
    "ListRunsRequestRequestTypeDef",
    "RunListItemTypeDef",
    "SequenceStoreFilterTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVariantImportJobsFilterTypeDef",
    "VariantImportJobItemTypeDef",
    "ListVariantStoresFilterTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "WorkflowListItemTypeDef",
    "ReadOptionsTypeDef",
    "StartReadSetActivationJobSourceItemTypeDef",
    "StartReferenceImportJobSourceItemTypeDef",
    "StartRunRequestRequestTypeDef",
    "VariantImportItemSourceTypeDef",
    "TsvStoreOptionsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAnnotationStoreRequestRequestTypeDef",
    "UpdateRunGroupRequestRequestTypeDef",
    "UpdateVariantStoreRequestRequestTypeDef",
    "UpdateWorkflowRequestRequestTypeDef",
    "ListReadSetActivationJobsRequestRequestTypeDef",
    "AnnotationStoreItemTypeDef",
    "CreateReferenceStoreRequestRequestTypeDef",
    "CreateSequenceStoreRequestRequestTypeDef",
    "CreateVariantStoreRequestRequestTypeDef",
    "ReferenceStoreDetailTypeDef",
    "SequenceStoreDetailTypeDef",
    "VariantStoreItemTypeDef",
    "BatchDeleteReadSetResponseTypeDef",
    "CreateReferenceStoreResponseTypeDef",
    "CreateRunGroupResponseTypeDef",
    "CreateSequenceStoreResponseTypeDef",
    "CreateVariantStoreResponseTypeDef",
    "CreateWorkflowResponseTypeDef",
    "DeleteAnnotationStoreResponseTypeDef",
    "DeleteVariantStoreResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetReadSetActivationJobResponseTypeDef",
    "GetReadSetResponseTypeDef",
    "GetReferenceResponseTypeDef",
    "GetReferenceStoreResponseTypeDef",
    "GetRunGroupResponseTypeDef",
    "GetRunResponseTypeDef",
    "GetRunTaskResponseTypeDef",
    "GetSequenceStoreResponseTypeDef",
    "GetVariantStoreResponseTypeDef",
    "ListAnnotationImportJobsResponseTypeDef",
    "ListReadSetActivationJobsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartAnnotationImportResponseTypeDef",
    "StartReadSetActivationJobResponseTypeDef",
    "StartReadSetExportJobResponseTypeDef",
    "StartReadSetImportJobResponseTypeDef",
    "StartReferenceImportJobResponseTypeDef",
    "StartRunResponseTypeDef",
    "StartVariantImportResponseTypeDef",
    "UpdateVariantStoreResponseTypeDef",
    "CreateWorkflowRequestRequestTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetReadSetExportJobResponseTypeDef",
    "ListReadSetExportJobsRequestRequestTypeDef",
    "ListReadSetExportJobsResponseTypeDef",
    "StartReadSetExportJobRequestRequestTypeDef",
    "ReadSetFilesTypeDef",
    "ReferenceFilesTypeDef",
    "GetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef",
    "GetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef",
    "GetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef",
    "GetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef",
    "GetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef",
    "GetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef",
    "GetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef",
    "GetRunRequestRunCompletedWaitTypeDef",
    "GetRunRequestRunRunningWaitTypeDef",
    "GetRunTaskRequestTaskCompletedWaitTypeDef",
    "GetRunTaskRequestTaskRunningWaitTypeDef",
    "GetVariantImportRequestVariantImportJobCreatedWaitTypeDef",
    "GetVariantStoreRequestVariantStoreCreatedWaitTypeDef",
    "GetVariantStoreRequestVariantStoreDeletedWaitTypeDef",
    "GetWorkflowRequestWorkflowActiveWaitTypeDef",
    "ReadSetListItemTypeDef",
    "GetReferenceImportJobResponseTypeDef",
    "GetVariantImportResponseTypeDef",
    "ListReadSetImportJobsRequestRequestTypeDef",
    "ListReadSetImportJobsResponseTypeDef",
    "ImportReadSetSourceItemTypeDef",
    "StartReadSetImportJobSourceItemTypeDef",
    "ListReferenceImportJobsRequestRequestTypeDef",
    "ListReferenceImportJobsResponseTypeDef",
    "ListAnnotationImportJobsRequestRequestTypeDef",
    "ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef",
    "ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef",
    "ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef",
    "ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef",
    "ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef",
    "ListRunGroupsRequestListRunGroupsPaginateTypeDef",
    "ListRunTasksRequestListRunTasksPaginateTypeDef",
    "ListRunsRequestListRunsPaginateTypeDef",
    "ListWorkflowsRequestListWorkflowsPaginateTypeDef",
    "ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef",
    "ListAnnotationStoresRequestRequestTypeDef",
    "ListReadSetsRequestListReadSetsPaginateTypeDef",
    "ListReadSetsRequestRequestTypeDef",
    "ListReferenceStoresRequestListReferenceStoresPaginateTypeDef",
    "ListReferenceStoresRequestRequestTypeDef",
    "ListReferencesRequestListReferencesPaginateTypeDef",
    "ListReferencesRequestRequestTypeDef",
    "ListReferencesResponseTypeDef",
    "ListRunGroupsResponseTypeDef",
    "ListRunTasksResponseTypeDef",
    "ListRunsResponseTypeDef",
    "ListSequenceStoresRequestListSequenceStoresPaginateTypeDef",
    "ListSequenceStoresRequestRequestTypeDef",
    "ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef",
    "ListVariantImportJobsRequestRequestTypeDef",
    "ListVariantImportJobsResponseTypeDef",
    "ListVariantStoresRequestListVariantStoresPaginateTypeDef",
    "ListVariantStoresRequestRequestTypeDef",
    "ListWorkflowsResponseTypeDef",
    "TsvOptionsTypeDef",
    "StartReadSetActivationJobRequestRequestTypeDef",
    "StartReferenceImportJobRequestRequestTypeDef",
    "StartVariantImportRequestRequestTypeDef",
    "StoreOptionsTypeDef",
    "ListAnnotationStoresResponseTypeDef",
    "ListReferenceStoresResponseTypeDef",
    "ListSequenceStoresResponseTypeDef",
    "ListVariantStoresResponseTypeDef",
    "GetReadSetMetadataResponseTypeDef",
    "GetReferenceMetadataResponseTypeDef",
    "ListReadSetsResponseTypeDef",
    "GetReadSetImportJobResponseTypeDef",
    "StartReadSetImportJobRequestRequestTypeDef",
    "FormatOptionsTypeDef",
    "CreateAnnotationStoreRequestRequestTypeDef",
    "CreateAnnotationStoreResponseTypeDef",
    "GetAnnotationStoreResponseTypeDef",
    "UpdateAnnotationStoreResponseTypeDef",
    "GetAnnotationImportResponseTypeDef",
    "StartAnnotationImportRequestRequestTypeDef",
)

ActivateReadSetFilterTypeDef = TypedDict(
    "ActivateReadSetFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "status": ReadSetActivationJobStatusType,
    },
    total=False,
)

_RequiredActivateReadSetJobItemTypeDef = TypedDict(
    "_RequiredActivateReadSetJobItemTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "sequenceStoreId": str,
        "status": ReadSetActivationJobStatusType,
    },
)
_OptionalActivateReadSetJobItemTypeDef = TypedDict(
    "_OptionalActivateReadSetJobItemTypeDef",
    {
        "completionTime": datetime,
    },
    total=False,
)

class ActivateReadSetJobItemTypeDef(
    _RequiredActivateReadSetJobItemTypeDef, _OptionalActivateReadSetJobItemTypeDef
):
    pass

_RequiredActivateReadSetSourceItemTypeDef = TypedDict(
    "_RequiredActivateReadSetSourceItemTypeDef",
    {
        "readSetId": str,
        "status": ReadSetActivationJobItemStatusType,
    },
)
_OptionalActivateReadSetSourceItemTypeDef = TypedDict(
    "_OptionalActivateReadSetSourceItemTypeDef",
    {
        "statusMessage": str,
    },
    total=False,
)

class ActivateReadSetSourceItemTypeDef(
    _RequiredActivateReadSetSourceItemTypeDef, _OptionalActivateReadSetSourceItemTypeDef
):
    pass

AnnotationImportItemDetailTypeDef = TypedDict(
    "AnnotationImportItemDetailTypeDef",
    {
        "jobStatus": JobStatusType,
        "source": str,
    },
)

AnnotationImportItemSourceTypeDef = TypedDict(
    "AnnotationImportItemSourceTypeDef",
    {
        "source": str,
    },
)

_RequiredAnnotationImportJobItemTypeDef = TypedDict(
    "_RequiredAnnotationImportJobItemTypeDef",
    {
        "creationTime": datetime,
        "destinationName": str,
        "id": str,
        "roleArn": str,
        "status": JobStatusType,
        "updateTime": datetime,
    },
)
_OptionalAnnotationImportJobItemTypeDef = TypedDict(
    "_OptionalAnnotationImportJobItemTypeDef",
    {
        "completionTime": datetime,
        "runLeftNormalization": bool,
    },
    total=False,
)

class AnnotationImportJobItemTypeDef(
    _RequiredAnnotationImportJobItemTypeDef, _OptionalAnnotationImportJobItemTypeDef
):
    pass

ReferenceItemTypeDef = TypedDict(
    "ReferenceItemTypeDef",
    {
        "referenceArn": str,
    },
    total=False,
)

_RequiredSseConfigTypeDef = TypedDict(
    "_RequiredSseConfigTypeDef",
    {
        "type": Literal["KMS"],
    },
)
_OptionalSseConfigTypeDef = TypedDict(
    "_OptionalSseConfigTypeDef",
    {
        "keyArn": str,
    },
    total=False,
)

class SseConfigTypeDef(_RequiredSseConfigTypeDef, _OptionalSseConfigTypeDef):
    pass

BatchDeleteReadSetRequestRequestTypeDef = TypedDict(
    "BatchDeleteReadSetRequestRequestTypeDef",
    {
        "ids": Sequence[str],
        "sequenceStoreId": str,
    },
)

ReadSetBatchErrorTypeDef = TypedDict(
    "ReadSetBatchErrorTypeDef",
    {
        "code": str,
        "id": str,
        "message": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

CancelAnnotationImportRequestRequestTypeDef = TypedDict(
    "CancelAnnotationImportRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

CancelRunRequestRequestTypeDef = TypedDict(
    "CancelRunRequestRequestTypeDef",
    {
        "id": str,
    },
)

CancelVariantImportRequestRequestTypeDef = TypedDict(
    "CancelVariantImportRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

_RequiredCreateRunGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRunGroupRequestRequestTypeDef",
    {
        "requestId": str,
    },
)
_OptionalCreateRunGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRunGroupRequestRequestTypeDef",
    {
        "maxCpus": int,
        "maxDuration": int,
        "maxRuns": int,
        "name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateRunGroupRequestRequestTypeDef(
    _RequiredCreateRunGroupRequestRequestTypeDef, _OptionalCreateRunGroupRequestRequestTypeDef
):
    pass

WorkflowParameterTypeDef = TypedDict(
    "WorkflowParameterTypeDef",
    {
        "description": str,
        "optional": bool,
    },
    total=False,
)

_RequiredDeleteAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAnnotationStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalDeleteAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAnnotationStoreRequestRequestTypeDef",
    {
        "force": bool,
    },
    total=False,
)

class DeleteAnnotationStoreRequestRequestTypeDef(
    _RequiredDeleteAnnotationStoreRequestRequestTypeDef,
    _OptionalDeleteAnnotationStoreRequestRequestTypeDef,
):
    pass

DeleteReferenceRequestRequestTypeDef = TypedDict(
    "DeleteReferenceRequestRequestTypeDef",
    {
        "id": str,
        "referenceStoreId": str,
    },
)

DeleteReferenceStoreRequestRequestTypeDef = TypedDict(
    "DeleteReferenceStoreRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteRunGroupRequestRequestTypeDef = TypedDict(
    "DeleteRunGroupRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteRunRequestRequestTypeDef = TypedDict(
    "DeleteRunRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteSequenceStoreRequestRequestTypeDef = TypedDict(
    "DeleteSequenceStoreRequestRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredDeleteVariantStoreRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteVariantStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalDeleteVariantStoreRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteVariantStoreRequestRequestTypeDef",
    {
        "force": bool,
    },
    total=False,
)

class DeleteVariantStoreRequestRequestTypeDef(
    _RequiredDeleteVariantStoreRequestRequestTypeDef,
    _OptionalDeleteVariantStoreRequestRequestTypeDef,
):
    pass

DeleteWorkflowRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredExportReadSetDetailTypeDef = TypedDict(
    "_RequiredExportReadSetDetailTypeDef",
    {
        "id": str,
        "status": ReadSetExportJobItemStatusType,
    },
)
_OptionalExportReadSetDetailTypeDef = TypedDict(
    "_OptionalExportReadSetDetailTypeDef",
    {
        "statusMessage": str,
    },
    total=False,
)

class ExportReadSetDetailTypeDef(
    _RequiredExportReadSetDetailTypeDef, _OptionalExportReadSetDetailTypeDef
):
    pass

ExportReadSetFilterTypeDef = TypedDict(
    "ExportReadSetFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "status": ReadSetExportJobStatusType,
    },
    total=False,
)

_RequiredExportReadSetJobDetailTypeDef = TypedDict(
    "_RequiredExportReadSetJobDetailTypeDef",
    {
        "creationTime": datetime,
        "destination": str,
        "id": str,
        "sequenceStoreId": str,
        "status": ReadSetExportJobStatusType,
    },
)
_OptionalExportReadSetJobDetailTypeDef = TypedDict(
    "_OptionalExportReadSetJobDetailTypeDef",
    {
        "completionTime": datetime,
    },
    total=False,
)

class ExportReadSetJobDetailTypeDef(
    _RequiredExportReadSetJobDetailTypeDef, _OptionalExportReadSetJobDetailTypeDef
):
    pass

ExportReadSetTypeDef = TypedDict(
    "ExportReadSetTypeDef",
    {
        "readSetId": str,
    },
)

FileInformationTypeDef = TypedDict(
    "FileInformationTypeDef",
    {
        "contentLength": int,
        "partSize": int,
        "totalParts": int,
    },
    total=False,
)

VcfOptionsTypeDef = TypedDict(
    "VcfOptionsTypeDef",
    {
        "ignoreFilterField": bool,
        "ignoreQualField": bool,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

GetAnnotationImportRequestRequestTypeDef = TypedDict(
    "GetAnnotationImportRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

GetAnnotationStoreRequestRequestTypeDef = TypedDict(
    "GetAnnotationStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)

GetReadSetActivationJobRequestRequestTypeDef = TypedDict(
    "GetReadSetActivationJobRequestRequestTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)

GetReadSetExportJobRequestRequestTypeDef = TypedDict(
    "GetReadSetExportJobRequestRequestTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)

GetReadSetImportJobRequestRequestTypeDef = TypedDict(
    "GetReadSetImportJobRequestRequestTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)

GetReadSetMetadataRequestRequestTypeDef = TypedDict(
    "GetReadSetMetadataRequestRequestTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)

SequenceInformationTypeDef = TypedDict(
    "SequenceInformationTypeDef",
    {
        "alignment": str,
        "generatedFrom": str,
        "totalBaseCount": int,
        "totalReadCount": int,
    },
    total=False,
)

_RequiredGetReadSetRequestRequestTypeDef = TypedDict(
    "_RequiredGetReadSetRequestRequestTypeDef",
    {
        "id": str,
        "partNumber": int,
        "sequenceStoreId": str,
    },
)
_OptionalGetReadSetRequestRequestTypeDef = TypedDict(
    "_OptionalGetReadSetRequestRequestTypeDef",
    {
        "file": ReadSetFileType,
    },
    total=False,
)

class GetReadSetRequestRequestTypeDef(
    _RequiredGetReadSetRequestRequestTypeDef, _OptionalGetReadSetRequestRequestTypeDef
):
    pass

GetReferenceImportJobRequestRequestTypeDef = TypedDict(
    "GetReferenceImportJobRequestRequestTypeDef",
    {
        "id": str,
        "referenceStoreId": str,
    },
)

_RequiredImportReferenceSourceItemTypeDef = TypedDict(
    "_RequiredImportReferenceSourceItemTypeDef",
    {
        "status": ReferenceImportJobItemStatusType,
    },
)
_OptionalImportReferenceSourceItemTypeDef = TypedDict(
    "_OptionalImportReferenceSourceItemTypeDef",
    {
        "description": str,
        "name": str,
        "sourceFile": str,
        "statusMessage": str,
        "tags": Dict[str, str],
    },
    total=False,
)

class ImportReferenceSourceItemTypeDef(
    _RequiredImportReferenceSourceItemTypeDef, _OptionalImportReferenceSourceItemTypeDef
):
    pass

GetReferenceMetadataRequestRequestTypeDef = TypedDict(
    "GetReferenceMetadataRequestRequestTypeDef",
    {
        "id": str,
        "referenceStoreId": str,
    },
)

_RequiredGetReferenceRequestRequestTypeDef = TypedDict(
    "_RequiredGetReferenceRequestRequestTypeDef",
    {
        "id": str,
        "partNumber": int,
        "referenceStoreId": str,
    },
)
_OptionalGetReferenceRequestRequestTypeDef = TypedDict(
    "_OptionalGetReferenceRequestRequestTypeDef",
    {
        "file": ReferenceFileType,
        "range": str,
    },
    total=False,
)

class GetReferenceRequestRequestTypeDef(
    _RequiredGetReferenceRequestRequestTypeDef, _OptionalGetReferenceRequestRequestTypeDef
):
    pass

GetReferenceStoreRequestRequestTypeDef = TypedDict(
    "GetReferenceStoreRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetRunGroupRequestRequestTypeDef = TypedDict(
    "GetRunGroupRequestRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredGetRunRequestRequestTypeDef = TypedDict(
    "_RequiredGetRunRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetRunRequestRequestTypeDef = TypedDict(
    "_OptionalGetRunRequestRequestTypeDef",
    {
        "export": Sequence[Literal["DEFINITION"]],
    },
    total=False,
)

class GetRunRequestRequestTypeDef(
    _RequiredGetRunRequestRequestTypeDef, _OptionalGetRunRequestRequestTypeDef
):
    pass

GetRunTaskRequestRequestTypeDef = TypedDict(
    "GetRunTaskRequestRequestTypeDef",
    {
        "id": str,
        "taskId": str,
    },
)

GetSequenceStoreRequestRequestTypeDef = TypedDict(
    "GetSequenceStoreRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetVariantImportRequestRequestTypeDef = TypedDict(
    "GetVariantImportRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

_RequiredVariantImportItemDetailTypeDef = TypedDict(
    "_RequiredVariantImportItemDetailTypeDef",
    {
        "jobStatus": JobStatusType,
        "source": str,
    },
)
_OptionalVariantImportItemDetailTypeDef = TypedDict(
    "_OptionalVariantImportItemDetailTypeDef",
    {
        "statusMessage": str,
    },
    total=False,
)

class VariantImportItemDetailTypeDef(
    _RequiredVariantImportItemDetailTypeDef, _OptionalVariantImportItemDetailTypeDef
):
    pass

GetVariantStoreRequestRequestTypeDef = TypedDict(
    "GetVariantStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)

_RequiredGetWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredGetWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalGetWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalGetWorkflowRequestRequestTypeDef",
    {
        "export": Sequence[Literal["DEFINITION"]],
        "type": WorkflowTypeType,
    },
    total=False,
)

class GetWorkflowRequestRequestTypeDef(
    _RequiredGetWorkflowRequestRequestTypeDef, _OptionalGetWorkflowRequestRequestTypeDef
):
    pass

ImportReadSetFilterTypeDef = TypedDict(
    "ImportReadSetFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "status": ReadSetImportJobStatusType,
    },
    total=False,
)

_RequiredImportReadSetJobItemTypeDef = TypedDict(
    "_RequiredImportReadSetJobItemTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "roleArn": str,
        "sequenceStoreId": str,
        "status": ReadSetImportJobStatusType,
    },
)
_OptionalImportReadSetJobItemTypeDef = TypedDict(
    "_OptionalImportReadSetJobItemTypeDef",
    {
        "completionTime": datetime,
    },
    total=False,
)

class ImportReadSetJobItemTypeDef(
    _RequiredImportReadSetJobItemTypeDef, _OptionalImportReadSetJobItemTypeDef
):
    pass

_RequiredSourceFilesTypeDef = TypedDict(
    "_RequiredSourceFilesTypeDef",
    {
        "source1": str,
    },
)
_OptionalSourceFilesTypeDef = TypedDict(
    "_OptionalSourceFilesTypeDef",
    {
        "source2": str,
    },
    total=False,
)

class SourceFilesTypeDef(_RequiredSourceFilesTypeDef, _OptionalSourceFilesTypeDef):
    pass

ImportReferenceFilterTypeDef = TypedDict(
    "ImportReferenceFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "status": ReferenceImportJobStatusType,
    },
    total=False,
)

_RequiredImportReferenceJobItemTypeDef = TypedDict(
    "_RequiredImportReferenceJobItemTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "referenceStoreId": str,
        "roleArn": str,
        "status": ReferenceImportJobStatusType,
    },
)
_OptionalImportReferenceJobItemTypeDef = TypedDict(
    "_OptionalImportReferenceJobItemTypeDef",
    {
        "completionTime": datetime,
    },
    total=False,
)

class ImportReferenceJobItemTypeDef(
    _RequiredImportReferenceJobItemTypeDef, _OptionalImportReferenceJobItemTypeDef
):
    pass

ListAnnotationImportJobsFilterTypeDef = TypedDict(
    "ListAnnotationImportJobsFilterTypeDef",
    {
        "status": JobStatusType,
        "storeName": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListAnnotationStoresFilterTypeDef = TypedDict(
    "ListAnnotationStoresFilterTypeDef",
    {
        "status": StoreStatusType,
    },
    total=False,
)

ReadSetFilterTypeDef = TypedDict(
    "ReadSetFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "name": str,
        "referenceArn": str,
        "status": ReadSetStatusType,
    },
    total=False,
)

ReferenceStoreFilterTypeDef = TypedDict(
    "ReferenceStoreFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "name": str,
    },
    total=False,
)

ReferenceFilterTypeDef = TypedDict(
    "ReferenceFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "md5": str,
        "name": str,
    },
    total=False,
)

_RequiredReferenceListItemTypeDef = TypedDict(
    "_RequiredReferenceListItemTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
        "md5": str,
        "referenceStoreId": str,
        "updateTime": datetime,
    },
)
_OptionalReferenceListItemTypeDef = TypedDict(
    "_OptionalReferenceListItemTypeDef",
    {
        "description": str,
        "name": str,
        "status": ReferenceStatusType,
    },
    total=False,
)

class ReferenceListItemTypeDef(
    _RequiredReferenceListItemTypeDef, _OptionalReferenceListItemTypeDef
):
    pass

ListRunGroupsRequestRequestTypeDef = TypedDict(
    "ListRunGroupsRequestRequestTypeDef",
    {
        "maxResults": int,
        "name": str,
        "startingToken": str,
    },
    total=False,
)

RunGroupListItemTypeDef = TypedDict(
    "RunGroupListItemTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
        "maxCpus": int,
        "maxDuration": int,
        "maxRuns": int,
        "name": str,
    },
    total=False,
)

_RequiredListRunTasksRequestRequestTypeDef = TypedDict(
    "_RequiredListRunTasksRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalListRunTasksRequestRequestTypeDef = TypedDict(
    "_OptionalListRunTasksRequestRequestTypeDef",
    {
        "maxResults": int,
        "startingToken": str,
        "status": TaskStatusType,
    },
    total=False,
)

class ListRunTasksRequestRequestTypeDef(
    _RequiredListRunTasksRequestRequestTypeDef, _OptionalListRunTasksRequestRequestTypeDef
):
    pass

TaskListItemTypeDef = TypedDict(
    "TaskListItemTypeDef",
    {
        "cpus": int,
        "creationTime": datetime,
        "memory": int,
        "name": str,
        "startTime": datetime,
        "status": TaskStatusType,
        "stopTime": datetime,
        "taskId": str,
    },
    total=False,
)

ListRunsRequestRequestTypeDef = TypedDict(
    "ListRunsRequestRequestTypeDef",
    {
        "maxResults": int,
        "name": str,
        "runGroupId": str,
        "startingToken": str,
    },
    total=False,
)

RunListItemTypeDef = TypedDict(
    "RunListItemTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
        "name": str,
        "priority": int,
        "startTime": datetime,
        "status": RunStatusType,
        "stopTime": datetime,
        "storageCapacity": int,
        "workflowId": str,
    },
    total=False,
)

SequenceStoreFilterTypeDef = TypedDict(
    "SequenceStoreFilterTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "name": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListVariantImportJobsFilterTypeDef = TypedDict(
    "ListVariantImportJobsFilterTypeDef",
    {
        "status": JobStatusType,
        "storeName": str,
    },
    total=False,
)

_RequiredVariantImportJobItemTypeDef = TypedDict(
    "_RequiredVariantImportJobItemTypeDef",
    {
        "creationTime": datetime,
        "destinationName": str,
        "id": str,
        "roleArn": str,
        "status": JobStatusType,
        "updateTime": datetime,
    },
)
_OptionalVariantImportJobItemTypeDef = TypedDict(
    "_OptionalVariantImportJobItemTypeDef",
    {
        "completionTime": datetime,
        "runLeftNormalization": bool,
    },
    total=False,
)

class VariantImportJobItemTypeDef(
    _RequiredVariantImportJobItemTypeDef, _OptionalVariantImportJobItemTypeDef
):
    pass

ListVariantStoresFilterTypeDef = TypedDict(
    "ListVariantStoresFilterTypeDef",
    {
        "status": StoreStatusType,
    },
    total=False,
)

ListWorkflowsRequestRequestTypeDef = TypedDict(
    "ListWorkflowsRequestRequestTypeDef",
    {
        "maxResults": int,
        "name": str,
        "startingToken": str,
        "type": WorkflowTypeType,
    },
    total=False,
)

WorkflowListItemTypeDef = TypedDict(
    "WorkflowListItemTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "digest": str,
        "id": str,
        "name": str,
        "status": WorkflowStatusType,
        "type": WorkflowTypeType,
    },
    total=False,
)

ReadOptionsTypeDef = TypedDict(
    "ReadOptionsTypeDef",
    {
        "comment": str,
        "encoding": str,
        "escape": str,
        "escapeQuotes": bool,
        "header": bool,
        "lineSep": str,
        "quote": str,
        "quoteAll": bool,
        "sep": str,
    },
    total=False,
)

StartReadSetActivationJobSourceItemTypeDef = TypedDict(
    "StartReadSetActivationJobSourceItemTypeDef",
    {
        "readSetId": str,
    },
)

_RequiredStartReferenceImportJobSourceItemTypeDef = TypedDict(
    "_RequiredStartReferenceImportJobSourceItemTypeDef",
    {
        "name": str,
        "sourceFile": str,
    },
)
_OptionalStartReferenceImportJobSourceItemTypeDef = TypedDict(
    "_OptionalStartReferenceImportJobSourceItemTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class StartReferenceImportJobSourceItemTypeDef(
    _RequiredStartReferenceImportJobSourceItemTypeDef,
    _OptionalStartReferenceImportJobSourceItemTypeDef,
):
    pass

_RequiredStartRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartRunRequestRequestTypeDef",
    {
        "requestId": str,
        "roleArn": str,
    },
)
_OptionalStartRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartRunRequestRequestTypeDef",
    {
        "logLevel": RunLogLevelType,
        "name": str,
        "outputUri": str,
        "parameters": Mapping[str, Any],
        "priority": int,
        "runGroupId": str,
        "runId": str,
        "storageCapacity": int,
        "tags": Mapping[str, str],
        "workflowId": str,
        "workflowType": WorkflowTypeType,
    },
    total=False,
)

class StartRunRequestRequestTypeDef(
    _RequiredStartRunRequestRequestTypeDef, _OptionalStartRunRequestRequestTypeDef
):
    pass

VariantImportItemSourceTypeDef = TypedDict(
    "VariantImportItemSourceTypeDef",
    {
        "source": str,
    },
)

TsvStoreOptionsTypeDef = TypedDict(
    "TsvStoreOptionsTypeDef",
    {
        "annotationType": AnnotationTypeType,
        "formatToHeader": Mapping[FormatToHeaderKeyType, str],
        "schema": Sequence[Mapping[str, SchemaValueTypeType]],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnnotationStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnnotationStoreRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateAnnotationStoreRequestRequestTypeDef(
    _RequiredUpdateAnnotationStoreRequestRequestTypeDef,
    _OptionalUpdateAnnotationStoreRequestRequestTypeDef,
):
    pass

_RequiredUpdateRunGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRunGroupRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateRunGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRunGroupRequestRequestTypeDef",
    {
        "maxCpus": int,
        "maxDuration": int,
        "maxRuns": int,
        "name": str,
    },
    total=False,
)

class UpdateRunGroupRequestRequestTypeDef(
    _RequiredUpdateRunGroupRequestRequestTypeDef, _OptionalUpdateRunGroupRequestRequestTypeDef
):
    pass

_RequiredUpdateVariantStoreRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVariantStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateVariantStoreRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVariantStoreRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateVariantStoreRequestRequestTypeDef(
    _RequiredUpdateVariantStoreRequestRequestTypeDef,
    _OptionalUpdateVariantStoreRequestRequestTypeDef,
):
    pass

_RequiredUpdateWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkflowRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
    },
    total=False,
)

class UpdateWorkflowRequestRequestTypeDef(
    _RequiredUpdateWorkflowRequestRequestTypeDef, _OptionalUpdateWorkflowRequestRequestTypeDef
):
    pass

_RequiredListReadSetActivationJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListReadSetActivationJobsRequestRequestTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetActivationJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListReadSetActivationJobsRequestRequestTypeDef",
    {
        "filter": ActivateReadSetFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReadSetActivationJobsRequestRequestTypeDef(
    _RequiredListReadSetActivationJobsRequestRequestTypeDef,
    _OptionalListReadSetActivationJobsRequestRequestTypeDef,
):
    pass

AnnotationStoreItemTypeDef = TypedDict(
    "AnnotationStoreItemTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "sseConfig": SseConfigTypeDef,
        "status": StoreStatusType,
        "statusMessage": str,
        "storeArn": str,
        "storeFormat": StoreFormatType,
        "storeSizeBytes": int,
        "updateTime": datetime,
    },
)

_RequiredCreateReferenceStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReferenceStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateReferenceStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReferenceStoreRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "sseConfig": SseConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateReferenceStoreRequestRequestTypeDef(
    _RequiredCreateReferenceStoreRequestRequestTypeDef,
    _OptionalCreateReferenceStoreRequestRequestTypeDef,
):
    pass

_RequiredCreateSequenceStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSequenceStoreRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateSequenceStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSequenceStoreRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "sseConfig": SseConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateSequenceStoreRequestRequestTypeDef(
    _RequiredCreateSequenceStoreRequestRequestTypeDef,
    _OptionalCreateSequenceStoreRequestRequestTypeDef,
):
    pass

_RequiredCreateVariantStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVariantStoreRequestRequestTypeDef",
    {
        "reference": ReferenceItemTypeDef,
    },
)
_OptionalCreateVariantStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVariantStoreRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateVariantStoreRequestRequestTypeDef(
    _RequiredCreateVariantStoreRequestRequestTypeDef,
    _OptionalCreateVariantStoreRequestRequestTypeDef,
):
    pass

_RequiredReferenceStoreDetailTypeDef = TypedDict(
    "_RequiredReferenceStoreDetailTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
    },
)
_OptionalReferenceStoreDetailTypeDef = TypedDict(
    "_OptionalReferenceStoreDetailTypeDef",
    {
        "description": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
    },
    total=False,
)

class ReferenceStoreDetailTypeDef(
    _RequiredReferenceStoreDetailTypeDef, _OptionalReferenceStoreDetailTypeDef
):
    pass

_RequiredSequenceStoreDetailTypeDef = TypedDict(
    "_RequiredSequenceStoreDetailTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
    },
)
_OptionalSequenceStoreDetailTypeDef = TypedDict(
    "_OptionalSequenceStoreDetailTypeDef",
    {
        "description": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
    },
    total=False,
)

class SequenceStoreDetailTypeDef(
    _RequiredSequenceStoreDetailTypeDef, _OptionalSequenceStoreDetailTypeDef
):
    pass

VariantStoreItemTypeDef = TypedDict(
    "VariantStoreItemTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "sseConfig": SseConfigTypeDef,
        "status": StoreStatusType,
        "statusMessage": str,
        "storeArn": str,
        "storeSizeBytes": int,
        "updateTime": datetime,
    },
)

BatchDeleteReadSetResponseTypeDef = TypedDict(
    "BatchDeleteReadSetResponseTypeDef",
    {
        "errors": List[ReadSetBatchErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateReferenceStoreResponseTypeDef = TypedDict(
    "CreateReferenceStoreResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRunGroupResponseTypeDef = TypedDict(
    "CreateRunGroupResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSequenceStoreResponseTypeDef = TypedDict(
    "CreateSequenceStoreResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVariantStoreResponseTypeDef = TypedDict(
    "CreateVariantStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "status": StoreStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkflowResponseTypeDef = TypedDict(
    "CreateWorkflowResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": WorkflowStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAnnotationStoreResponseTypeDef = TypedDict(
    "DeleteAnnotationStoreResponseTypeDef",
    {
        "status": StoreStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVariantStoreResponseTypeDef = TypedDict(
    "DeleteVariantStoreResponseTypeDef",
    {
        "status": StoreStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadSetActivationJobResponseTypeDef = TypedDict(
    "GetReadSetActivationJobResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "id": str,
        "sequenceStoreId": str,
        "sources": List[ActivateReadSetSourceItemTypeDef],
        "status": ReadSetActivationJobStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadSetResponseTypeDef = TypedDict(
    "GetReadSetResponseTypeDef",
    {
        "payload": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReferenceResponseTypeDef = TypedDict(
    "GetReferenceResponseTypeDef",
    {
        "payload": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReferenceStoreResponseTypeDef = TypedDict(
    "GetReferenceStoreResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRunGroupResponseTypeDef = TypedDict(
    "GetRunGroupResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "id": str,
        "maxCpus": int,
        "maxDuration": int,
        "maxRuns": int,
        "name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRunResponseTypeDef = TypedDict(
    "GetRunResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "definition": str,
        "digest": str,
        "id": str,
        "logLevel": RunLogLevelType,
        "name": str,
        "outputUri": str,
        "parameters": Dict[str, Any],
        "priority": int,
        "resourceDigests": Dict[str, str],
        "roleArn": str,
        "runGroupId": str,
        "runId": str,
        "startTime": datetime,
        "startedBy": str,
        "status": RunStatusType,
        "statusMessage": str,
        "stopTime": datetime,
        "storageCapacity": int,
        "tags": Dict[str, str],
        "workflowId": str,
        "workflowType": WorkflowTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRunTaskResponseTypeDef = TypedDict(
    "GetRunTaskResponseTypeDef",
    {
        "cpus": int,
        "creationTime": datetime,
        "logStream": str,
        "memory": int,
        "name": str,
        "startTime": datetime,
        "status": TaskStatusType,
        "statusMessage": str,
        "stopTime": datetime,
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSequenceStoreResponseTypeDef = TypedDict(
    "GetSequenceStoreResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "sseConfig": SseConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVariantStoreResponseTypeDef = TypedDict(
    "GetVariantStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "sseConfig": SseConfigTypeDef,
        "status": StoreStatusType,
        "statusMessage": str,
        "storeArn": str,
        "storeSizeBytes": int,
        "tags": Dict[str, str],
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnnotationImportJobsResponseTypeDef = TypedDict(
    "ListAnnotationImportJobsResponseTypeDef",
    {
        "annotationImportJobs": List[AnnotationImportJobItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReadSetActivationJobsResponseTypeDef = TypedDict(
    "ListReadSetActivationJobsResponseTypeDef",
    {
        "activationJobs": List[ActivateReadSetJobItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAnnotationImportResponseTypeDef = TypedDict(
    "StartAnnotationImportResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartReadSetActivationJobResponseTypeDef = TypedDict(
    "StartReadSetActivationJobResponseTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "sequenceStoreId": str,
        "status": ReadSetActivationJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartReadSetExportJobResponseTypeDef = TypedDict(
    "StartReadSetExportJobResponseTypeDef",
    {
        "creationTime": datetime,
        "destination": str,
        "id": str,
        "sequenceStoreId": str,
        "status": ReadSetExportJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartReadSetImportJobResponseTypeDef = TypedDict(
    "StartReadSetImportJobResponseTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "roleArn": str,
        "sequenceStoreId": str,
        "status": ReadSetImportJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartReferenceImportJobResponseTypeDef = TypedDict(
    "StartReferenceImportJobResponseTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "referenceStoreId": str,
        "roleArn": str,
        "status": ReferenceImportJobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartRunResponseTypeDef = TypedDict(
    "StartRunResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": RunStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartVariantImportResponseTypeDef = TypedDict(
    "StartVariantImportResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVariantStoreResponseTypeDef = TypedDict(
    "UpdateVariantStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "status": StoreStatusType,
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkflowRequestRequestTypeDef",
    {
        "requestId": str,
    },
)
_OptionalCreateWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkflowRequestRequestTypeDef",
    {
        "definitionUri": str,
        "definitionZip": Union[str, bytes, IO[Any], StreamingBody],
        "description": str,
        "engine": WorkflowEngineType,
        "main": str,
        "name": str,
        "parameterTemplate": Mapping[str, WorkflowParameterTypeDef],
        "storageCapacity": int,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateWorkflowRequestRequestTypeDef(
    _RequiredCreateWorkflowRequestRequestTypeDef, _OptionalCreateWorkflowRequestRequestTypeDef
):
    pass

GetWorkflowResponseTypeDef = TypedDict(
    "GetWorkflowResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "definition": str,
        "description": str,
        "digest": str,
        "engine": WorkflowEngineType,
        "id": str,
        "main": str,
        "name": str,
        "parameterTemplate": Dict[str, WorkflowParameterTypeDef],
        "status": WorkflowStatusType,
        "statusMessage": str,
        "storageCapacity": int,
        "tags": Dict[str, str],
        "type": WorkflowTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadSetExportJobResponseTypeDef = TypedDict(
    "GetReadSetExportJobResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "destination": str,
        "id": str,
        "readSets": List[ExportReadSetDetailTypeDef],
        "sequenceStoreId": str,
        "status": ReadSetExportJobStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListReadSetExportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListReadSetExportJobsRequestRequestTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetExportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListReadSetExportJobsRequestRequestTypeDef",
    {
        "filter": ExportReadSetFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReadSetExportJobsRequestRequestTypeDef(
    _RequiredListReadSetExportJobsRequestRequestTypeDef,
    _OptionalListReadSetExportJobsRequestRequestTypeDef,
):
    pass

ListReadSetExportJobsResponseTypeDef = TypedDict(
    "ListReadSetExportJobsResponseTypeDef",
    {
        "exportJobs": List[ExportReadSetJobDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartReadSetExportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartReadSetExportJobRequestRequestTypeDef",
    {
        "destination": str,
        "roleArn": str,
        "sequenceStoreId": str,
        "sources": Sequence[ExportReadSetTypeDef],
    },
)
_OptionalStartReadSetExportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartReadSetExportJobRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class StartReadSetExportJobRequestRequestTypeDef(
    _RequiredStartReadSetExportJobRequestRequestTypeDef,
    _OptionalStartReadSetExportJobRequestRequestTypeDef,
):
    pass

ReadSetFilesTypeDef = TypedDict(
    "ReadSetFilesTypeDef",
    {
        "index": FileInformationTypeDef,
        "source1": FileInformationTypeDef,
        "source2": FileInformationTypeDef,
    },
    total=False,
)

ReferenceFilesTypeDef = TypedDict(
    "ReferenceFilesTypeDef",
    {
        "index": FileInformationTypeDef,
        "source": FileInformationTypeDef,
    },
    total=False,
)

_RequiredGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef = TypedDict(
    "_RequiredGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef",
    {
        "jobId": str,
    },
)
_OptionalGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef = TypedDict(
    "_OptionalGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef(
    _RequiredGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef,
    _OptionalGetAnnotationImportRequestAnnotationImportJobCreatedWaitTypeDef,
):
    pass

_RequiredGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef = TypedDict(
    "_RequiredGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef = TypedDict(
    "_OptionalGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef(
    _RequiredGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef,
    _OptionalGetAnnotationStoreRequestAnnotationStoreCreatedWaitTypeDef,
):
    pass

_RequiredGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef = TypedDict(
    "_RequiredGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef = TypedDict(
    "_OptionalGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef(
    _RequiredGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef,
    _OptionalGetAnnotationStoreRequestAnnotationStoreDeletedWaitTypeDef,
):
    pass

_RequiredGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef = TypedDict(
    "_RequiredGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)
_OptionalGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef = TypedDict(
    "_OptionalGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef(
    _RequiredGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef,
    _OptionalGetReadSetActivationJobRequestReadSetActivationJobCompletedWaitTypeDef,
):
    pass

_RequiredGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef = TypedDict(
    "_RequiredGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)
_OptionalGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef = TypedDict(
    "_OptionalGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef(
    _RequiredGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef,
    _OptionalGetReadSetExportJobRequestReadSetExportJobCompletedWaitTypeDef,
):
    pass

_RequiredGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef = TypedDict(
    "_RequiredGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef",
    {
        "id": str,
        "sequenceStoreId": str,
    },
)
_OptionalGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef = TypedDict(
    "_OptionalGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef(
    _RequiredGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef,
    _OptionalGetReadSetImportJobRequestReadSetImportJobCompletedWaitTypeDef,
):
    pass

_RequiredGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef = TypedDict(
    "_RequiredGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef",
    {
        "id": str,
        "referenceStoreId": str,
    },
)
_OptionalGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef = TypedDict(
    "_OptionalGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef(
    _RequiredGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef,
    _OptionalGetReferenceImportJobRequestReferenceImportJobCompletedWaitTypeDef,
):
    pass

_RequiredGetRunRequestRunCompletedWaitTypeDef = TypedDict(
    "_RequiredGetRunRequestRunCompletedWaitTypeDef",
    {
        "id": str,
    },
)
_OptionalGetRunRequestRunCompletedWaitTypeDef = TypedDict(
    "_OptionalGetRunRequestRunCompletedWaitTypeDef",
    {
        "export": Sequence[Literal["DEFINITION"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetRunRequestRunCompletedWaitTypeDef(
    _RequiredGetRunRequestRunCompletedWaitTypeDef, _OptionalGetRunRequestRunCompletedWaitTypeDef
):
    pass

_RequiredGetRunRequestRunRunningWaitTypeDef = TypedDict(
    "_RequiredGetRunRequestRunRunningWaitTypeDef",
    {
        "id": str,
    },
)
_OptionalGetRunRequestRunRunningWaitTypeDef = TypedDict(
    "_OptionalGetRunRequestRunRunningWaitTypeDef",
    {
        "export": Sequence[Literal["DEFINITION"]],
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetRunRequestRunRunningWaitTypeDef(
    _RequiredGetRunRequestRunRunningWaitTypeDef, _OptionalGetRunRequestRunRunningWaitTypeDef
):
    pass

_RequiredGetRunTaskRequestTaskCompletedWaitTypeDef = TypedDict(
    "_RequiredGetRunTaskRequestTaskCompletedWaitTypeDef",
    {
        "id": str,
        "taskId": str,
    },
)
_OptionalGetRunTaskRequestTaskCompletedWaitTypeDef = TypedDict(
    "_OptionalGetRunTaskRequestTaskCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetRunTaskRequestTaskCompletedWaitTypeDef(
    _RequiredGetRunTaskRequestTaskCompletedWaitTypeDef,
    _OptionalGetRunTaskRequestTaskCompletedWaitTypeDef,
):
    pass

_RequiredGetRunTaskRequestTaskRunningWaitTypeDef = TypedDict(
    "_RequiredGetRunTaskRequestTaskRunningWaitTypeDef",
    {
        "id": str,
        "taskId": str,
    },
)
_OptionalGetRunTaskRequestTaskRunningWaitTypeDef = TypedDict(
    "_OptionalGetRunTaskRequestTaskRunningWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetRunTaskRequestTaskRunningWaitTypeDef(
    _RequiredGetRunTaskRequestTaskRunningWaitTypeDef,
    _OptionalGetRunTaskRequestTaskRunningWaitTypeDef,
):
    pass

_RequiredGetVariantImportRequestVariantImportJobCreatedWaitTypeDef = TypedDict(
    "_RequiredGetVariantImportRequestVariantImportJobCreatedWaitTypeDef",
    {
        "jobId": str,
    },
)
_OptionalGetVariantImportRequestVariantImportJobCreatedWaitTypeDef = TypedDict(
    "_OptionalGetVariantImportRequestVariantImportJobCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetVariantImportRequestVariantImportJobCreatedWaitTypeDef(
    _RequiredGetVariantImportRequestVariantImportJobCreatedWaitTypeDef,
    _OptionalGetVariantImportRequestVariantImportJobCreatedWaitTypeDef,
):
    pass

_RequiredGetVariantStoreRequestVariantStoreCreatedWaitTypeDef = TypedDict(
    "_RequiredGetVariantStoreRequestVariantStoreCreatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetVariantStoreRequestVariantStoreCreatedWaitTypeDef = TypedDict(
    "_OptionalGetVariantStoreRequestVariantStoreCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetVariantStoreRequestVariantStoreCreatedWaitTypeDef(
    _RequiredGetVariantStoreRequestVariantStoreCreatedWaitTypeDef,
    _OptionalGetVariantStoreRequestVariantStoreCreatedWaitTypeDef,
):
    pass

_RequiredGetVariantStoreRequestVariantStoreDeletedWaitTypeDef = TypedDict(
    "_RequiredGetVariantStoreRequestVariantStoreDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetVariantStoreRequestVariantStoreDeletedWaitTypeDef = TypedDict(
    "_OptionalGetVariantStoreRequestVariantStoreDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetVariantStoreRequestVariantStoreDeletedWaitTypeDef(
    _RequiredGetVariantStoreRequestVariantStoreDeletedWaitTypeDef,
    _OptionalGetVariantStoreRequestVariantStoreDeletedWaitTypeDef,
):
    pass

_RequiredGetWorkflowRequestWorkflowActiveWaitTypeDef = TypedDict(
    "_RequiredGetWorkflowRequestWorkflowActiveWaitTypeDef",
    {
        "id": str,
    },
)
_OptionalGetWorkflowRequestWorkflowActiveWaitTypeDef = TypedDict(
    "_OptionalGetWorkflowRequestWorkflowActiveWaitTypeDef",
    {
        "export": Sequence[Literal["DEFINITION"]],
        "type": WorkflowTypeType,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class GetWorkflowRequestWorkflowActiveWaitTypeDef(
    _RequiredGetWorkflowRequestWorkflowActiveWaitTypeDef,
    _OptionalGetWorkflowRequestWorkflowActiveWaitTypeDef,
):
    pass

_RequiredReadSetListItemTypeDef = TypedDict(
    "_RequiredReadSetListItemTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "fileType": FileTypeType,
        "id": str,
        "sequenceStoreId": str,
        "status": ReadSetStatusType,
    },
)
_OptionalReadSetListItemTypeDef = TypedDict(
    "_OptionalReadSetListItemTypeDef",
    {
        "description": str,
        "name": str,
        "referenceArn": str,
        "sampleId": str,
        "sequenceInformation": SequenceInformationTypeDef,
        "subjectId": str,
    },
    total=False,
)

class ReadSetListItemTypeDef(_RequiredReadSetListItemTypeDef, _OptionalReadSetListItemTypeDef):
    pass

GetReferenceImportJobResponseTypeDef = TypedDict(
    "GetReferenceImportJobResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "id": str,
        "referenceStoreId": str,
        "roleArn": str,
        "sources": List[ImportReferenceSourceItemTypeDef],
        "status": ReferenceImportJobStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVariantImportResponseTypeDef = TypedDict(
    "GetVariantImportResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "destinationName": str,
        "id": str,
        "items": List[VariantImportItemDetailTypeDef],
        "roleArn": str,
        "runLeftNormalization": bool,
        "status": JobStatusType,
        "statusMessage": str,
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListReadSetImportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListReadSetImportJobsRequestRequestTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetImportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListReadSetImportJobsRequestRequestTypeDef",
    {
        "filter": ImportReadSetFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReadSetImportJobsRequestRequestTypeDef(
    _RequiredListReadSetImportJobsRequestRequestTypeDef,
    _OptionalListReadSetImportJobsRequestRequestTypeDef,
):
    pass

ListReadSetImportJobsResponseTypeDef = TypedDict(
    "ListReadSetImportJobsResponseTypeDef",
    {
        "importJobs": List[ImportReadSetJobItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImportReadSetSourceItemTypeDef = TypedDict(
    "_RequiredImportReadSetSourceItemTypeDef",
    {
        "sampleId": str,
        "sourceFileType": FileTypeType,
        "sourceFiles": SourceFilesTypeDef,
        "status": ReadSetImportJobItemStatusType,
        "subjectId": str,
    },
)
_OptionalImportReadSetSourceItemTypeDef = TypedDict(
    "_OptionalImportReadSetSourceItemTypeDef",
    {
        "description": str,
        "generatedFrom": str,
        "name": str,
        "referenceArn": str,
        "statusMessage": str,
        "tags": Dict[str, str],
    },
    total=False,
)

class ImportReadSetSourceItemTypeDef(
    _RequiredImportReadSetSourceItemTypeDef, _OptionalImportReadSetSourceItemTypeDef
):
    pass

_RequiredStartReadSetImportJobSourceItemTypeDef = TypedDict(
    "_RequiredStartReadSetImportJobSourceItemTypeDef",
    {
        "referenceArn": str,
        "sampleId": str,
        "sourceFileType": FileTypeType,
        "sourceFiles": SourceFilesTypeDef,
        "subjectId": str,
    },
)
_OptionalStartReadSetImportJobSourceItemTypeDef = TypedDict(
    "_OptionalStartReadSetImportJobSourceItemTypeDef",
    {
        "description": str,
        "generatedFrom": str,
        "name": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class StartReadSetImportJobSourceItemTypeDef(
    _RequiredStartReadSetImportJobSourceItemTypeDef, _OptionalStartReadSetImportJobSourceItemTypeDef
):
    pass

_RequiredListReferenceImportJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListReferenceImportJobsRequestRequestTypeDef",
    {
        "referenceStoreId": str,
    },
)
_OptionalListReferenceImportJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListReferenceImportJobsRequestRequestTypeDef",
    {
        "filter": ImportReferenceFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReferenceImportJobsRequestRequestTypeDef(
    _RequiredListReferenceImportJobsRequestRequestTypeDef,
    _OptionalListReferenceImportJobsRequestRequestTypeDef,
):
    pass

ListReferenceImportJobsResponseTypeDef = TypedDict(
    "ListReferenceImportJobsResponseTypeDef",
    {
        "importJobs": List[ImportReferenceJobItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnnotationImportJobsRequestRequestTypeDef = TypedDict(
    "ListAnnotationImportJobsRequestRequestTypeDef",
    {
        "filter": ListAnnotationImportJobsFilterTypeDef,
        "ids": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef = TypedDict(
    "ListAnnotationImportJobsRequestListAnnotationImportJobsPaginateTypeDef",
    {
        "filter": ListAnnotationImportJobsFilterTypeDef,
        "ids": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef = TypedDict(
    "_RequiredListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef = TypedDict(
    "_OptionalListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef",
    {
        "filter": ActivateReadSetFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef(
    _RequiredListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef,
    _OptionalListReadSetActivationJobsRequestListReadSetActivationJobsPaginateTypeDef,
):
    pass

_RequiredListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef = TypedDict(
    "_RequiredListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef = TypedDict(
    "_OptionalListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef",
    {
        "filter": ExportReadSetFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef(
    _RequiredListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef,
    _OptionalListReadSetExportJobsRequestListReadSetExportJobsPaginateTypeDef,
):
    pass

_RequiredListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef = TypedDict(
    "_RequiredListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef = TypedDict(
    "_OptionalListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef",
    {
        "filter": ImportReadSetFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef(
    _RequiredListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef,
    _OptionalListReadSetImportJobsRequestListReadSetImportJobsPaginateTypeDef,
):
    pass

_RequiredListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef = TypedDict(
    "_RequiredListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef",
    {
        "referenceStoreId": str,
    },
)
_OptionalListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef = TypedDict(
    "_OptionalListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef",
    {
        "filter": ImportReferenceFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef(
    _RequiredListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef,
    _OptionalListReferenceImportJobsRequestListReferenceImportJobsPaginateTypeDef,
):
    pass

ListRunGroupsRequestListRunGroupsPaginateTypeDef = TypedDict(
    "ListRunGroupsRequestListRunGroupsPaginateTypeDef",
    {
        "name": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRunTasksRequestListRunTasksPaginateTypeDef = TypedDict(
    "_RequiredListRunTasksRequestListRunTasksPaginateTypeDef",
    {
        "id": str,
    },
)
_OptionalListRunTasksRequestListRunTasksPaginateTypeDef = TypedDict(
    "_OptionalListRunTasksRequestListRunTasksPaginateTypeDef",
    {
        "status": TaskStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRunTasksRequestListRunTasksPaginateTypeDef(
    _RequiredListRunTasksRequestListRunTasksPaginateTypeDef,
    _OptionalListRunTasksRequestListRunTasksPaginateTypeDef,
):
    pass

ListRunsRequestListRunsPaginateTypeDef = TypedDict(
    "ListRunsRequestListRunsPaginateTypeDef",
    {
        "name": str,
        "runGroupId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorkflowsRequestListWorkflowsPaginateTypeDef = TypedDict(
    "ListWorkflowsRequestListWorkflowsPaginateTypeDef",
    {
        "name": str,
        "type": WorkflowTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef = TypedDict(
    "ListAnnotationStoresRequestListAnnotationStoresPaginateTypeDef",
    {
        "filter": ListAnnotationStoresFilterTypeDef,
        "ids": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAnnotationStoresRequestRequestTypeDef = TypedDict(
    "ListAnnotationStoresRequestRequestTypeDef",
    {
        "filter": ListAnnotationStoresFilterTypeDef,
        "ids": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListReadSetsRequestListReadSetsPaginateTypeDef = TypedDict(
    "_RequiredListReadSetsRequestListReadSetsPaginateTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetsRequestListReadSetsPaginateTypeDef = TypedDict(
    "_OptionalListReadSetsRequestListReadSetsPaginateTypeDef",
    {
        "filter": ReadSetFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReadSetsRequestListReadSetsPaginateTypeDef(
    _RequiredListReadSetsRequestListReadSetsPaginateTypeDef,
    _OptionalListReadSetsRequestListReadSetsPaginateTypeDef,
):
    pass

_RequiredListReadSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListReadSetsRequestRequestTypeDef",
    {
        "sequenceStoreId": str,
    },
)
_OptionalListReadSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListReadSetsRequestRequestTypeDef",
    {
        "filter": ReadSetFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReadSetsRequestRequestTypeDef(
    _RequiredListReadSetsRequestRequestTypeDef, _OptionalListReadSetsRequestRequestTypeDef
):
    pass

ListReferenceStoresRequestListReferenceStoresPaginateTypeDef = TypedDict(
    "ListReferenceStoresRequestListReferenceStoresPaginateTypeDef",
    {
        "filter": ReferenceStoreFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListReferenceStoresRequestRequestTypeDef = TypedDict(
    "ListReferenceStoresRequestRequestTypeDef",
    {
        "filter": ReferenceStoreFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListReferencesRequestListReferencesPaginateTypeDef = TypedDict(
    "_RequiredListReferencesRequestListReferencesPaginateTypeDef",
    {
        "referenceStoreId": str,
    },
)
_OptionalListReferencesRequestListReferencesPaginateTypeDef = TypedDict(
    "_OptionalListReferencesRequestListReferencesPaginateTypeDef",
    {
        "filter": ReferenceFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListReferencesRequestListReferencesPaginateTypeDef(
    _RequiredListReferencesRequestListReferencesPaginateTypeDef,
    _OptionalListReferencesRequestListReferencesPaginateTypeDef,
):
    pass

_RequiredListReferencesRequestRequestTypeDef = TypedDict(
    "_RequiredListReferencesRequestRequestTypeDef",
    {
        "referenceStoreId": str,
    },
)
_OptionalListReferencesRequestRequestTypeDef = TypedDict(
    "_OptionalListReferencesRequestRequestTypeDef",
    {
        "filter": ReferenceFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListReferencesRequestRequestTypeDef(
    _RequiredListReferencesRequestRequestTypeDef, _OptionalListReferencesRequestRequestTypeDef
):
    pass

ListReferencesResponseTypeDef = TypedDict(
    "ListReferencesResponseTypeDef",
    {
        "nextToken": str,
        "references": List[ReferenceListItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRunGroupsResponseTypeDef = TypedDict(
    "ListRunGroupsResponseTypeDef",
    {
        "items": List[RunGroupListItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRunTasksResponseTypeDef = TypedDict(
    "ListRunTasksResponseTypeDef",
    {
        "items": List[TaskListItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRunsResponseTypeDef = TypedDict(
    "ListRunsResponseTypeDef",
    {
        "items": List[RunListItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSequenceStoresRequestListSequenceStoresPaginateTypeDef = TypedDict(
    "ListSequenceStoresRequestListSequenceStoresPaginateTypeDef",
    {
        "filter": SequenceStoreFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSequenceStoresRequestRequestTypeDef = TypedDict(
    "ListSequenceStoresRequestRequestTypeDef",
    {
        "filter": SequenceStoreFilterTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef = TypedDict(
    "ListVariantImportJobsRequestListVariantImportJobsPaginateTypeDef",
    {
        "filter": ListVariantImportJobsFilterTypeDef,
        "ids": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVariantImportJobsRequestRequestTypeDef = TypedDict(
    "ListVariantImportJobsRequestRequestTypeDef",
    {
        "filter": ListVariantImportJobsFilterTypeDef,
        "ids": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListVariantImportJobsResponseTypeDef = TypedDict(
    "ListVariantImportJobsResponseTypeDef",
    {
        "nextToken": str,
        "variantImportJobs": List[VariantImportJobItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVariantStoresRequestListVariantStoresPaginateTypeDef = TypedDict(
    "ListVariantStoresRequestListVariantStoresPaginateTypeDef",
    {
        "filter": ListVariantStoresFilterTypeDef,
        "ids": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVariantStoresRequestRequestTypeDef = TypedDict(
    "ListVariantStoresRequestRequestTypeDef",
    {
        "filter": ListVariantStoresFilterTypeDef,
        "ids": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListWorkflowsResponseTypeDef = TypedDict(
    "ListWorkflowsResponseTypeDef",
    {
        "items": List[WorkflowListItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TsvOptionsTypeDef = TypedDict(
    "TsvOptionsTypeDef",
    {
        "readOptions": ReadOptionsTypeDef,
    },
    total=False,
)

_RequiredStartReadSetActivationJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartReadSetActivationJobRequestRequestTypeDef",
    {
        "sequenceStoreId": str,
        "sources": Sequence[StartReadSetActivationJobSourceItemTypeDef],
    },
)
_OptionalStartReadSetActivationJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartReadSetActivationJobRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class StartReadSetActivationJobRequestRequestTypeDef(
    _RequiredStartReadSetActivationJobRequestRequestTypeDef,
    _OptionalStartReadSetActivationJobRequestRequestTypeDef,
):
    pass

_RequiredStartReferenceImportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartReferenceImportJobRequestRequestTypeDef",
    {
        "referenceStoreId": str,
        "roleArn": str,
        "sources": Sequence[StartReferenceImportJobSourceItemTypeDef],
    },
)
_OptionalStartReferenceImportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartReferenceImportJobRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class StartReferenceImportJobRequestRequestTypeDef(
    _RequiredStartReferenceImportJobRequestRequestTypeDef,
    _OptionalStartReferenceImportJobRequestRequestTypeDef,
):
    pass

_RequiredStartVariantImportRequestRequestTypeDef = TypedDict(
    "_RequiredStartVariantImportRequestRequestTypeDef",
    {
        "destinationName": str,
        "items": Sequence[VariantImportItemSourceTypeDef],
        "roleArn": str,
    },
)
_OptionalStartVariantImportRequestRequestTypeDef = TypedDict(
    "_OptionalStartVariantImportRequestRequestTypeDef",
    {
        "runLeftNormalization": bool,
    },
    total=False,
)

class StartVariantImportRequestRequestTypeDef(
    _RequiredStartVariantImportRequestRequestTypeDef,
    _OptionalStartVariantImportRequestRequestTypeDef,
):
    pass

StoreOptionsTypeDef = TypedDict(
    "StoreOptionsTypeDef",
    {
        "tsvStoreOptions": TsvStoreOptionsTypeDef,
    },
    total=False,
)

ListAnnotationStoresResponseTypeDef = TypedDict(
    "ListAnnotationStoresResponseTypeDef",
    {
        "annotationStores": List[AnnotationStoreItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReferenceStoresResponseTypeDef = TypedDict(
    "ListReferenceStoresResponseTypeDef",
    {
        "nextToken": str,
        "referenceStores": List[ReferenceStoreDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSequenceStoresResponseTypeDef = TypedDict(
    "ListSequenceStoresResponseTypeDef",
    {
        "nextToken": str,
        "sequenceStores": List[SequenceStoreDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVariantStoresResponseTypeDef = TypedDict(
    "ListVariantStoresResponseTypeDef",
    {
        "nextToken": str,
        "variantStores": List[VariantStoreItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadSetMetadataResponseTypeDef = TypedDict(
    "GetReadSetMetadataResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "fileType": FileTypeType,
        "files": ReadSetFilesTypeDef,
        "id": str,
        "name": str,
        "referenceArn": str,
        "sampleId": str,
        "sequenceInformation": SequenceInformationTypeDef,
        "sequenceStoreId": str,
        "status": ReadSetStatusType,
        "subjectId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReferenceMetadataResponseTypeDef = TypedDict(
    "GetReferenceMetadataResponseTypeDef",
    {
        "arn": str,
        "creationTime": datetime,
        "description": str,
        "files": ReferenceFilesTypeDef,
        "id": str,
        "md5": str,
        "name": str,
        "referenceStoreId": str,
        "status": ReferenceStatusType,
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReadSetsResponseTypeDef = TypedDict(
    "ListReadSetsResponseTypeDef",
    {
        "nextToken": str,
        "readSets": List[ReadSetListItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetReadSetImportJobResponseTypeDef = TypedDict(
    "GetReadSetImportJobResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "id": str,
        "roleArn": str,
        "sequenceStoreId": str,
        "sources": List[ImportReadSetSourceItemTypeDef],
        "status": ReadSetImportJobStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartReadSetImportJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartReadSetImportJobRequestRequestTypeDef",
    {
        "roleArn": str,
        "sequenceStoreId": str,
        "sources": Sequence[StartReadSetImportJobSourceItemTypeDef],
    },
)
_OptionalStartReadSetImportJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartReadSetImportJobRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class StartReadSetImportJobRequestRequestTypeDef(
    _RequiredStartReadSetImportJobRequestRequestTypeDef,
    _OptionalStartReadSetImportJobRequestRequestTypeDef,
):
    pass

FormatOptionsTypeDef = TypedDict(
    "FormatOptionsTypeDef",
    {
        "tsvOptions": TsvOptionsTypeDef,
        "vcfOptions": VcfOptionsTypeDef,
    },
    total=False,
)

_RequiredCreateAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnnotationStoreRequestRequestTypeDef",
    {
        "storeFormat": StoreFormatType,
    },
)
_OptionalCreateAnnotationStoreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnnotationStoreRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "sseConfig": SseConfigTypeDef,
        "storeOptions": StoreOptionsTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateAnnotationStoreRequestRequestTypeDef(
    _RequiredCreateAnnotationStoreRequestRequestTypeDef,
    _OptionalCreateAnnotationStoreRequestRequestTypeDef,
):
    pass

CreateAnnotationStoreResponseTypeDef = TypedDict(
    "CreateAnnotationStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "status": StoreStatusType,
        "storeFormat": StoreFormatType,
        "storeOptions": StoreOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnnotationStoreResponseTypeDef = TypedDict(
    "GetAnnotationStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "sseConfig": SseConfigTypeDef,
        "status": StoreStatusType,
        "statusMessage": str,
        "storeArn": str,
        "storeFormat": StoreFormatType,
        "storeOptions": StoreOptionsTypeDef,
        "storeSizeBytes": int,
        "tags": Dict[str, str],
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnnotationStoreResponseTypeDef = TypedDict(
    "UpdateAnnotationStoreResponseTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "id": str,
        "name": str,
        "reference": ReferenceItemTypeDef,
        "status": StoreStatusType,
        "storeFormat": StoreFormatType,
        "storeOptions": StoreOptionsTypeDef,
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnnotationImportResponseTypeDef = TypedDict(
    "GetAnnotationImportResponseTypeDef",
    {
        "completionTime": datetime,
        "creationTime": datetime,
        "destinationName": str,
        "formatOptions": FormatOptionsTypeDef,
        "id": str,
        "items": List[AnnotationImportItemDetailTypeDef],
        "roleArn": str,
        "runLeftNormalization": bool,
        "status": JobStatusType,
        "statusMessage": str,
        "updateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartAnnotationImportRequestRequestTypeDef = TypedDict(
    "_RequiredStartAnnotationImportRequestRequestTypeDef",
    {
        "destinationName": str,
        "items": Sequence[AnnotationImportItemSourceTypeDef],
        "roleArn": str,
    },
)
_OptionalStartAnnotationImportRequestRequestTypeDef = TypedDict(
    "_OptionalStartAnnotationImportRequestRequestTypeDef",
    {
        "formatOptions": FormatOptionsTypeDef,
        "runLeftNormalization": bool,
    },
    total=False,
)

class StartAnnotationImportRequestRequestTypeDef(
    _RequiredStartAnnotationImportRequestRequestTypeDef,
    _OptionalStartAnnotationImportRequestRequestTypeDef,
):
    pass
