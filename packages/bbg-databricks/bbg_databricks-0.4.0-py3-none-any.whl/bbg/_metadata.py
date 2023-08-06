from ._globals import get_global

def load_file(source: str, filename: str) -> None:
    """
    Loads a file from "dbfs:/mnt/filename" to "file:/tmp/source/filename"
    to be used in databricks.

    Parameters:
        source:
            The directory in tmp to store the file.
        filename:
            The name of the file.

    Example:
        >>> load_file(
        ...     "metadata/processed/raw_to_processed_metadata.json",
        ...     "HANASidecarOnPrem",
        ... )
    """
    get_global("dbutils").fs.cp(
        f"dbfs:/mnt/{filename}", f"file:/tmp/{source}/{filename}"
    )
