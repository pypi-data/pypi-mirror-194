from enum import Enum
from typing import Any, Literal, Optional, overload

import pandas as pd
import pyspark.sql

from bbg.secrets import Client, get_db_secret
from ._typing import Connection
from ._pyspark import PySparkQuery, PySparkConnection, Read, Write, Mode


class Watermarks(Connection, Enum):
    """The Watermarks SQL connection."""
    _connection: Optional[PySparkConnection]

    CONNECTION = None

    def __init__(self, value: None) -> None:
        self._connection = None

    def _clean(self, query: str) -> str:
        """Cleans a query by adding parentheses and table_alias."""
        query = super()._clean(query)
        if not query.startswith("("):
            query = "(" + query
        if query.count(")") < query.count("("):
            query += ")"
        if not query.endswith("table_alias"):
            query += " table_alias"
        return query

    def _ensure_connection(self) -> PySparkConnection:
        if self._connection is not None:
            return self._connection
        secrets = [
            get_db_secret(key)
            for key in ("BaseName", "BaseScope", "environment")
        ]
        hostname = "-".join(secrets) + "-sqlserver.database.windows.net"
        database = "".join(secrets) + "metadatadb"
        with Client.connect() as client:
            username = client.get_secret("metadatadbadminuser")
            password = client.get_secret("metadatadbadminpass")
        port = 1433
        url = f"jdbc:sqlserver://{hostname}:{port};database={database}"
        properties = {
            "user": username,
            "password": password,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        }
        connection = PySparkConnection(url, properties)
        self._connection = connection
        return connection

    @overload
    def query_pyspark(self, query: str, mode: Read = ...) -> pyspark.sql.DataFrame: ...

    @overload
    def query_pyspark(self, query: str, mode: Write) -> None: ...

    def query_pyspark(self, query: str, mode: Mode = "read") -> Optional[pyspark.sql.DataFrame]:
        """
        Query the Watermarks connection and cache any missing metadata from
        the Azure key vault if missing. This requires the dbutils
        global variable to be set before running.

        Parameters:
            query:
                A SQL table query.
            mode:
                Either read, append, overwrite, ignore, or error.
                If read, results are returned as a dataframe.
                Otherwise, None is returned.

        Returns:
            df:
                A PySpark DataFrame if mode="read".

        Returns:
            df:
                A PySpark DataFrame if mode="read".

        Example:
            >>> query = '''
            ...     select
            ...         COUNT(DISTINCT "OrderID")
            ...     from
            ...         "SUPPLYCHAIN"."csg.Models.SupplyChain.Data::SalesOrders"
            ... '''
            >>> df = connection.query_pyspark(query)
        """
        return self._ensure_connection().query_pyspark(self._clean(query))

    @overload
    def query(self, query: str, mode: Read = ...) -> pd.DataFrame: ...

    @overload
    def query(self, query: str, mode: Write) -> None: ...

    def query(self, query: str, mode: Mode = "read") -> Optional[pd.DataFrame]:
        """
        Query the Watermarks connection and cache any missing metadata from
        the Azure key vault if missing. This requires the dbutils
        global variable to be set before running.

        Parameters:
            query:
                A SQL table query.
            mode:
                Either read, append, overwrite, ignore, or error.
                If read, results are returned as a dataframe.
                Otherwise, None is returned.

        Returns:
            df:
                A PySpark DataFrame if mode="read".

        Returns:
            df:
                A Pandas DataFrame if mode="read".

        Example:
            >>> query = '''
            ...     select
            ...         COUNT(DISTINCT "OrderID")
            ...     from
            ...         "SUPPLYCHAIN"."csg.Models.SupplyChain.Data::SalesOrders"
            ... '''
            >>> df = connection.query(query)
        """
        return self._ensure_connection().query(self._clean(query))

    def select(self, *args: str, **kwargs: Any) -> PySparkQuery:
        return self._ensure_connection().select(*args, **kwargs)


watermarks = Watermarks.CONNECTION
