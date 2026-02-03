"""
Salesforce OAuth 2.0 Authentication Plugin

Provides OAuth 2.0 Client Credentials authentication for Salesforce API access.
REQ: openspec/changes/salesforce-bulk-api-dag/specs/sf-oauth-auth/spec.md
"""

from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class SalesforceAuthError(Exception):
    """Raised when Salesforce authentication fails."""


def get_salesforce_token(conn_id: str = "salesforce_api") -> dict[str, Any]:
    """
    Authenticate to Salesforce using OAuth 2.0 Client Credentials flow.

    Reads client_id, client_secret, and host from an Airflow Connection.

    Args:
        conn_id: Airflow Connection ID containing Salesforce credentials.
            - login: client_id (Consumer Key)
            - password: client_secret (Consumer Secret)
            - host: Salesforce base URL (e.g. https://instance.my.salesforce.com)

    Returns:
        dict with keys: access_token, instance_url, token_type

    Raises:
        SalesforceAuthError: If authentication fails or connection fields are missing.
    """
    from airflow.hooks.base import BaseHook

    # Read credentials from Airflow Connection
    conn = BaseHook.get_connection(conn_id)

    client_id = conn.login
    client_secret = conn.password
    host = conn.host

    # Validate required fields
    missing = []
    if not client_id:
        missing.append("login (client_id)")
    if not client_secret:
        missing.append("password (client_secret)")
    if not host:
        missing.append("host (base URL)")

    if missing:
        raise SalesforceAuthError(
            f"Airflow Connection '{conn_id}' is missing required fields: {', '.join(missing)}"
        )

    # Ensure host has scheme
    if not host.startswith("http"):
        host = f"https://{host}"

    token_url = f"{host.rstrip('/')}/services/oauth2/token"

    logger.info(f"Authenticating to Salesforce at {host}")

    response = requests.post(
        token_url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error_description", error_data.get("error", "Unknown error"))
        except Exception:
            error_msg = response.text

        raise SalesforceAuthError(
            f"Salesforce authentication failed (HTTP {response.status_code}): {error_msg}"
        )

    data = response.json()

    logger.info(f"Authenticated successfully. Instance: {data.get('instance_url')}")

    return {
        "access_token": data["access_token"],
        "instance_url": data["instance_url"],
        "token_type": data.get("token_type", "Bearer"),
    }
