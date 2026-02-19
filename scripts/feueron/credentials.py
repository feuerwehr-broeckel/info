"""Shared FeuerON credential helpers."""

import os


def get_credentials() -> tuple[str, str, str]:
    """Get FeuerON credentials from environment variables.

    Returns:
        Tuple of (username, password, region_id)

    Raises:
        ValueError: If required environment variables are not set
    """
    username = os.getenv("FEUERON_USERNAME")
    password = os.getenv("FEUERON_PASSWORD")
    region_id = os.getenv("FEUERON_REGION_ID", "156")

    if not username or not password:
        raise ValueError(
            "Please set FEUERON_USERNAME and FEUERON_PASSWORD environment variables"
        )

    return username, password, region_id
