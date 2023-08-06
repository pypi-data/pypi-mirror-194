"""Utility methods for managing storage of cached data."""

import hashlib
import logging
import shutil
from json import JSONDecodeError
from pathlib import Path

import platformdirs
from equilibrator_cache.zenodo import ZenodoSettings, get_zenodo_files

logger = logging.getLogger(__name__)

DEFAULT_KCAT_MODEL = ZenodoSettings(
    doi="10.5281/zenodo.7664120",
    filename="model_kcat_light.rds",
    md5="11e43520a63c9f4796bb8a4b08de96d4",
    url="https://zenodo.org/api/",
)

DEFAULT_KM_MODEL = ZenodoSettings(
    doi="10.5281/zenodo.7664120",
    filename="model_km_light.rds",
    md5="d36f43a79a06cac94d5b09e5e02f9254",
    url="https://zenodo.org/api/",
)


def get_data_path() -> Path:
    """Gets the path usage for storing cached data.

    Returns
    -------
    Path
        Tha cache path.
    """
    return platformdirs.user_data_path("enkie")


def clear_enkie_cache() -> None:
    """Clears the cache of the enkie package. This includes cache MetaNetX mapping files
    and cached Uniprot requests."""
    shutil.rmtree(get_data_path())


def get_cached_filepath(settings: ZenodoSettings) -> Path:
    """Get data from a file stored in Zenodo (or from cache, if available). Based on
    code by Elad Noor and Moritz Beber in equilibrator_cache,:
    https://gitlab.com/equilibrator/equilibrator-cache/-/blob/2249b3f334ebe8eed9b62475644bf7a2e385cde1/src/equilibrator_cache/zenodo.py

    Parameters
    ----------
    settings : ZenodoSettings
        Configuration for the interaction with Zenodo.org.

    Returns
    -------
    Path
        The path to the locally cached file.

    """

    cache_fname = get_data_path() / settings.filename

    if cache_fname.exists():
        if hashlib.md5(cache_fname.read_bytes()).hexdigest() == settings.md5:
            return cache_fname

    # If the checksum is not okay, it means the file is corrupted or
    # exists in an older version. Therefore, we ignore it and replace it
    # with a new version.
    logger.info("Downloading model parameters from Zenodo.")
    try:
        dataframe_dict = get_zenodo_files(settings)
    except JSONDecodeError as exc:
        raise IOError(
            "Some required data needs to be downloaded from Zenodo.org, but "
            "there is a communication problem at the "
            "moment. Please wait and try again later."
        ) from exc

    for filename, data in dataframe_dict.items():
        (get_data_path() / filename).write_bytes(data.getbuffer())

    logger.info("Validate the downloaded copy using MD5 checksum '%s'.", settings.md5)
    md5 = hashlib.md5(cache_fname.read_bytes()).hexdigest()
    if md5 != settings.md5:
        raise IOError(
            f"The newly downloaded Zenodo file (DOI: {settings.doi} -> "
            f"{settings.filename}) did not pass the MD5 "
            f"checksum test: expected ({settings.md5}) != actual ({md5})."
        )

    return cache_fname
