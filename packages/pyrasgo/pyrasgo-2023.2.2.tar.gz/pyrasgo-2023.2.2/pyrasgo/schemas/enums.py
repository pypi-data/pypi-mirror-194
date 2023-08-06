from enum import Enum


class DataWarehouseType(Enum):
    """
    Supported Data Warehouses
    """

    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
