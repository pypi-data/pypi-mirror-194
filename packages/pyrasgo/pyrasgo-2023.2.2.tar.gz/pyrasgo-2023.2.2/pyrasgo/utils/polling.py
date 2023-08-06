import time
from typing import Optional

from pyrasgo import errors, schemas
from pyrasgo.config import MAX_POLL_ATTEMPTS, POLL_RETRY_RATE


def poll_anything(
    connection_obj,
    status_tracking_obj: schemas.StatusTracking,
    timeout: Optional[int] = None,
):
    """
    This function tracks status of asynchronous jobs

    Args:
        connection_obj: API object for calls
        max_poll_attempts: The maxiumum number of poll attempts
        status_tracking_obj: A StatusTracking schema to use for the first iteration of calls
        timeout: Max timeout window after which to fail the dataset publishing
        poll_retry_rate: Number of seconds between which to make another status tracking check
    """
    for i in range(1, MAX_POLL_ATTEMPTS):
        status_tracking_obj = schemas.StatusTracking(
            **connection_obj._get(f"/status-tracking/{status_tracking_obj.tracking_uuid}", api_version=2).json()
        )
        if status_tracking_obj.status == "completed":
            return status_tracking_obj.message
        if status_tracking_obj.status == "failed":
            raise errors.APIError(status_tracking_obj.message)
        if timeout and (POLL_RETRY_RATE * i) > timeout:
            raise errors.APITimeoutWarning("Timeout reached.")
        time.sleep(POLL_RETRY_RATE)
    raise errors.APIError(f"Max wait of {(MAX_POLL_ATTEMPTS * POLL_RETRY_RATE) // 60} minutes exceeded.")


def poll_dataset(
    connection_obj,
    status_tracking_obj: schemas.StatusTracking,
    timeout: Optional[int] = None,
) -> schemas.Dataset:
    """
    When publishing a dataset async, this function tracks StatusTracking
    objects and returns a dataset, if one is successfully created
    """
    ds_id = int(
        poll_anything(
            connection_obj=connection_obj,
            status_tracking_obj=status_tracking_obj,
            timeout=timeout,
        )
    )
    return schemas.Dataset(**connection_obj._get(f"/datasets/{ds_id}", api_version=2).json())


def poll_operation_set(
    connection_obj,
    status_tracking_obj: schemas.StatusTracking,
    timeout: Optional[int] = None,
) -> schemas.OperationSet:
    """
    When publishing an OperationSet async, this function tracks StatusTracking
    objects and returns an OperationSet, if one is successfully created
    """
    op_set_id = int(
        poll_anything(
            connection_obj=connection_obj,
            status_tracking_obj=status_tracking_obj,
            timeout=timeout,
        )
    )
    return schemas.OperationSet(**connection_obj._get(f"/operation-sets/{op_set_id}", api_version=2).json())
